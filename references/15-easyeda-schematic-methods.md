# EasyEDA schematic methods

Use this reference when creating or revising an EasyEDA schematic. It integrates
the useful recipes from the bundled [schematic enhancement skill](../vendor/easyeda-schematic-net-fanout/SKILL.md)
with this project's drafting and verification workflow. Source/version details
are in [UPSTREAM.md](../vendor/easyeda-schematic-net-fanout/UPSTREAM.md).

## Operating foundation and loading order

1. Read [EDA operations](06-easyeda-execution.md) and the bundled
   [API entrypoint](../vendor/easyeda-api/SKILL.md). Resolve exact signatures and
   return types from the bundled reference for the operation, then verify the
   installed client's behavior. Use the existing bridge, selected port and
   explicit window/document identity.
2. Read [drafting standards](12-schematic-drafting.md), select free-layout or
   framed-layout, then use this methods reference. Read the upstream recipe for
   relevant call examples; its example values and shortcuts are not acceptance criteria.
3. Apply G2-A placement review before G2-B connectivity. API success, object
   counts and upstream example screenshots cannot replace native rendering,
   independent pin-net checks, electrical analysis or PCB geometry checks.

The API layer and this methods library are both bundled operating foundations.
No second skill discovery, download, service or agent mode switch is required.
Make a task plan in the available environment; the upstream README's Plan-mode
recommendation does not block operation when that UI mode is unavailable.
For PCB-only operations, use the API and PCB references; do not load schematic
examples unnecessarily. Other EDA tools retain their own native operation path.

## Batch selection and placement: G2-A

Batch lookup by supplier code is useful, but results are candidate devices:

```javascript
const results = await eda.lib_Device.getByLcscIds(lcscIds, undefined, true);
```

Read the documented result shape. Associate each candidate with its requested
supplier code; never zip results to inputs by array position or accept the first
match silently. Resolve missing/ambiguous matches by exact MPN, value, package,
ratings, footprint and pin mapping. Preserve a selection map from designator/unit
to supplier code and chosen library/device UUID. PART-IDENTITY still requires
independently resolved part specifications.

Define usable page bounds and block rectangles before mutation. Reserve the
title block for framed-layout; free-layout uses explicit export bounds and a
compact metadata area. Size each block from the actual symbol, visible attributes,
longest labels and future local wiring. Draw graphical separators first, then
place parts inside. Upstream center-spacing and approximately 100-unit margins
are starting estimates only; they do not measure full rendered extents and must
not become PCB clearances or fixed universal symbol spacing.

Prove one dense block, including save/reopen, before repeating its pattern.
Use the documented component create and asynchronous property setter pattern;
guard undefined returns and verify the chosen UUID, designator, value, supplier
and footprint survived the edit. Avoid replacement setters with partial metadata.
Finish placement with zero native electrical wires AND buses in the scoped new
block/sheet. Save the inventory and visual/count evidence before adding external
ports, power flags or wires. Existing wired blocks retain valid connections.

## Geometry and compatibility probes

The upstream recipe uses schematic units of 10 mil, upward-increasing Y and a
rectangle specified by its top-left with height extending downward. Confirm this
on one native graphical rectangle and symbol for the current API/client before
batch drawing. Serialized and child-attribute coordinates may differ. Never fix
a mismatch by globally negating coordinates.

- Use transparent block fills only after confirming native rendering. The
  upstream uses `fillColor: "none"`; a default fill can cover circuit content.
- Reserve the heading's actual text bounds inside its block, away from pins and
  wires; a fixed 15-unit heading offset is not a legibility guarantee.
- If a documented enum is absent from the execution context, resolve the numeric
  value from that exact enum reference and probe one object. For the bundled SCH
  text-alignment enum, CENTER_TOP is 4. Do not assume all enum globals are absent
  or reuse this value for unrelated types.
- Read primitive state through documented getters where present. The bundled
  wire interface documents `getState_Line()` and `getState_Net()`; upstream `.line`
  and `.net` examples need runtime verification before use. Missing
  `getState_Coordinates()` does not mean there are no documented wire getters.
- Wire geometry may be a polyline, not just two endpoints. Preserve all vertices.
  Net state can lag asynchronous canvas refresh; verify refreshed native pin nets,
  not only a freshly assigned wire property.

Record the verified transform/signatures once per relevant client/API version and
reuse them until conditions change. Follow reference 06's protected-property probe
and reference 12's bounded repair procedure when a check fails.

## Local wiring and selective fanout: G2-B

Build a complete designator/unit/pin-to-net map from the reviewed circuit intent.
Read actual pin endpoints using `getAllPinsByPrimitiveId()` after final placement,
rotation and mirroring. For each physical/electrical pin, explicitly classify its
required connection or documented intentional NC state. Missing map entries are
unresolved design issues. Exposed pads, connector shields, internally common pins
and mechanical pads require exact-part review; never skip them simply because
the example omitted them. Verify button internal common pairs from the exact
datasheet and symbol/footprint map, not a universal numbering assumption.

Show local regulator feedback/energy paths, reset/BOOT, clock, decoupling and
protection topology with readable direct wires. Use short label/port fanout for
distant or cross-block signals and where it genuinely improves readability.
Power/ground flags must preserve domain identity. Choose signal port direction
from actual interface semantics; do not mark every signal bidirectional just
because the upstream example does. Check native label scope and accidental net
merging, especially when duplicating modules.

The upstream's 10-unit pin offset is a starting stub length only. Derive the
outward direction from verified pin semantics and the current transform; test
all orientations/mirroring used by the design. Adjust length and label location
to avoid pin numbers, symbol text, neighboring labels and block boundaries.
Use valid shared local ground branches when repeated GND labels would crowd a
dense symbol. Apply native intentional-NC markers when the datasheet permits;
omitting a wire alone is not an NC review.

Before completing G2-B, compare actual native connected pin sets with independent
intent, resolve ERC findings, and inspect every block at readable detail plus the
whole page. A successful fanout pass does not establish a completed schematic.

## Batches, partial failure and revisions

Use the bridge discovered by reference 06 with an explicit windowId. Send code
as structured JSON; for file transport write UTF-8 JSON to the task's writable
temporary directory and pass the filename instead of embedding shell-quoted
JSON. Respect the user's storage location on Windows and macOS. Do not copy the
upstream's fixed localhost port or assume /tmp exists.

Batch related operations within one bounded block to reduce transport overhead.
Do not put an entire unproven schematic into one request. Record intended object
keys and successful returned primitive IDs for components, wires, labels and
frames. Await each mutation and validate its result. A batch is not a transaction:
failure halfway through can leave valid earlier objects. On failure/timeout,
read actual state and reconcile the receipt before retrying missing operations.
Do not repeat the whole batch or promise a token/runtime saving without measurement.

For revisions, record ownership/associations before changing or deleting a
component. Remove only obsolete, unshared generated wires/labels with verified
IDs and connectivity. Coordinate proximity or a null designator may select
unrelated ports, power symbols or other component objects; neither is sufficient
authority to delete. If no association record exists, inspect candidate types,
pin nets and geometry first, preserve shared objects, and narrow the edit.
Preserve IDs for unchanged objects and avoid deleting/recreating valid work.
Read back intended changes, detect orphaned generated labels and duplicate parts,
compare affected nets, then save/reopen and review.

## Acceptance and example boundaries

The methods produce native editable EDA objects. Their acceptance remains the
G2 gates in reference 12 and the visual/geometry checks in reference 14. Counts
are diagnostics only: match the placed inventory by identity/unit and verify
electrical relationships independently. PCB pad/silk/mask clearance checks still
apply at G3/G4; schematic spacing supplies no physical clearance evidence.

The bundled ESP32-S3 example illustrates API usage. Its pin mappings, parts,
voltages, counts and circuit choices require fresh design review before reuse.
Its declared verification is upstream evidence for that example, not a PASS for
this package or a new project. Current integration validation is recorded in
VALIDATION.md; live client rendering and save/reopen must be tested separately.
