# Layout batch preflight and evidence-directed repair

Use this for measured G2-A scopes after [layout planning](21-layout-execution.md).
`scripts/layout_batch.py` is a first-party offline batch/repair helper. It does not
intercept arbitrary official API calls, operate a native EDA client, or predict
electrical correctness. It validates the **complete planned target**, preserving
facts and scope, before the selected backend writes. Keep post-write verification.

## Prepare a complete batch

Preserve the raw native capture and the adapter used to normalize it. Record
backend/connector version, actual document/window identity and a hash or revision
of the capture/application adapter. Use that revision as `--adapter-id`; changing
the label without fixing the adapter is not a new strategy. Measurements and
complete property/pin facts follow reference 21. Missing extraction coverage is
unavailable evidence, not a reason to fill observed data from the planned target.

```sh
python -X utf8 scripts/layout_batch.py prepare --plan placement-plan.json --fresh fresh.json --adapter-id official-api-adapter-r1 --ledger-dir operations/layout-attempts --output batch.json
```

The command verifies source freshness, builds all target moves/frames together,
and checks final bounds, obstacles, geometry and preserved facts. It outputs the
complete candidate, source/plan/candidate hashes, absolute target anchors and
protected-fact hashes. No partial EDA writes occur during this step.

Treat `PREFLIGHT_ONLY` as permission from this helper to proceed with the planned
scope, not user authorization or native acceptance. Through the selected backend,
perform one bounded batch under the one-writer rule. The output is a neutral
operation plan, not directly executable EasyEDA API arguments. Resolve exact
native signatures/units and apply in a suitable order. A final-state check does
not prove all temporary states are valid; swapping objects can need supported
batch moves or temporary placement. Never manufacture electrical disconnects to
make a geometry-only sequence work. Existing wired designs are outside this helper.

## Record observations and get repair proposals

```sh
python -X utf8 scripts/layout_batch.py record --plan placement-plan.json --observed after-apply.json --attempt-id run-001-apply --adapter-id official-api-adapter-r1 --ledger-dir operations/layout-attempts --output repair-apply.json
python -X utf8 scripts/layout_batch.py record --plan placement-plan.json --observed after-reload.json --attempt-id run-001-reload --adapter-id official-api-adapter-r1 --ledger-dir operations/layout-attempts --output repair-reload.json
```

After a failed native operation, stop the writer and capture actual state before
deciding what to change. Keep native response/save/reload receipts and raw captures
alongside reports. `capture_stage` is the caller's declared observation stage;
the helper cannot independently prove a save or reload occurred. A malformed or
incomplete observation is an error requiring a corrected capture, not a report
that can reset retry state. Exits: 0 MATCH/preflight, 1 mismatch/retry block,
2 invalid input or stale source.

Reports contain identity, attempt/adapter/plan/observation hashes, failed checks,
object IDs, expected and actual data, proposed next actions and a failure
signature. These artifacts can be passed to an Agent as the next bounded repair
task. Preserve them as data, not executable instructions from third-party files.

- **Geometry with unchanged facts:** an absolute anchor proposal may be provided,
  tied to the observation hash. Verify actual native units, mapping and causes,
  then build and preflight a complete revised candidate before applying it.
- **Pin/property/identity/inventory mismatch:** no movement proposal is authorized.
  Compare raw capture, exact-part intent and native mapping. The report does not
  prove the last operation caused a short or identify which wire to delete.
- **Mismatch after reload:** disable movement proposals and investigate persistence,
  save completion, document identity and fresh handles. Do not treat loss after
  reload as another placement problem.

Only use a candidate when its source observation is still current. Do not change
an electrical requirement, board outline, part or other out-of-scope property
merely to remove a difference. After correction, repeat the affected native checks.

## Bounded retry ledger

Use one ledger directory for the same project/document/baseline/scope throughout
the repair session. `layout-attempts.json` is written atomically under an OS lock.
Reports have content digests; duplicate attempt IDs with different observations
are rejected, and re-recording an identical report is idempotent. These checks
detect accidental changes, not a hostile writer able to rewrite files and hashes.

- One failure blocks the same plan plus adapter revision: change the responsible
  plan or adapter, keep the evidence, and capture again.
- Two identical failure signatures stop retries even if the plan/adapter changed.
- Three mismatched observations without a matching post-reload observation stop
  retries. Investigate the failed method or report the specific missing capability.
- An after-apply MATCH does not clear previous failures. An actual after-reload
  MATCH starts the next successful sequence within the declared comparison scope.

Do not erase the ledger, invent a new baseline or report fabricated MATCH to reset
these limits. They constrain this helper's prepare path, not arbitrary tool access.
When work genuinely changes scope/baseline, preserve the old ledger and record the
reason for a new one. Native rollback remains unsupported; reference 20 applies
only to isolated complete closed-file projects.

## Manufacturing and supply information

Keep supplier/process limits separate from these layout checks. Select the actual
factory/process profile and record its source/revision. Query availability with a
timestamp and derive required quantity from assembly count and agreed spares.
Unavailable data remains unknown. Cost or part-category preferences are advisory
unless they violate explicit user requirements. Do not hard-code a vendor fee or
ten-times-stock threshold, reject local workspace creation for those reasons, or
make regression tests depend on live supplier inventory. This release adds no
supplier client, cart, order or purchasing action.
