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
5. This toolkit's **board JSON is a different contract** from reference 10's
   normalized component snapshots. Do not rename or pass it to audit_design.py
   or check_connectivity.py as if interchangeable. Preserve both exports with the
   same baseline if using both toolchains. Independent circuit intent still
   comes from requirements and exact-part documentation (reference 13).

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
