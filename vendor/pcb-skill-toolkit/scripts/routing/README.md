# `routing/` — the Specctra DSN/SES autoroute chain, and how to know it worked

Five scripts covering one loop: hand a router a DSN it can actually route, watch it so a
stall cannot go unnoticed, convert the session file back, and judge the result on the
board the EDA hands back.

Nothing here launches a router. That is deliberate: which router, which JVM, which flags
and which machine are yours, and a wrapper that hides them makes a failed run harder to
read, not easier.

---

## The files

| file | what it does |
|---|---|
| `dsn_rewrite.py` | patch an EDA-exported `.dsn`: solid planes → `(type power)`, per-net widths, **bare class members**, optional board-edge keepout |
| `dsn_slim.py` | keep only the protected wiring worth protecting; drop nets the router must not be given |
| `ses_import.py` | parse a `.ses` and write neutral wiring JSON, or append records to a `.epcb` |
| `route_accept.py` | acceptance on the read-back board; progress metric is **islands merged** |
| `route_supervise.py` | four-state watchdog + connections-per-minute floor |

`route_accept.py` reads the board JSON produced by `../placement/import_easyeda.py` and
imports `geom2d`/`boardmodel` from `../placement`, so keep `scripts/` together.

---

## The loop

```sh
# 0. before you route at all: is the placement routable?
python3 ../placement/channels.py board.json --track-width 0.10

# 1. patch the export
python3 dsn_rewrite.py raw.dsn tuned.dsn --config route.json --min-classes 100

# 2. cut it down to what the router should be asked to do
python3 dsn_slim.py tuned.dsn slim.dsn \
        --keep "NET_A_P,NET_A_N,NET_B_P,NET_B_N" --drop "GND" --min-kept 10

# 3. run YOUR router, however you run it, writing a log and a .ses
#    ... and in another shell, watch it:
python3 route_supervise.py --log route.log --output route.ses --pid $ROUTER_PID \
        --poll 30 --max-seconds 50400 --min-rate 0.10

# 4. convert the session file
python3 ses_import.py route.ses --format easyeda -o merged.epcb \
        --base current.epcb --layer-map layers.json --strip \
        --protected "NET_A_P,NET_A_N" --keep-nets "GND" \
        --forbid-layers "Inner1"

# 5. push it, then PULL IT BACK and judge the read-back, never the pushed file
python3 ../placement/import_easyeda.py after.json readback.epcb footprints/
python3 route_accept.py after.json --baseline before.json \
        --protected "NET_A_P,NET_A_N" --plane-nets "GND" --expect-open "VBUS"
```

Every script self-tests:

```sh
for f in dsn_rewrite dsn_slim ses_import route_accept route_supervise; do
  python3 $f.py --selftest
done
```

---

## `dsn_rewrite.py` — four edits, all of them paid for

1. **Solid inner planes become `(type power)`.**
   An EDA exports a solid ground plane as `(type signal)`. A router given that will cut
   the reference plane to pieces, and every impedance-controlled pair loses its
   reference. If the "layer block not found" assertion fires, **stop** — the export
   format changed and every other edit is now unverified.

2. **Per-net widths.** Widths set by *physics* (impedance, IPC-2221 current) rather than
   by routing convenience must be pinned per class, or dropping the default silently
   halves them.

3. **Class members are emitted BARE.** This is the expensive one. The EDA writes
   `(class X 'X' …)` — the net name **single-quoted** — and the router then binds the
   class to nothing. Every net comes back at the structure default width. A 40-minute
   run was lost to this, with a nominally-90 Ω pair routed at roughly 120 Ω, before
   anyone noticed. The rewritten class emits `(class X X …)`.

4. **Optional board-edge keepout ring.** A router honours only the *class* clearance
   from the DSN boundary, not the board's edge rule: measured, with a 0.115 mm class
   clearance it placed a via **0.2036 mm** from the outline against a 0.29972 mm rule.
   Insetting the boundary polygon instead makes FreeRouting fail on load (*"Polyline:
   must contain at least 2 different points"*, then an NPE), so the cure is a keepout
   **ring** on every copper layer. Your real edge margin is `ring + clearance`.

**Ask for a little more clearance than the rule.** FreeRouting works in 1/1000 mil
integers and lands tracks *exactly* on whatever the DSN asks for, so asking for the
board's own rule produced gaps 0.1–1.6 µm **short** of it. Ask for more in the DSN;
measure the finished board against the real rule.

### Config (all lengths in **millimetres**)

```json
{
  "plane_layers":    ["Inner1"],
  "default_width":   0.10,
  "clearance":       0.115,
  "widths":          {"USB_DP": 0.20, "USB_DM": 0.20, "VSYS": 0.30, "GND": 0.30},
  "width_patterns":  [["^MIPI_", 0.19]],
  "extra_clearance": {"HV_RAIL": 0.30},
  "edge_keepout":    {"ring": 0.20, "board": [41.4, 100.0],
                      "layers": ["TopLayer","Inner1","Inner2","BottomLayer"]}
}
```

**These numbers are the example project's**, shown so the shape is clear: a 41.4 × 100 mm
4-layer board whose rule is 0.102 mm, whose USB pair wants 0.20 mm, whose MIPI lanes
were computed at 0.19 mm for ≈106 Ω differential on that stack-up, and whose backlight
rail carries 22–26 V so it gets 0.30 mm. **None of them transfers to your board.**

`--min-classes N` is not decoration: a regex that matches nothing is indistinguishable
from a file that needed no change, which is how the bare-member fault hid. Set it.

---

## `dsn_slim.py` — fewer protected traces, not more stack

Feeding a router every existing trace as protected wiring **overflows its stack**.
Measured: 3326 protected traces crashed FreeRouting inside `PolylineTrace.combine`,
which recurses once per trace in a connected chain. `-Xss512m` only moved the crash from
3 seconds to 11 minutes. Keeping 51 wires plus 7 vias let the run complete.

Two edits:

* **wiring** — keep only copper that is finished, verified and expensive to redo;
* **network** — drop nets the router must not be given:
  * **poured nets** (a plane plus pours is not a routing problem; laying traces for it
    wastes channel width on copper the pour would have made anyway);
  * **nets the router physically cannot do.** Measured: after five passes and 39 minutes
    the router had laid **zero** segments of nine power rails — every rail's island count
    still equalled its pad count — while burning 105 s per connection gained, because
    0.50 mm of track plus two 0.102 mm clearances needs 0.704 mm and the placement's
    channels were 0.55 mm.

**A dropped net is not routed.** Something else must close it, and `route_accept.py`
must be told to expect it (`--expect-open`), or you will ship an open circuit that every
gate called a pass. `--min-kept` / `--max-kept` guard a filter that matched nothing or
everything.

---

## `ses_import.py` — four numbers and one merge trap

1. **SES integers are 1/1000 mil** — coordinates *and* widths — while the EDA's own DSN
   numbers are plain mil. Getting it wrong silently produces 2.5 mm-wide tracks that
   look like a routing disaster rather than a units bug. The parser reads
   `(resolution <unit> <n>)` and refuses a unit it does not know.
2. **`(via <padstack> <x> <y>` has no closing paren on its line.** A regex expecting one
   matches nothing and reports "0 vias", which reads like a router that chose not to use
   any.
3. **The router quotes a net name only when it needs to.** `(net "A_NET"` and `(net VSYS`
   occur in the *same* file; a parser matching only the quoted form silently dropped 15
   nets including every power rail.
4. **Protected copper is echoed back.** Re-adding it duplicates every segment. Name it
   with `--protected`.

**The merge trap:** when the router routed from scratch, its result knows nothing about
the copper still on the board. Measured: merging one such session onto a board that
still held its previous 3275 tracks produced **1783 clearance violations**, with overlaps
to −0.15 mm. `--strip` removes the old routing first — but `--strip` is only safe when
you have checked that every strippable record really is routing. On the reference board
that was checked and true: every `LINE` record was copper and carried a net name, with no
silkscreen or outline geometry among them. **Check yours.**

`--forbid-layers "Inner1"` is fatal by design: copper on a declared solid plane means the
DSN did not declare it as a plane, and the session is not usable.

---

## `route_accept.py` — islands merged

```
islands = Σ over nets of that net's island count
merges  = Σ over nets of (islands − 1)      ← the work still to do
```

**Merges outstanding is the progress metric.** Not "percent routed", not "unrouted
connections". It is monotone, comparable between runs, and goes to zero exactly when the
board is connected — which is what makes two candidate sessions comparable on one ruler.
`--baseline` prints the delta.

Gates: protected nets remain one island and preserve baseline geometry · solid planes uncut · different-net clearance at
the rule · merges == 0. `--expect-open` moves deliberately-withheld nets out of the
failure count **and lists them every time**, so "we meant to do that" stays a decision
somebody made rather than a silence.

**It cannot see pour copper.** A net closed by a pour keeps reporting islands here
forever, and that is the wrong ruler for it. `--plane-nets` models it: each island
holding a via or a through-hole pad is treated as reaching the plane. For the real
answer, measure the manufactured artwork with `../verify/clearance.py`.

Validated: on a released board it reproduces that board's minimum different-net gap of
**0.1020 mm** over ~40 000 examined pairs, in about a quarter of a second.

---

## `route_supervise.py` — four states plus a rate floor

A router can fail four ways and only one looks like a failure. A run was left alone for
**10 hours 53 minutes** because nothing said anything: the process was alive, the log was
growing, and it had stopped making progress hours earlier.

Checked every `--poll` seconds, **in this order**:

| # | state | why it is separate |
|---|---|---|
| 1 | **output present** | checked first — a router that finishes and exits also trips 3 and 4 |
| 2 | **crash signature** | a stack overflow or OOM looks like ordinary output to a size check; a JVM dying in a worker thread can still exit 0 |
| 3 | **process gone** | a silent death is a different failure from a crash with a message |
| 4 | **wall clock** | a cap never reached costs nothing; a missing one costs a night |
| 5 | **rate floor** | see below |

**Judge connections per MINUTE, not per pass.** A router's passes get longer as the board
fills — 2:59 → 9:56 on one measured run — so a fixed per-pass threshold silently tightens
and condemns a run that is still working. With fewer than `--rate-window` timed passes the
verdict is `unknown`, **never** `stalled`: a run that has not produced enough evidence has
not failed. If `--pass-regex` matches nothing the rate check reports itself as
*unavailable* rather than as zero.

**This supervisor never kills anything.** It reports a verdict and exits with a code
(0 fresh stable output candidate · 1 crash · 2 gone · 3 clock · 4 rate;
5 means a --once query is still running). Killing a job that is 95 % done because
a threshold fired is a bad thing to automate.

`--rate-only route.log` prints just the per-pass table, which is the quickest way to see
whether a run is worth waiting for.

## Local integration: run identity

The watcher rejects output older than the run start. Supply --started-at with the
Unix timestamp recorded before launching the router when attaching later; otherwise
the watcher uses its own start time. Always use a fresh per-run directory/log and
record input hashes. Exit 0 only identifies a fresh stable candidate; parse and
verify the route before accepting it. Windows PID checks use non-destructive
process handles. Access failure is unknown, not proof of process exit.

Local acceptance scope: `--protected` requires `--baseline`; equivalent collinear
segmentation is accepted, while changed copper geometry fails. Empty netted-pad
coverage and unsupported geometry return NOT_CHECKED. NPTH never bridges layers;
explicit via spans are respected. Plane-net connectivity remains an assumption.
Compare island deltas only when the intended object/net inventory is unchanged.
