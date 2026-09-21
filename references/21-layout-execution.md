# Measured layout plans and native execution

Use this for a new schematic scope at G2-A. It connects measured component
geometry to a fixed placement plan, then compares actual native readbacks with
that plan. Keep the two formats and G2-A/G2-B sequence in reference 12.

## What is implemented

`scripts/schematic_layout.py` packs **already measured, locally arranged unwired
blocks** into a bounded sheet. It preserves block order, symbol scale, orientation,
and relative component positions. A shelf algorithm places blocks left-to-right,
top-to-bottom, with explicit spacing and rectangular obstacles. It produces
component anchor targets, full envelope targets, separator rectangles and title
envelopes. It does not solve local pin arrangement, wire routing, multiple pages,
or PCB placement. NO_FIT means this bounded method failed, not that no layout exists.

The script neither connects to EDA nor generates a native project. A backend
adapter must obtain native observations and apply the plan through supported
operations. Our official API remains the default; a compatible installed
easyeda-agent may provide planning/compose operations under reference 16.

## Measure before planning

1. Identify project, document, baseline and the exact new scope. Obtain the
   complete scoped component inventory and native electrical wire/bus counts.
   An existing wired sheet is not input to this unwired planner. Keep its objects
   untouched and represent their occupied areas as obstacles when adding a block.
2. Read component anchors, rotation, identity and complete pin map from EDA.
   Include value, attributes, DNP/unit and all other fields that must survive in
   `facts`. Object fields are strictly `id`, `bbox`, `anchor`, `facts`; put all other protected
   properties inside `facts`. Record explicit null for observed unassigned pins. Keep independent
   circuit intent separate; never populate actual pin maps from expected design.
3. Measure each component's full visible envelope: symbol, pins, designator,
   value and displayed attributes. `bbox` is their union, in the chosen rotation.
   If the backend omits property text, supplement measurements from native geometry
   or render evidence before planning. Do not guess widths from character counts.
4. Arrange each local circuit block around its real pins using the existing
   schematic methods. Internal overlaps are reported for local correction; the
   planner will not shuffle supporting components to force a fit.
5. Supply the usable rectangle and all protected obstacles. For framed-layout,
   exclude the title block and inner-frame margins. For free-layout, reserve a
   metadata header/footer outside the usable rectangle and define export bounds.
   Titles require measured width and a sufficient title height at the actual font.

The input contract is shown in [the source example](../assets/layout-source.example.json)
and [the layout specification](../assets/layout-spec.example.json). Example dimensions
are synthetic, not design defaults. Coordinates are `[xmin,ymin,xmax,ymax]` in
EasyEDA schematic raw units (0.01 inch), with Y increasing upward. Component
`anchor` is the native placement origin, not the bounding-box center. Keep units
explicit when adapting an upstream source. These are scoped observations, not a
replacement for the reference 10 circuit or reference 20 PCB contracts.

## Plan, apply, save, reload, compare

```sh
python scripts/schematic_layout.py plan --source measured.json --spec layout-spec.json --output placement-plan.json
# Capture the same semantic source fields again immediately before writing.
python scripts/schematic_layout.py preflight --plan placement-plan.json --source fresh.json
```

Preflight compares the entire source digest. Put timestamps, logs and capture
receipts in separate files so they do not vary a semantic snapshot. If geometry,
identity or facts changed, read back and create a new plan. Never replace the
stored digest to allow a stale write. It cannot lock out unrelated EDA edits;
retain one writer and a quiet document throughout the bounded batch.

Apply via the backend selected in reference 16:

- Select the exact document and map stable component IDs to fresh native handles.
  Resolve signatures and property semantics from the bundled
  [component API](../vendor/easyeda-api/references/classes/SCH_PrimitiveComponent.md)
  and [schematic methods](15-easyeda-schematic-methods.md). Coordinate targets
  `moves[].to` are absolute anchor positions; do not substitute bbox centers or
  apply the same displacement twice.
- Create the planned graphical separators/titles using documented primitive
  operations. Maintain a block ID to native frame/title ID map so retries read
  existing objects rather than duplicate them. Use fresh native IDs after reopen.
- Move only scoped components. Preserve full properties, library identity,
  rotation and pin facts. No wire/flag creation in this G2-A batch. If a backend
  silently rewrites properties or couples placement with wiring, use supported
  separate operations through the official path instead.
- Capture actual component envelopes/anchors/facts and actual frame/title
  envelopes. Normalize frame observations to the plan's block IDs using the
  recorded native mapping, preserving title text. Set `capture_stage` to
  `after-apply` and run the comparison below. Never construct observations by
  copying `moves[].expected` or the planned frames.
- Save through the documented [SCH_Document](../vendor/easyeda-api/references/classes/SCH_Document.md)
  operation; preserve its actual result and handle pending/failed saves.
  Only after successful save, use supported close/reopen or reload for the same
  document. Merely activating the same tab does not demonstrate persistence.
  Reacquire objects and measurements, set `capture_stage` to `after-reload`, and
  compare again. Save receipts, reload evidence and native overview/detail images
  remain separate evidence files under the same plan and baseline.

```sh
python scripts/schematic_layout.py verify --plan placement-plan.json --observed after-apply.json
python scripts/schematic_layout.py verify --plan placement-plan.json --observed after-reload.json
```

An observation has the source fields plus `capture_stage` and `frames`, with
each frame containing `id`, `title`, `bbox`, `title_bbox`. CLI exits: 0 means the
declared comparison matched, 1 means mismatch, 2 means invalid/incomplete input.
The default tolerance is 0.01 raw; use measured API precision and keep it well
below the spacing margin. Actual page bounds, frame/content margins and obstacle gaps are rechecked without
using matching tolerance to waive clearance. The tool refuses tolerance above one quarter of
padding/gap. It compares complete `facts`, component inventories, anchors and
envelopes, and all planned frames/titles. It cannot prove that the caller really
saved/reloaded, that extraction covered all native objects, or that the circuit
is electrically correct. MATCH is scoped comparison evidence only.

Complete G2-A with native wire/bus counts, inventory review and native visual
evidence. Then continue G2-B automatically within the user's authorized scope.
Do not repeat valid earlier work just because later wiring needs different checks.

## Correct once at the responsible layer

| Finding | Bounded next action |
|---|---|
| Block contents overlap | Correct local measured placement once; pack again with unchanged circuit facts |
| NO_FIT | Inspect the reported block, obstacles and page bounds; enlarge/split the sheet or revise local arrangement; do not shrink symbols/text |
| Source changed before apply | Recapture and replan; inspect changes instead of replaying stale absolute positions |
| API success but after-apply mismatch | Stop the queue, read actual properties/units/IDs and fix the adapter; preserve returned failures |
| After-apply matches, after-reload differs | Investigate save completion, document selection or persistence; do not keep rearranging the drawing |
| Repeated identical mismatch | Keep source, plan and both readbacks; change the responsible method or report the specific backend limitation |

Fix all related findings in one planned batch where possible. Record native
warning dispositions individually; neither a cosmetic warning nor a layout score
justifies ignoring missing connections or changing an electrical constraint.
Live EDA rollback is still unsupported by our file recovery tool. Reference 20
recovery applies only to complete closed-file isolated projects.

## Upstream contribution and validation boundary

The useful pattern is preserved source → computed target → supported application
→ independent native readback. This first-party helper does not copy upstream code.
At the reviewed easyeda-agent commit `caf102b3ea12a667c963b9d29484f5887751b97b`,
`internal/app/cmd_sch_layout_render.go` emits offline SVG; it is not a live writer.
Its local/whole-sheet planners and compose queue are separate steps. Confirm
installed command contracts before using them. No Caveman integration, fixed
token reduction, millisecond live rendering or complete hardware compilation is
claimed. Measure end-to-end time, actual agent token usage, retries, native
save/reload results and remaining findings on the same board before comparing
backends. Offline success alone cannot select the better production path.

## Batch preflight and repair feedback

Use [the batch/repair helper](22-batch-repair.md) before a scoped G2-A write and
when an actual readback differs. It assesses the full target and records bounded
repair attempts; it neither intercepts every native API nor executes proposals.
Keep raw capture, adapter revision and save/reload evidence with the reports.

## Native movement entrypoint

v1.6 adds [guarded live movement](23-live-eda.md) for existing parts on unwired schematic pages. It supplies actual capture, property-preserving writes, per-step readback, save/reopen checks and guarded inverse operations. The helper described above retains its own scope; arbitrary official calls and PCB routing are not globally intercepted.
