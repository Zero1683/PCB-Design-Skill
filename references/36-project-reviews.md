# Sourced project reviews: states, variants, porting and PCBA

Read only for applicable work. These methods adapt ideas reviewed in
[Keitark/pcba-design-skills](https://github.com/Keitark/pcba-design-skills/tree/d41e9996f052016727403236cf0f7476f8f23a1b).
Our implementation is original; no additional vendor runtime or orchestration
system is installed. Keep the existing design stages and two schematic formats.

## What changes in the workflow

- **Requirements:** record prohibited behavior and applicable operating modes in
  the existing functional brief. Derive engineering details; do not give novices
  another questionnaire or reopen previously delegated choices.
- **Circuit:** review startup, reset, programming, operation, sleep, fault and
  partial-power modes when applicable. Record active driver ownership, enable
  polarity, rails, safe defaults and unpowered inputs. Static net connectivity
  cannot establish transient sequencing. Use local wires inside functional
  blocks; keep cross-page/long-distance labels where they aid readability.
- **Generated variants:** record the selected configuration, effective parameters,
  generator digest and output roles. Read an actual output marker/export to prove
  the chosen variant was used. Do not use the desired configuration as readback.
- **Derivative boards:** freeze donor inputs; list electrical and mechanical deltas
  before placement. Protect mating datum, contact geometry, insertion envelope,
  fixed parts, keepouts and unaffected routes. Reuse functional relationships,
  not blindly cropped/scaled coordinates. Compare donor/target at the same
  physical orthographic scale. A plausible 3D image is not a fit test.
- **Assembly:** separately compare fitted PCB references, BOM, submitted placement
  and supplier-imported placement. Source normalization must document origin,
  units, angle and bottom-side transforms. Never guess package corrections.
- **Release:** select file roles for the requested deliverable. Bare PCB release
  does not require CPL. PCBA requires BOM, placement data, assembly drawings and
  relevant evidence. Resolve changes in source, regenerate and recheck.

Map applicable reviews into existing requirements/acceptance records. The script
does not infer applicability, parse proprietary source files, or supply missing
observations. Do not claim coverage of a feature without its actual export and
review. If unavailable, record the specific missing evidence.

## Local input and execution contract

`scripts/project_reviews.py` checks normalized observations against independently
reviewed expectations. Use project-relative nonempty files with SHA-256 bindings.
All plan, contract, observation, supporting evidence and release artifacts must
be listed in the current `design-baseline.json` inputs. Generate the plan first,
then freeze the baseline; avoid circular references. Preserve raw source exports
and the adapter/version/conversion record as supporting evidence.

```json
{
  "schema": 1,
  "project_id": "actual-native-project-id",
  "baseline_id": "RevB",
  "reviews": [{
    "id": "startup-states",
    "kind": "states",
    "contract": {"path": "reviews/states-expected.json", "sha256": "actual-hash"},
    "observation": {"path": "reviews/states-observed.json", "sha256": "actual-hash"},
    "evidence": [{"path": "exports/native-source.json", "sha256": "actual-hash"}]
  }]
}
```

These hash labels are documentation placeholders, never runnable proof. Compute
real hashes with `workflow_io.file_hash`. The expectation and observation must
be different files; that restriction and hashes establish integrity, not their
independence or authenticity. Do not fabricate a source export or user decision.

```sh
python scripts/project_reviews.py --root /project --plan project-reviews.json --baseline RevB
```

Exit 0 is scoped `CHECK_OK`, 1 is `BLOCKED`, 2 is invalid/missing/stale evidence.
Results name affected references/modes/objects; keep full reports on disk. Run
through `local_checks.py` with job `kind: "project-reviews"`,
`inputs: ["project-reviews.json"]`, `options: {"baseline": "RevB"}` for bounded
summaries and exact-input reuse. Root dependencies remain conservatively hashed;
fine-grained dependency invalidation is not implemented by this update.

G5 design checks rerun a present `project-reviews.json`; any failed review blocks
that check. Missing optional plans are not synthesized by the checker. The agent
must declare applicability and attach these reviews to the project's requirement
coverage. Deleting a frozen input makes baseline verification fail; do not refreeze
a baseline merely to remove required evidence.

## Supported review data

Every object below uses exact field names; unknown fields are rejected at the
document/row boundaries. Use native identifiers, normalized units and consistent
JSON types. `1`, `1.0` and `true` are not interchangeable in generic config diffs.

### assembly

Contract: `coordinate_frame` is
`{units:"mm", origin:"documented datum", axes:"X-right/Y-down", angle_view:"assembly-side", rotation:"clockwise", bottom:"normalized"}`;
use a real nonempty origin description and keep the raw conversion record.
Other fields:
`position_tolerance_mm` (>0, <=0.10), `angle_tolerance_deg` (>0, <=1), and
`components` with one row per board reference:
`{ref, fitted: boolean, part, x_mm, y_mm, side, rotation_deg}`.
Angles are normalized to [0,360), side is `Top`/`Bottom`, positions are mm.

Observation: same `coordinate_frame`; `bom` rows `{ref, part}`;
`submitted` and `imported` rows `{ref, part, x_mm, y_mm, side, rotation_deg}`;
`manual_browser_edits` boolean. `part` is the exact selected supplier/MPN identity
in the same identifier system across all four datasets. Aggregate BOM rows are
expanded by reference. DNP references remain in the board contract and must not
occur in assembled tables. Missing, extra, repeated or substituted rows block.
Coordinates must already represent the same physical pose after evidenced
package-specific mapping; this checker never silently translates/rotates a board.

The checker uses Euclidean position difference and wrapped angle difference.
It does not inspect pad polygons, paste overlap or supplier 3D images. It cannot
prove the imported table is freshly captured. Fresh web observations remain
mandatory before assembly approval, regardless of cached offline consistency.

For each assembled side inspect at least three separated non-collinear anchors
when the design has enough suitable parts; otherwise document the reduced
calibration coverage and do not claim full calibration. Include asymmetric pin-1
geometry and package exceptions. Inspect every placed body and critical terminals,
tabs, polarity, connector mouth, antenna and support features. Bind screenshots,
supplier project/upload identity, final CPL hash and unresolved rows separately.
Correct source mapping, regenerate, re-upload and repeat review after browser
edits. Do not launch an ordering flow for ordinary PCB design delivery.

### states

Contract: `modes: [{name, signals: {signal: value}}]`,
`exclusive_groups: [[signalA, signalB, ...]]`.
Observation: `modes` in the same format. Allowed values are strings
`"0"`, `"1"`, `"Z"`, `"off"`, `"on"`; unknown data is not a safe state.
Every expected mode and signal must be covered exactly. Group signals represent
normalized active-driver indicators (`"1"`/`"on"` = driving), after documented
active-low polarity conversion. Each group permits at most one active member in
every declared mode; it is not suitable for intentionally shared open-drain buses.

This catches declared state mismatches and conflicting driver enables, including
an internally conflicting expectation. It does not derive states from firmware,
solve analog conduction, prove break-before-make timing or validate omitted modes.
Record the datasheet/truth-table/measurement basis independently.

### variant

Contract and observation: `{variant_id, generator_sha256, parameters, output_roles}`.
Parameters are a nonempty JSON object; output_roles is a unique nonempty list.
The actual generator file must be bound in `evidence` with the declared digest.
Extract observed configuration/marker from the actual generation run/output;
record output artifact integrity separately with `release`. Comparing declared
roles does not parse generated source or prove a marker was truthful.

### port

Contract: `donor` is a nonempty object map keyed by stable native identity;
`allowed_changes` is a list of `{object, before, after, reason}`.
Observation: `target` is the corresponding complete scoped object map. Include
all protected objects and electrical/mechanical fields relevant to the migration,
not only the changed components. Record extraction coverage in supporting evidence.

Every allowed change must match the donor and expected target exactly; unused
allowances and any other change block. Use null only to mean object absence in
an add/remove allowance; object maps cannot contain null entries. Normalize units
and number types before comparison. This is a scoped data diff, not a PCB geometric
or routing solver; rerun native connectivity, geometry and manufacturing checks.

### release

Contract: `{revision, roles: [role, ...]}` with exact required role set for this
delivery. Observation: `artifacts: [{role, revision, file: {path, sha256}}]`.
Missing/extra/duplicate roles, mixed revisions or stale files block. Every actual
file must be a bound current-baseline input. File roles and revision fields are
declared metadata; they do not replace parsing Gerber, BOM or PCB semantics.

## Related methods without extra runtimes

- Source substitutes by exact part/package/pin semantics and required behavior;
  add lifecycle, CAD and 3D status when relevant. Missing optional cosmetic 3D
  models must not block unrelated electrical work. Keep approved authorizations.
- For connectors distinguish deliberate body/mouth overhang from unsupported
  solder pads/anchors. Record electrical mapping, orderable part, footprint,
  mating system and physical-fit evidence separately.
- For stencil work check actual production panel, paste layer, assembly side,
  fixture working area and aperture/process requirements. Do not copy a universal
  thickness or create unrelated artwork to set an order's outer dimensions.
- Extend the existing retry ledger with actual before/after metrics and changed
  conditions. Compare against the best safe candidate, preserve hard constraints,
  and diagnose fixed/movable route scopes before repeating a failed router job.
- Separate price refresh from part identity changes conceptually. Keep conservative
  cache invalidation until an explicit dependency implementation has been tested.
- For requested demonstrations preserve source-bound stage snapshots and public
  vs private evidence. Default to lightweight logs, not continual screenshots.
  Hash chains prove consistency, not authenticity; text scanning does not inspect
  all private information in images. Project lessons do not rewrite installed skills.

No external case-study pictures, fixed board parameters or additional licensed
assets are bundled. These responsibilities stay within the existing
G0–G9 workflow rather than adding another manager.
