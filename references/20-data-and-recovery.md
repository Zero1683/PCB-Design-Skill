# Reconciled data, bounded queries and operation recovery

Use these helpers when combining actual native PCB exports with normalized records,
reading large datasets, or editing a complete closed-file native project copy.
The helpers use Python 3.10+ and its standard library. They do not connect to EDA,
generate a complete circuit, run an autorouter or replace native acceptance.

## Reconcile the two observed models

`design_data.py` joins an observed normalized **PCB** snapshot to the toolkit board
model. It preserves both complete inputs and adds native component IDs, per-pin
reconciliation, a baseline binding and a content digest. It does not fill missing
part metadata from guesses or use planned wiring as observed data.

1. Export the selected PCB using the documented backend. Record project/document
   identity, baseline and actual native readback evidence. Generate the toolkit
   model using the current importer, which now preserves `native_id` for components.
   Earlier exports lacking this field must be regenerated, not assigned invented IDs.
2. Obtain the complete normalized PCB snapshot from actual readback using reference 10.
   Keep requirements/connection expectations independent; reference 13 still governs
   intent checks. A schematic snapshot is not a substitute for observed PCB data.
3. Start from [binding fields](../assets/data-binding.example.json). Compute input
   digests with `hash` below. Bind the exact project, document and baseline; record
   a reviewed per-reference mapping between normalized footprint names and toolkit
   footprint IDs. Generate repeated mapping rows with local code, not conversation.
4. Missing PAD_NET does not imply NC. If native readback proves a physical pin is
   unassigned, list `[reference, pin]` in `unconnected_pins` and retain that evidence.
   The normalized snapshot must also contain explicit null. Connected NC declarations,
   unresolved pads, absent pins and conflicting repeated-number lands are rejected.
5. Build and save the reconciled file. Component sets, footprint bindings, actual pin
   maps and import component counts must agree. Number and element PAD_NET entries
   must agree. Unknown physical pad entries and incomplete export coverage fail.

```sh
python scripts/design_data.py hash /project/checks/pcb-normalized.json
python scripts/design_data.py hash /project/checks/board.json
python scripts/design_data.py build --snapshot /project/checks/pcb-normalized.json --board /project/checks/board.json --binding /project/checks/binding.json --output /project/checks/design-data.json
```

JSON digests use sorted keys and compact UTF-8 serialization, not source file bytes.
They detect input changes; they do not verify that the declared source is truthful.
Native archive hashes, extraction coverage and native checks remain independent.
The reconciled file is an inspection interface, not a restorable native project.
Unnumbered mechanical copper and formats outside the adapter's supported subset
require native review/adaptation; do not fabricate electrical pin numbers to pass.

Export the preserved contracts for existing tools:

```sh
python scripts/design_data.py export /project/checks/design-data.json --format normalized --output /project/checks/observed-pcb.json
python scripts/check_connectivity.py /project/checks/observed-pcb.json /project/checks/independent-intent.json
python scripts/design_data.py export /project/checks/design-data.json --format board --output /project/checks/observed-board.json
python scripts/pcb_toolkit.py courtyard /project/checks/observed-board.json
```

Outputs are created exclusively; choose a new filename instead of overwriting a
reviewed artifact. Stored raw sections, visual attributes, rules and geometry survive
the round trip. Successful reconciliation does not certify their geometry or routing.

## Read only what the next decision needs

```sh
python scripts/design_data.py summary /project/checks/design-data.json
python scripts/design_data.py query /project/checks/design-data.json --ref U1 --limit 1
python scripts/design_data.py query /project/checks/design-data.json --net USB_DP --section tracks --limit 25
python scripts/design_data.py query /project/checks/design-data.json --section footprints --offset 25 --limit 25
python scripts/design_data.py diff /project/checks/before.json /project/checks/after.json --limit 25
```

Use summary first. Detailed query sections are components, tracks, vias, pours,
footprints, rules, layers and outline. Component queries support exact reference and
net filters; routed objects support exact net filtering. Pages contain at most 100
records, a total and a next offset. Retain the digest while fetching subsequent pages;
if it changes, restart the query on the intended snapshot. Page limits are record
limits, not hard token limits: a large footprint can itself contain many primitives.

Diffs use the same project/document identity. They return changed references and
changed board sections with hashes, rather than dumping old/new geometry. Fetch the
relevant section only when needed. Section-level changes are deliberately coarser
than a native object diff. Preserve full raw files on disk for exact examination.
These helpers reduce repeated context transfer without filtering away visual evidence
needed for schematic text, silkscreen, mask or placement checks. No fixed percentage
of token savings or large-board performance guarantee is claimed.

## Isolated closed-file operation state machine

`operation_state.py` works on a **separate candidate directory**. It never replaces
the original project. For live EDA editing, continue reference 06's one-writer,
native checkpoint/readback procedure; do not call this file tool against an open
client's working directory. A healthy bridge does not prove native restore capability.

The source bundle must contain the native project, all required local dependencies
and hashed evidence that it reopens in the intended client. Close the client and stop
writers before copying. A cloud-only project or unresolved external library is not
a complete closed-file bundle. The completeness flags in the plan are caller
declarations supported by evidence; the helper cannot validate native file semantics.

```text
PREPARED -> APPLYING -> VERIFYING -> ACCEPTED
                 |          |
                 +--------> FAILED -> RECOVERING -> RECOVERED
```

Prepare [the operation plan](../assets/operation-plan.example.json) with project,
document, baseline, current phase, actual native files, reopen evidence and required
check IDs **before editing**. Use applicable existing gate IDs; G2-A still requires
the unwired check. A later stage may require different checks. Scope each operation
to one bounded batch; accepted earlier checks are not automatically invalidated by
ordinary incompleteness in a new batch.

```sh
python scripts/operation_state.py begin --source /project/closed-native-bundle --plan /project/operation-plan.json --output /project/operations/batch-001
python scripts/operation_state.py start /project/operations/batch-001
# Run supported file operations ONLY in batch-001/candidate; then stop the writer.
python scripts/operation_state.py hash /project/operations/batch-001/candidate
python scripts/operation_state.py capture /project/operations/batch-001 --expected-digest <returned-digest> --writer-stopped
# Perform the planned checks on this frozen candidate and save actual evidence.
python scripts/operation_state.py decide /project/operations/batch-001 --report /project/check-results/report.json
```

Report fields: `project_id`, `document_id`, `baseline_id`, `phase`,
`candidate_digest`, and `checks`. Each check contains `id`, `status`
(`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`) and a nonempty `evidence` list of
`{ "path": "relative-file", "sha256": "actual-file-hash" }`.
Evidence must be inside the report directory; it is copied into the transaction.
All planned required checks must appear and pass for ACCEPTED. Any explicit FAIL
prevents acceptance. Reported status remains caller evidence, not independent
electrical approval. Missing required native files also prevent acceptance.

If a writer fails or times out, stop it and observe current candidate files before
recording the failure. Do not blindly retry an uncertain operation:

```sh
python scripts/operation_state.py hash /project/operations/batch-001/candidate
python scripts/operation_state.py fail /project/operations/batch-001 --expected-digest <returned-digest> --reason "specific failed operation" --writer-stopped
python scripts/operation_state.py recover /project/operations/batch-001 --writer-stopped
python scripts/operation_state.py status /project/operations/batch-001
```

Recovery verifies the full checkpoint and unchanged original source, and matches the
candidate to the recorded failed version. It preserves the failed directory and
restores only the isolated candidate. If recovery is interrupted between directory
renames, rerun recover; RECOVERING records identify the remaining step. OS file locks
are released when the helper process exits. These locks coordinate helper instances,
not unrelated EDA/file writers; stopping those writers is still required.

Unexpected source/candidate edits, links, checkpoint damage, changed plans and stale
reports cause refusal without replacing the original. Interrupted initial copying
leaves an incomplete transaction without an executable state; inspect it and create
a new transaction directory. Do not delete user changes or rewrite hashes to force
recovery. Reopen the recovered native project and repeat affected native checks
before use. RECOVERED means matching checkpoint file bytes, not restored live UI or
revalidated electrical behavior.

ACCEPTED yields a candidate for explicit native handoff; it does not automatically
install it into the user's source tree. After recovery, change the failed strategy
and start a new scoped operation. This is resumable workflow orchestration around
existing tools, not an atomic transaction across arbitrary EasyEDA API calls.

Status queries recheck frozen candidate files, the original source, the checkpoint,
and archived evidence. Drift returns `STALE` with the historical `recorded_state`;
an earlier ACCEPTED result does not validate changed files. Archived reports use
paths that resolve within their evidence bundle, and retain the original report.
Repeated physical pads with the same logical pin number require a network entry
for each pad element; a numeric pin mapping cannot fill missing observations.
