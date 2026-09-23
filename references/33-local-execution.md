# Local checks and economical context use

Use deterministic local work to reduce repeated model reads and tool round trips. Keep stability and precision ahead of speed. Do not remove a check, relax its tolerance, or shrink the exported object inventory to save context.

## Default execution pattern

1. Read the skill entrypoint and only the references needed for the current stage. Search an API method by exact name and read that class, rather than sending the full API index or export to the model.
2. Save full native exports locally once per relevant revision. Use existing `design_data.py summary/query/diff` for navigation. Request specific object IDs or changed nets; keep omitted records explicitly accessible.
3. Batch related read-only queries and supported typed operations. For schematic placement, measure envelopes and compute a complete plan locally before applying it. Retain fresh identity, intermediate collision checks, readback and save/reopen. Critical PCB nets still require their own constraints; suitable ordinary nets can use native autorouting.
4. Run offline check plans with `local_checks.py`. Reports stay on disk. Return bounded summaries first; open a failing report once, consolidate its related defects and make one repair pass. Do not rerun an unchanged failure with the same plan.
5. Reuse only exact-input offline results. Query live EDA state again before a write and before freezing a release. Never cache live DRC, unsaved native state, prices, stock or physical measurements as current facts.

## A check plan

Save this as a project-local JSON file, adapting actual file names and rules:

```json
{"schema":1,"jobs":[
  {"id":"parts","kind":"compare","inputs":["schematic.json","pcb.json"],"options":{}},
  {"id":"body-gap","kind":"geometry","inputs":["pcb.json"],"options":{"clearance_mm":0.3}},
  {"id":"pin-nets","kind":"connectivity","inputs":["pcb.json","circuit-checks.json"],"options":{}},
  {"id":"envelope","kind":"mechanical","inputs":[],"options":{"baseline":"RevA"}},
  {"id":"release-records","kind":"gates","inputs":[],"options":{"baseline":"RevA","through":"G5"}}
]}
```

The 0.3 mm value is syntax illustration, not a universal clearance. Supported kinds also include `electrical` with one calculation file and no options, and `intake` with no input files and a baseline option. `geometry`, `compare` and `connectivity` consume their existing normalized schemas; the runner is not an exporter. No arbitrary commands, shell snippets or EDA write jobs are accepted.

```sh
python scripts/local_checks.py --root /project --plan checks-plan.json
python scripts/local_checks.py --root /project --plan checks-plan.json --force
```

The runner stores reports and cache records in `.pcb-local/`. It hashes the job parameters, input bytes, local checker code and Python version; root-based checkers conservatively hash the full project outside `.pcb-local/` to include referenced evidence. Vendor parser changes invalidate results too. Unrelated project changes can therefore rerun root-based jobs; this favors correctness over fine-grained cache hit rates. A changed or corrupted report is recomputed. Input/code changes during a job invalidate its result. Failed checks can be reused only when their exact inputs remain unchanged; tool errors/timeouts cannot establish coverage.

Default output includes up to eight job summaries and aggregate counts; `--offset` and `--limit` page that view. The complete summary is `.pcb-local/latest.json`, and individual reports retain their original checker output. JSON output is capped at 8,192 bytes. `CHECK_OK` describes that checker scope only; `CALCULATED` never means electrical acceptance. The runner does not write PASS into project gate records. Continue normal evidence binding and review. Cache hashes do not authenticate externally edited reports against an adversary.

Keep one runner per project. A stale lock requires checking that its recorded process has stopped before removal. Use `--force` for release revalidation or to deliberately rerun after diagnosis. Interrupted jobs are not proof of completed checks.

An execution-time read or validation error is reported per job; independent jobs
continue and the batch still exits unsuccessfully. Read that job's `stderr` or
report, fix the named input, and rerun. Invalid plans are rejected before execution.
Unreadable directories block dependency capture rather than being silently skipped.

## Measure savings honestly

Record full report bytes versus returned summary bytes, checker executions versus cache hits, and the current stage. Byte savings and cache hits are not model-token measurements. A complete new-session benchmark must measure actual tool calls, context and time before claiming an end-to-end quota reduction. Do not promise a percentage from a synthetic board fixture.

Project JSON inputs must not directly or indirectly reference `.pcb-local` files. The runner rejects such references before cache lookup because that directory is excluded from the project fingerprint. Keep input exports and evidence in separate project directories.

For source-bound PCBA/state/variant/port/release reviews use job kind
`project-reviews`, inputs `["project-reviews.json"]`, and options
`{"baseline":"RevB"}`. See [review schemas and limits](36-project-reviews.md).
The root and every indirect source remain covered by conservative cache hashing.
