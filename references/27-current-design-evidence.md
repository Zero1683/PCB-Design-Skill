# Current-design evidence and complete stage checks

Load at stage acceptance, source revision, recovery, or before manufacturing export. This applies to project records, not a request for another user approval.

## Required checks cannot disappear

Use `check_evidence.py --design-gates` for stage acceptance. Without this flag, the command only lints supplied rows and must not be presented as G5 approval.

`assets/design-check-registry.json` is the skill-owned minimum registry, independent of a project's editable CSV. Every registered item through the selected stage must exist with its original stage and applicability. Required items must PASS. Assessed items may be PASS or N_A with a scoped, sourced decision. Deleting a failed DRC row, shifting its stage, or relabeling it optional does not clear the gate. Add project-specific checks from requirements; the registry cannot discover an omitted requirement.

Keep G2-A and G2-B separate. `--through G2` checks completion of both, so do not run that final stage gate to demand wires during G2-A. Review the unwired placement snapshot first; only run the full G2 gate after wiring and electrical review. Never delete final wires to recreate a historical zero-wire result.

## Bind the saved design

At a reviewed candidate snapshot, save the native project and capture its actual document IDs. Preserve the native source files, extraction inputs, design rules, requirements and other acceptance-critical files. Cloud exports are snapshots, not proof that an open unsaved canvas is unchanged. Read back/save/reopen as supported before acceptance.

Create a new manifest from actual local files:

```sh
python scripts/evidence_binding.py --root /project --project actual-project-id --baseline RevA --document actual-document-id --input native/project.epro --input exports/pcb.json --input requirements.json --input constraints.json
```

Repeat `--document` and `--input` as needed. Only name files that actually exist; the example extensions do not imply a supported import/export operation. Include every design source involved in the accepted scope; a single extracted JSON is insufficient if authoritative native files are available. Never bind only a screenshot or a checker output as the design source.

The command creates `design-baseline.json` exclusively:

- `schema: 1`, `project_id`, `baseline_id`, unique nonempty `document_ids`.
- `inputs`: nonempty file references `{path, sha256}`. Paths are project-relative; links and junctions are rejected.

Hashes cover exact bytes. Object digests use `workflow_io.digest()` (canonical sorted compact UTF-8 JSON). Generate them using the helper, not manually. The manifest does not include itself, `check-bindings.json`, CHECKS.csv, or mutable report outputs, avoiding a circular digest.

## Bind each acceptance observation

`check-bindings.json` contains `schema: 1`, matching `project_id` and `baseline_id`, and `checks`. Each record has:

| Field | Meaning |
|---|---|
| `id`, `status` | Exact CHECKS.csv ID and PASS or N_A outcome |
| `design_digest` | Digest of the current parsed design-baseline.json |
| `checked_at`, `method` | Actual timezone-qualified observation time and procedure |
| `inputs` | Hashed local inputs used for this observation |
| `evidence` | Hashed report/decision files; paths must exactly match the CSV evidence list |
| `mode` | `manual` or `machine` |

Manual review additionally requires `reviewer`, `finding`, and `basis`. The reviewer may be the Agent; do not label it human review unless a person actually reviewed it. Record what was inspected, criteria applied, actual result and unresolved limits. A core registered gate requires this composite assessment because the existing narrow helpers cannot independently prove an entire electrical, geometry, or manufacturing gate.

Machine records use subordinate IDs (for example `USB-PIN-NETS`) and additionally contain `report: {output: {path, sha256}, tool: {name, sha256}}`. The tool digest covers the maintained helper bundle via `evidence_binding.tool_digest(name)`. Supported reports are connectivity, normalized comparison, body geometry, component quote arithmetic, and exported geometry constraints. A failing output cannot support PASS. Partial helper PASS does not replace a core stage gate.

Machine report import and recorded execution use the same identity checks. Every
supported CLI now embeds `source_inputs`, an ordered list of `{role, sha256}`
computed from the exact bytes parsed. A report must carry the current `baseline_id`;
all reported input hashes must match the observation's bound inputs. Primary design
inputs must also belong to `design-baseline.json`. Declared project/document IDs
are checked against that manifest. This association does not discover missing IDs
or prove that an export came from the claimed native document.

For `check_constraints.mjs` evidence, add the same `baseline_id` to the exported
snapshot and constraints JSON. The CLI separates this metadata from the strict
geometry contract and records project/document IDs and exact byte hashes, including
any UTF-8 BOM. Without baseline metadata it can still screen geometry, but the result
cannot support a current-design machine binding. Rerun legacy machine reports that
lack input hashes; never add guessed hashes or relabel an old result. A justified
manual carry-forward remains available under the revision procedure below.

Prefer the bounded execution recorder in `scripts/run_bound_check.py` for connectivity, comparison, body geometry and cost arithmetic:

```sh
python scripts/run_bound_check.py --root /project --project actual-project-id --baseline RevA --check-id USB-PIN-NETS --output evidence/run-001 --timeout 60 connectivity --snapshot exports/schematic.json --contract intent.json
```

The output parent directory must already exist; the run directory must be new. Alternative subcommands are `compare --left schematic.json --right pcb.json`, `geometry --snapshot pcb.json --clearance-mm <actual-rule>`, and `cost --input component-quotes.json`. Their primary design inputs must be listed in the current manifest; every checker input declares the same baseline. A timeout, invalid report or drift produces BLOCKED; a genuine failed check remains FAIL. Output includes raw report.json, stderr.txt, execution.json and one binding.json. It creates fresh outputs and a single binding record, checks design/tool/input hashes before and after execution, and never writes EDA or changes CSV status. Merge a successful subordinate binding into check-bindings only after reviewing its scope. For other tools, retain their genuine raw outputs and write an explicit composite review.

At G5, every PASS check referenced by requirement-checks.json must also have a matching current PASS CSV row and evidence path. Run:

```sh
python scripts/check_evidence.py --root /project --baseline RevA --through G5 --design-gates
```

## Revision and carry-forward

Archive the old candidate's manifest, checks and reports before creating a new candidate. Do not overwrite historical evidence. A changed native file invalidates its manifest; a new manifest digest invalidates old bindings. Re-run affected checks. For checks genuinely unaffected, write a new manual carry-forward assessment linking the historical evidence, current source and reviewed diff, and explain why the checked property remains valid. Do not merely update hashes or baseline labels.

For SCH-UNWIRED, the original zero-wire snapshot remains historical proof of G2-A. The final current binding should cite that snapshot and the traceable progression into G2-B. It must not claim the final wired design contains zero wires. If a later change adds an unreviewed block, inspect that block's placement before its wiring.

These checks verify local consistency and supported report outcomes. They cannot authenticate an intentionally fabricated report, discover unlisted native files, prove unsaved EDA state, or establish electrical correctness from prose. Keep native observations and independently review critical sources. This boundary is explicit rather than hidden behind a PASS label.
