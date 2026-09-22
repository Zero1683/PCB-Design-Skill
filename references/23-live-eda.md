# Guarded live EasyEDA movement

Use `scripts/eda_live.mjs` for moving existing native **parts on an unwired schematic page** at G2-A. This is a typed Gateway writer with preflight, actual readback and compensating inverse operations. It does not intercept calls made outside this entrypoint. Keep one writer and stop manual editing during a batch.

## Scope and preparation

1. Read the bundled API skill and connect Run API Gateway. `node scripts/easyeda_bridge.mjs status` lists local bridges and windows. Read the current project/document through the official API and select the exact intended page.
2. Finish component inventory and choose one of the two required schematic formats. This writer moves existing parts; frame/title creation and visual review remain separate official API operations. It does not create parts, wire nets, route PCB tracks or restore an entire project.
3. Specify a usable rectangle excluding the title block and page margins, plus positive clearance. Coordinates use native **0.01 inch units, y-up**; do not pass millimetres. Bounds and spacing must come from the actual page design.
4. Capture immediately before planning. Capture includes component facts, local pins/attributes, native bounding boxes, fixed graphics and wire/bus counts. Missing API coverage fails closed. Standalone attributes and wired pages are unsupported. Graphic bounding boxes are conservative obstacles. Unfilled, square-corner, axis-aligned rectangles allow contained parts with border clearance; the tested native representation includes null fill style plus null fill color. Filled, rounded, rotated or incomplete shapes remain conservative obstacles; do not remove legitimate graphics merely to pass. Handle unsupported scopes with a reviewed backend operation and separate verification.

New batches require a reviewed constraint file; see [executable constraints](24-executable-constraints.md). Existing v1.6.0 journals remain historical evidence; use a fresh capture and constrained plan for new writes.

## Commands

Node.js 18+ is required. Substitute actual IDs and local files. All journal files for capture/apply must be new paths.

```sh
node scripts/eda_live.mjs capture --port 49620 --window WINDOW --project PROJECT --document PAGE --journal capture.json
node scripts/eda_live.mjs apply --port 49620 --window WINDOW --project PROJECT --document PAGE --source capture.json --moves moves.json --constraints constraints.json --journal operation.json
node scripts/eda_live.mjs status --journal operation.json
node scripts/eda_live.mjs reopen --journal operation.json
node scripts/eda_live.mjs rollback --journal operation.json
```

`moves.json` contains only existing native IDs and target anchors:

```json
{"moves":[{"id":"NATIVE_PART_ID","x":300,"y":500}],"bounds":[20,150,1150,805],"gap":10}
```

These numbers illustrate syntax, not a universal layout standard. Never translate a planner's IDs or coordinates without verifying mapping and units. `schematic_layout.py` and `layout_batch.py` remain planning/feedback tools; this writer consumes native captures, not their normalized JSON directly.

## Execution and recovery

- A full-target preview rejects stale source, unsupported mutation fields, collisions, insufficient clearance and objects outside the supplied rectangle before writing. Every ordered intermediate placement is preflighted too. A direct swap that collides is rejected before any write; use separately verified staging batches. The native calls are not an atomic EDA transaction.
- Each step checks the current native state, calls the documented `sch_PrimitiveComponent.modify`, then rereads the page and checks actual bounds, clearance and contract rules. The final capture is checked again before reporting success. Forward and inverse writes preserve every documented writable component property. Real testing found that coordinate-only calls could clear extended properties and change supplier IDs; never simplify this call to x/y only.
- `APPLIED` means in-memory native readback matched. `reopen` explicitly saves, closes and reopens the selected page; only `RELOADED_MATCH` confirms that persistence check.
- A failed batch automatically compensates only if current captured state matches a known step. Unexpected changes result in `RECOVERY_BLOCKED`, with no blind overwrite. Explicit `rollback` uses the same inverse path. If the batch was saved, restored state is saved and reread too.
- `REJECTED` means this request was stopped before mutation. `ROLLED_BACK` with an error means the attempted write failed and compensation succeeded; the CLI still exits nonzero. Do not describe that batch as applied.
- Request IDs prevent duplicate application within the same Gateway session. A replay rereads the selected document and actual state; changed state requires reconciliation. `status` is a historical operation record, not a fresh geometry validation. A local exclusive lock serializes journal updates. After transport uncertainty, run `status`; never replay an unknown write. Browser restart loses the in-memory operation registry. `NOT_FOUND` requires manual reconciliation using the journal; it does not prove that nothing was written. Do not remove a stale lock until the owning process is confirmed stopped.
- Recovery uses captured API facts, not every byte in the native project. External clients can bypass this wrapper. No guarantee is made about an arbitrary concurrent editor or unsupported primitive type. Preserve the original project backup for recovery beyond this supported batch.

## Directed repair of an invalid source

Ordinary batches require a compliant source. To repair known contract defects, add `repair` to `moves.json`:

```json
{"moves":[{"id":"PART_ID","x":300,"y":500}],"bounds":[20,150,1150,805],"gap":10,"repair":{"reason":"Place connector in its required region","allow":[{"code":"ALLOWED_REGION","id":"PART_ID"}]}}
```

Use the actual source report, IDs and measured coordinates. `allow` must enumerate all and only the existing contract violation code/ID pairs. Intermediate states may retain unchanged source violations; new or changed violations are rejected. Complete targets must pass all rules and the ordered path must remain collision-free. This scope does not waive source identity, unsupported-page restrictions, final compliance or spacing. A rollback can restore an originally defective baseline; inspect `restoredConstraintReport` before describing the design as compliant.

## Acceptance

Run `node --test scripts/test_eda_live.mjs`. For native validation, use an explicitly authorized test page: capture, reject collision and bounds violations, apply a valid move, save/reopen, rollback, then compare a new capture to the original. Record client/API scope separately from injected mock failures. Complete the normal G2-A visual and schematic checks afterward; guarded movement is not electrical acceptance.
