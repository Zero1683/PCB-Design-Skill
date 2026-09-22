# PCB inspection and routing toolkit

Use this at G3-G5 when actual exports are available: extracting native PCB geometry,
checking placement and routing space, comparing physical connectivity, inspecting
manufacturing artwork, or preparing a supported DSN/SES routing round trip.

The bundled implementation is an adapted subset of daishuge/pcb-skill, pinned and
licensed in [UPSTREAM.md](../vendor/pcb-skill-toolkit/UPSTREAM.md). It supplies tools;
our requirements, schematic formats, stage gates, manufacturing scope and assembly
choices continue to govern the task. It does not install a second EDA bridge.

## Entry point and dependencies

Run from this skill's directory, passing project files by absolute path:

```sh
python scripts/pcb_toolkit.py --help
python scripts/pcb_toolkit.py import /project/checks/board.json /project/exports/board.epcb /project/exports/footprints --rules /project/checks/rules.json --layers /project/checks/layers.json
python scripts/pcb_toolkit.py courtyard /project/checks/board.json
python scripts/pcb_toolkit.py bodies /project/checks/board.json
python scripts/pcb_toolkit.py channels /project/checks/board.json --track-width <actual-mm>
python scripts/pcb_toolkit.py nets /project/checks/board.json /project/checks/assertions.json
python scripts/pcb_toolkit.py reconcile /project/checks/board.json --netlist /project/exports/schematic-netlist.json
```

Python 3.10+ is required by our adapter. Most tools use the standard library.
`raster` and `clearance` additionally need NumPy in that same Python environment;
it is not bundled. Inspect the existing environment before installing anything.
If unavailable, record those checks as NOT_RUN and continue other checks. Do not
translate a skipped self-test or missing package into PASS. Use the task's chosen
dependency/cache locations; do not install tools globally as a side effect.

Tool flags and data shapes: [placement](../vendor/pcb-skill-toolkit/scripts/placement/README.md),
[routing](../vendor/pcb-skill-toolkit/scripts/routing/README.md),
[manufacturing checks](../vendor/pcb-skill-toolkit/scripts/verify/README.md).
Their measured example values describe the upstream board only.

## Extract once, prove coverage, retain the source

1. Export the actual selected PCB and its referenced footprints. Preserve raw
   exports, baseline, client version, input hashes, rule sources and extraction
   command beside results. Never reconstruct an export from what the drawing
   was intended to contain.
2. Supply full `rules.json` and `layers.json` as defined by the placement README.
   The adapter requires explicit positive clearances and the actual layer map;
   do not inherit its example four-layer map or zero courtyard gap. Derive values
   from the chosen fabricator, assembly method and selected components. Copper,
   hole, body and silkscreen clearances remain separate checks.
3. The importer rejects missing footprints, duplicate designators, empty PCBs
   and multiple PCB documents. Its `import_coverage` counts are only a starting
   check. Independently reconcile native component/pad/hole/track/via counts,
   layers and outline against the readback. Unsupported primitives, history
   encodings and omitted data must be resolved before accepting geometry results.
4. Calibrate units, pad rotation and bottom-side mirroring on a known asymmetric
   footprint from this client/version. Compare actual pad coordinates, not only
   a plausible-looking rectangle. Outline curves are approximated; tight edge
   clearances and cutouts need native or exact geometric checks.
5. Use [the reconciliation adapter](20-data-and-recovery.md) to bind this toolkit's
   board JSON to an actual normalized PCB snapshot from reference 10. It checks
   component/pin correspondence and preserves both contracts for existing tools;
   do not pass one shape directly into the other's checker. Independent intent
   still comes from requirements and exact-part documentation (reference 13).

## Use results at the relevant stage

| Stage | Tool / useful evidence | Remaining check |
|---|---|---|
| G3 | `courtyard`, `bodies`: pad/hole envelopes, body conflicts | Pad, silk and mask gates in reference 14; exact bodies and assembly access |
| G3 | `channels`: track capacity, via corridors, escape space | Estimate only; confirm feasible critical routing and actual native result |
| G3/G5 | `mesh`: fresh OBJ geometry, modeled-part count, overlapping boxes | Missing models, connector insertion direction/space, flexible parts and tolerances |
| G4 | `nets`, `reconcile`, `route-accept`: physical groups and pin-map comparison | Actual copper pours, complete rules and native DRC/ERC |
| G5 | `outline`, `drills`, `mask`, `gerber` | Supported format coverage, cutouts/slots and assembly needs |
| G5 | `raster`, `clearance`: manufactured copper occupancy/gaps | Resolution limit, all required layers, supported polarity, actual net attribution |

A same-net exemption for copper must never exempt hole spacing or component
assembly clearance. For antenna areas, inspect all applicable copper layers and
drills from the final frozen package; a graphical keepout boundary is insufficient.
Retain region bounds, pixel pitch, measured occupancy and layer identity in evidence.

## Hardened behavior and limits

- Use the public wrapper with input files before options. Misspelled, duplicate,
  missing-value and malformed inspection options are rejected. Do not weaken a
  board's clearance rule through a command-line override.
- Physical connectivity distinguishes copper on a layer from a plated barrel.
  NPTH features never bridge layers. Drilled pads require explicit plating; vias
  with explicit spans connect only their contiguous declared copper layers. Legacy
  neutral vias without type/span still mean through-vias. Verify that assumption
  against the native export. Plane assumptions require reaching a declared plane.
- Repeated-number pads contribute every physical land to connection, isolation
  and open-pin assertions. A correct final land cannot hide a disconnected or
  shorted earlier land. This geometry model excludes drill-void subtraction and
  actual copper pours; it does not replace native DRC or final-artwork inspection.
- `route-accept --protected N --baseline before.json` compares straight-segment,
  pad and via geometry. Equivalent collinear segmentation is allowed; changed
  paths, widths, layers, pads or via spans fail even if connectivity remains one
  island. Missing baselines and empty netted-pad coverage are NOT_CHECKED.
- `mask` uses the union of supported mask flashes and simple linear regions.
  Offset openings and multiple openings may together cover a pad. Full pad-area
  coverage passes; no positive-area opening fails. Partial openings are NOT_CHECKED
  by default. Use `--allow-partial-openings` only with a documented solder-mask-defined
  pad policy; its PASS proves positive opening area, not sufficient solderable area.
  Review actual opening dimensions and mask dams separately.
- Untagged copper flashes need `--assume-all-pads` plus an independent pad-count
  check; via identity is then unavailable. Empty pad scopes, stroked mask openings,
  compound/hole regions, region arcs and unsupported commands remain NOT_CHECKED.
  `--tol` affects concentric expansion reporting only, never opening coverage.
  Results record state, checked/excluded objects and policy. Floating-point geometric
  resolution is limited; it is not a fabrication tolerance.
- Native record import currently rejects BLIND vias, nonempty via rule references,
  missing via type and unmodeled inner-layer lands. Array-format VIA and actually
  drilled PAD records are rejected until their field meanings are verified.
  Retain the export and use a supported native check; never delete these features
  to obtain a passing import.

- The outline checker reconstructs actual segment endpoints into one simple ring.
  Shuffled/reversed edges are supported; gaps, branches, overlaps, self-intersections,
  multiple rings and internal cutouts are rejected. It never substitutes a bounding
  box for the board boundary. Centreline dimensions are the finished outline;
  do not subtract the drawing pen width.
- Requested copper and drill edge margins are enforced, including complete copper
  edges and slot centrelines at concave notches. Omitted files are NOT CHECKED;
  explicitly supplied empty layers remain incomplete. A valid intentionally empty
  layer needs a scoped N_A review, not a false claim that geometry was checked.
  Arcs and some rounded apertures remain approximated; use independent exact/native
  inspection for near-threshold curves and unsupported cutouts.
- Reconciliation retains every physical land using its element identity. Same-number
  lands must each have a unique element ID and explicit element-net observation;
  legitimate same-number/same-net lands remain supported. Conflicting number/element
  maps, missing identities and contradictory schematic net memberships fail.
- Assertion contracts reject empty/unknown/malformed rules. Every named net and
  pad must resolve. An unresolved target is a failure, including isolation and
  open-pin assertions. Valid rules still cover only the relationships specified.
- Gerber dark/positive polarity is supported. Clear/negative polarity and
  non-identity transforms are rejected before geometric checks; these features
  are **not implemented** by this integration. Use a capable independent reader
  for such files. Never remove commands or regenerate altered artwork just to
  make this reader pass. Preserve the original manufacturing package.
- Gerber raster results have a pixel-size limit; mesh checks use axis-aligned
  boxes, not full solid intersection. Unknown/missing models remain unchecked.
  Courtyard/body fallback to library graphics needs confirmation.
- `--plane-nets` models assumed connection through a plane. It is not a
  measurement of actual fill continuity; verify final copper separately.
- `--expect-open` permits deliberately deferred nets during routing work. It
  does not waive required final connections or grant G4/G5 acceptance.
- A script exit code is one result with a stated scope, never a whole-board
  approval. Record source coverage, assumptions, unresolved warnings and baseline
  using existing CHECKS/evidence tools. Native visualization and save/reopen
  remain required; keep the existing two-format schematic gates unchanged.

## Optional external autorouting

Use native EasyEDA routing when suitable. For a supported external router, the
toolkit adds `dsn-rewrite`, `dsn-slim`, `ses-import`, `route-watch` and
`route-accept`; no router/JVM or external service is installed or launched.

1. Freeze the input board and record protected critical nets, actual stackup,
   widths, clearance and plane layers. Scope any replacement of existing copper.
2. Use an exclusive per-run output directory. Record a Unix start timestamp
   **before launching the router**, plus DSN/config/input hashes and router
   version. Do not reuse an old session path. Keep a fresh log for the run.
3. If attaching the watcher after the router starts, pass the recorded timestamp:

   ```sh
   python scripts/pcb_toolkit.py route-watch --log /project/run/route.log --output /project/run/route.ses --pid <pid> --started-at <unix-seconds> --max-seconds <budget>
   ```

   Without that argument the watcher uses its own start time. Output must be
   nonempty, stable and at least as recent as this run. A stale/growing file does
   not hide crash/timeout checks. Windows process probing uses a read-only handle,
   not os.kill. Exit 0 reports a **fresh stable file candidate**, not a parsed,
   complete or correct route. `--once` while still running exits 5, not success.
   PID access errors mean unknown, not that the process is gone.
4. Parse the candidate and check expected nets/counts/layers; protected routes,
   intentional exclusions and unit conversions must match the input record.
   Convert into a copy first. `--strip` requires verifying that the selected
   records really are replaceable routing, not outline/silk or unrelated work.
5. Import through the selected EDA backend, read back fresh native data, rebuild
   affected pours, inspect/save/reopen, then run connection, spacing and native
   checks. Validate generated manufacturing files from that same final revision.

The progress relay is retained as a patched optional utility, not part of the
default invocation path. Do not configure or use an external messaging transport
without the user's explicit authorization. Automatic approval watchers and the
upstream purchasing/setup workflow are not bundled or activated.

Mask aperture macros are evaluated from their actual exposed literal outline,
including a macro named RoundRect. Parameterized/compound RoundRect exports need
an independent capable checker; their names or ADD dimensions cannot establish
geometry. Native EasyEDA parameterized macro exports have not been qualified.
