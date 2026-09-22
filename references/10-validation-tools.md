# Validation tools and data contracts

For native PCB extraction and independent geometry/manufacturing checks, use
[the bundled inspection toolkit](18-pcb-inspection-toolkit.md). Preserve actual
input coverage and baseline; its board model is distinct from our normalized
component snapshots. The existing gates in this reference still apply.

These tools analyze explicit inputs and records. They do not parse arbitrary EasyEDA files, run a field solver, or replace EDA connectivity and DRC. Do not label helper output as complete board approval.

## Check records

```sh
python scripts/check_evidence.py --root /path/to/project --baseline revA --through G5 --design-gates
```

`--through G5` checks design/manufacturing records without demanding a physical board. For hardware work select the relevant stage and supply `--board <id>` and `--firmware <id>` when applicable. Exit 0 means selected records are complete; 1 means unresolved/invalid records; 2 means invalid input. The tool does not modify statuses.

PASS needs method, conditions, acceptance criteria, actual result, baseline, timezone-qualified timestamp and a nonempty local evidence file. Use semicolon-separated project-relative evidence paths. Keep linked files inside the project; save an external measurement/export locally with provenance. N_A requires justification. ACCEPTED_LIMITATION requires a reason/source and decision-record file and remains separate from passing verification. Checks with `assess` applicability must be resolved to an applicable result or justified N_A; they are not silently skipped.

Baseline mismatches require review; the tool cannot infer which design changes invalidate which results. For unaffected evidence, record a reviewed carry-forward justification rather than changing the baseline label without review. The design-gates mode now enforces the skill-owned registry, current design/source hashes and bound observations. It detects deleted registered checks; project-specific omissions still require requirement review. Read [current-design evidence](27-current-design-evidence.md) for binding and carry-forward. Without --design-gates, the command only lints supplied records.

Split outcomes that can differ. LED, button, sensor identity/data, interrupt, and sleep tests must have separate rows when relevant. Existing projects migrate by adding new rows; retain old evidence and explain replaced aggregate rows.

For schematic drafting, retain separate G2-A placement and G2-B wiring evidence as described in [reference 12](12-schematic-drafting.md). SCH-UNWIRED is mandatory for new schematics and new blocks; `assess` allows a documented applicability decision for an existing wired design. A final wired drawing does not invalidate an authentic earlier zero-wire snapshot. This checker validates records, not native wire counts or the chronological execution of the stages.

## Normalized design exports

Build these records from actual native API/netlist/BOM exports using version-specific mappings, recording the source and coverage. Retain the raw export and the extraction code. Never reconstruct missing nets from screenshots or declare coverage complete when parsing failed. `coverage: complete` is an extraction assertion requiring review, not something the helper independently proves.

Each snapshot uses:

```json
{
  "schema": 1,
  "kind": "pcb",
  "baseline_id": "revA",
  "source": "exports/pcb-raw.json; documented extractor/version",
  "coverage": "complete",
  "components": [{
    "ref": "R1", "part": "exact manufacturer part", "value": "10k",
    "footprint": "verified footprint ID", "fitted": true, "in_bom": true,
    "pins": {"1": "3V3", "2": "EN"},
    "side": "top", "body_aabb_mm": [1, 2, 3, 4],
    "geometry_source": "manufacturer body outline transformed to PCB coordinates"
  }]
}
```

- `kind` is schematic, pcb or bom. Expand grouped BOM references into one component per reference; compare exact normalized strings. Preserve DNP as `fitted: false`, and exclusions as `in_bom: false`. A fitted-only purchasing list is not a complete design BOM.
- `pins` maps electrical pin numbers to net names. Use null only for documented NC pins; unavailable data is an incomplete export. Multiple physical pads sharing a number collapse electrically only after verifying they share a net. Retain all physical instances in the raw export.
- Different documents must share the same baseline. Compare `schematic → pcb` and `schematic → bom`; the latter compares component properties rather than pin nets. Empty exports and partial coverage are rejected.
- For body screening, provide transformed **board-coordinate** axis-aligned bounds in millimetres after rotation/mirroring. Missing body geometry stays unchecked. Opposite sides are not compared; connectors, through-hole leads, board edges, pad clearance, height and mating space still require separate review.

```sh
python scripts/audit_design.py compare schematic.json pcb.json
python scripts/audit_design.py compare schematic.json bom.json
python scripts/audit_design.py geometry pcb.json --clearance-mm 0.5
```

The clearance above is an example, not a default manufacturing requirement. Exit 1 reports mismatches or suspect/missing geometry; exit 2 reports invalid input. No suspects is not mechanical acceptance: rotated AABBs overestimate bodies, and the helper does not inspect copper. Confirm each suspect against exact outlines and actual EDA views.

## Connection intent and revision checks

Use [circuit intent and reuse](13-circuit-intent-and-reuse.md) to check independently specified pin relationships with `check_connectivity.py` and review normalized component/pin changes with `audit_design.py diff`. These use the snapshot schema above. `compare` still requires one shared baseline across documents; `diff` requires distinct baselines of the same document kind. Preserve native exports and extraction provenance for both.

## Change reports and manufacturing checks

For authorized edits, retain before/after native snapshots and export diffs. Compare reference, part, pin-net, position/rotation/side, rules, trace/via/pour geometry, and affected manufacturing files using actual format support. The normalized tools compare component properties and pin nets within or across baselines. They do not compare native geometry, routing, pours, or rules. Never claim unchanged routing from matching component records alone.

Use the release-manifest tool only on reviewed frozen deliverables. Gerber/drill/stencil/BOM/placement consistency and rendered previews remain separate engineering tasks. Run the helpers on derived records; do not use them to rewrite the source project automatically.

## Drawing and physical-object screening

`scripts/screen_visual_geometry.py` checks supplied transformed object bounds for page/title-block intrusion and pad/silk/mask spacing. Read [the schema and acceptance procedure](14-visual-geometry-gates.md). It does not parse native EDA files, establish export coverage, or replace rendered review and exact-contour checks. The older `audit_design.py geometry` command remains a body-only screen.

## Reconciled PCB data and bounded queries

[Reference 20](20-data-and-recovery.md) documents `design_data.py`: explicit observed
snapshot/board binding, component/pin reconciliation, preserved contract export,
summary, pagination and section deltas. Existing comparison/connectivity tools
consume its normalized export; toolkit tools consume its board export. No schema
is silently renamed. The accompanying operation state helper is file-only.

## Measured G2-A layout

`scripts/schematic_layout.py` provides `plan`, `preflight`, and `verify` for measured
unwired scopes. See [the contract and commands](21-layout-execution.md). MATCH
covers declared geometry and protected facts only; native save/reload receipts,
rendered checks and G2 stage acceptance remain separate.

## Batch preflight and repair feedback

Use [the batch/repair helper](22-batch-repair.md) before a scoped G2-A write and
when an actual readback differs. It assesses the full target and records bounded
repair attempts; it neither intercepts every native API nor executes proposals.
Keep raw capture, adapter revision and save/reload evidence with the reports.
