# `scripts/` — PCB placement, routing and fabrication checkers

Python 3, standard library, one optional numpy dependency. Every script says in its own
docstring **what it measures, what it cannot see, and how it was validated** — the blind
spots are the most useful part, so read them before you trust a `PASS`.

These are a port of tooling that took a real 4-layer board through placement, autorouting
and fabrication release. Numbers quoted throughout ("0.1020 mm", "3326 protected traces",
"10 h 53 m") are measurements from that project, kept because a specific number is
evidence and a rounded one is a story.

---

## The four directories

```
placement/   is this layout buildable, and can it be routed?
routing/     the DSN/SES autoroute chain, and how to know it worked
verify/      measure the artefact that gets built
notify/      make a long job's silence mean something
```

Each has its own `README.md` with the exact invocations and the traps. Keep `scripts/`
together: `routing/` and `verify/` import the geometry core and board model from
`placement/` by relative path.

---

## How they fit together

```
   EDA export ──► placement/import_easyeda.py ──► board.json ─┐
                                                              │
   board.json ──► placement/courtyard_check.py                │  courtyards, pad/drill
              ──► placement/body_clearance.py                 │  to outline, hole to
              ──► placement/channels.py                       │  hole, bodies, channels
                                                              │
   raw .dsn   ──► routing/dsn_rewrite.py ──► routing/dsn_slim.py ──► your router
                                                              │
   .ses       ──► routing/ses_import.py ──► push ──► PULL BACK ┘
   readback   ──► placement/import_easyeda.py ──► after.json
   after.json ──► routing/route_accept.py            (islands merged, planes, clearance)
      (watched throughout by routing/route_supervise.py and notify/progress_relay.py)

   gerber/    ──► verify/outline_check.py  verify/drill_census.py  verify/mask_check.py
              ──► verify/clearance.py      verify/raster.py --compare-fills
   board.json ──► verify/pad_reconcile.py  verify/netlist_assert.py
   3D export  ──► verify/mesh3d.py
```

One rule runs through all of it: **judge the artefact, not the intention.** Verify the
document the EDA hands back, not the one you pushed; measure the Gerber, not the design
model; parse the 3D export you just made, not a cached one.

---

## The board JSON

One EDA-independent document that every checker reads. Porting the toolkit to another
EDA means writing a sibling of `placement/import_easyeda.py` and nothing else. The schema
is in `placement/README.md`; `placement/boardmodel.py --selftest` builds a valid one in
memory if you want to see the shape.

---

## Dependencies

| | |
|---|---|
| Python | 3.6+ (tested on 3.9) |
| stdlib only | everything except the two below |
| numpy | `verify/raster.py` and `verify/clearance.py` only |

Both numpy users check for it, exit with a clear message if it is missing, and report
`SKIPPED` from `--selftest` rather than failing. No other third-party package is used
anywhere, and nothing here writes an image with an image library — the PNG writer is
`zlib` and `struct`.

---

## Self-tests

Every script runs on synthetic input with no board, no EDA and no network:

```sh
cd scripts
for d in placement routing verify notify; do
  for f in $d/*.py; do
    python3 "$f" --selftest 2>&1 | tail -1
  done
done
```

A self-test is not a substitute for running the tool on a real export. Several of the
faults below are **alignment-dependent and do not reproduce from clean synthetic
geometry** — which is precisely why they survived so long.

---

## The four tool faults

Every one of these was found in the original scripts, on a released board, and every one
of them **passed a check that was not actually checking**. All four are fixed in what is
published here, each noted in the code comment where it lives.

| # | fault | where it was | fixed in |
|---|---|---|---|
| 1 | a **pickle-cached 3D model** measuring the *previous release* — 95 430 vertices instead of 107 775, reporting 0 interferences on a board that had three | 3D gate | `verify/mesh3d.py` |
| 2 | a **polygon-distance function blind to full containment** — a land that had entirely swallowed an 0805 pad still read 0.22 mm clear | clearance core | `placement/geom2d.py` |
| 3 | a **placement gate that only tested bodies ≥ 20 mm²** — so an 0603 was legally placed under a 9.8 mm² tantalum, because nothing was looking | placement | `placement/body_clearance.py` |
| 4 | a **raster fill leaking through a plane's keyhole cut-ins**, merging two physically separate copper regions into one label — an isolated via read as shorted to the ground plane, and every Gerber-side clearance number on the project had been computed on merged labels | Gerber raster | `verify/raster.py` |

Two more from the same family, equally silent:

* **the clearance sweep skips same-net pairs — right for copper, wrong for holes.** Three
  stacked router vias passed the sweep and failed the real DRC.
  → `placement/courtyard_check.py` is net-blind about holes.
* **one drill file can be a strict subset of another**, so summing them nearly doubled the
  count. → `verify/drill_census.py` proves the subset relation and reports the union.

---

## Genericising

Nothing here carries a board-specific constant. Rules, layer ids, net names, widths,
budgets and paths are all arguments or small JSON configs. Where a number from the
reference project is shown — 0.102 mm clearance, 0.2997 mm hole-to-hole, 41.4 × 100 mm,
621 drill hits, 0.19 mm for ≈106 Ω differential lanes — **it is labelled as an example and
it is a property of that board and that fabricator.** Substitute your own; none of them is
a default you should inherit.

---

## Licence and provenance

Ported from working tooling, not rewritten from a description. Where the original made a
choice for a measured reason, the reason is in the code comment next to the choice —
including the ones that were wrong the first time.
