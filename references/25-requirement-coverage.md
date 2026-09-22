# Requirement coverage and verification scope

Read this at G0/G1, when requirements change, and before G5 release freeze. Geometry checks evaluate supplied rules only. They cannot discover a missing connector position or an omitted power requirement.

## Persistent mapping

Keep these project-local documents under revision control:

- `requirements.json`: schema 1, nonempty `project_id`, current `baseline_id`, and a nonempty `requirements` array. Each requirement has a unique `id`, a concrete `statement`, and `source: {path, sha256}` pointing to a nonempty local requirement record or original technical source.
- `requirement-checks.json`: schema 1, the same project/baseline, `requirements_digest`, and a `checks` array. Each check has a unique `id`, nonempty `requirement_ids`, `method`, `subjects` identifying actual nets/parts/interfaces, and `status` (`NOT_RUN`, `BLOCKED`, `PASS`, or `FAIL`). PASS and FAIL need `evidence: {path, sha256}` pointing to the actual nonempty report.

`sha256` hashes file bytes. `requirements_digest` uses `workflow_io.digest()` on the entire parsed requirements object: sorted-key JSON, UTF-8, compact separators, no NaN. Generate values from actual files with `workflow_io.file_hash()` and `workflow_io.read()`; do not manually invent hashes. Referenced files must stay inside the project and cannot pass through symbolic links or junctions.

A representative *unperformed* check is:

```json
{"id":"MECH-J1","requirement_ids":["REQ-USB-POSITION"],"method":"Compare transformed native connector geometry with enclosure drawing","subjects":["J1"],"status":"NOT_RUN"}
```

At intake, reconcile requirements with the user's request and source documents. Include applicable power/load and operating conditions, interfaces, boot/recovery, mechanics, assembly and test access. A compact project needs only relevant requirements. Review this list for omissions before calling its coverage complete. Derive executable constraints and electrical checks from it; preserve sources and units.

```sh
python scripts/requirement_coverage.py --root /project --baseline RevA
python scripts/check_evidence.py --root /project --baseline RevA --through G5 --design-gates
```

The first command exits 0 for complete mapping with matching file hashes, 1 for uncovered/unverified requirements, and 2 for malformed or stale records. At G5 and later, `--design-gates` requires both files and complete current coverage. Existing projects must add the mapping and evidence; old PASS rows alone no longer satisfy this gate. Earlier G2/G3 inspections remain available.

Requirements without checks are `UNMAPPED`. Any pending check keeps the requirement unverified; a failed check cannot be hidden behind another PASS. Changing a requirement invalidates its mapping digest. Changing source or evidence bytes invalidates the corresponding hash. After a design revision, re-run affected checks on the new baseline and record the actual exported inputs used. Never refresh hashes just to silence an error.

The result reports mapping and integrity only. It does not parse every report's engineering meaning, establish that declared requirements are exhaustive, or by itself establish native-source provenance. G5 also requires the [current-design bindings](27-current-design-evidence.md), including corresponding PASS CSV rows for mapped checks. Inspect original observations, bind their input hashes and document identity, and complete electrical/manufacturing review. `engineering_correctness` remains `NOT_ASSESSED`.

## Capability and evidence matrix

| Capability | Current evidence | Remaining boundary |
|---|---|---|
| Existing unwired schematic part moves | Native test1 capture, preflight, actual move, save/reopen and inverse restoration | No part creation, wiring or whole-project rollback through this writer |
| Unfilled rectangular partition frames | Native no-fill representation and contained move tested | Rounded, non-axis-aligned or ambiguous shapes use conservative obstacles |
| Directed contract repair | Native source rejection, scoped repair, persistence and restoration tested | Existing defects must be enumerated; target rules remain mandatory |
| Drift, intermediate collision and stale replay rejection | Adversarial native API mock regressions | Does not intercept callers bypassing this entrypoint |
| PCB mechanical constraints | Synthetic exported-geometry checks | Native capture completeness, PCB writing and routing restoration need live qualification |
| Requirement coverage | Mapping, hash, missing evidence and G5 integration regressions | Semantic engineering acceptance remains a separate review |
| Whole-board G0-G5 workflow | Not benchmarked in this update | No claim of production readiness, HDI/DDR capability or measured token savings |

## Next benchmark before broadening native writes

Use one authorized project with fixed requirements and a known-good source backup. Choose a representative MCU board and record tool/API versions, exact source/export hashes, elapsed time and operation counts. Exercise intake, component verification, one of the two schematic formats, netlist comparison, footprint/spacing checks, routing and final fabrication export. Read back and independently inspect the exported files; run the coverage gate against those reports.

For recovery, first add a bounded native PCB operation with capture, preflight, property-preserving write, readback, save/reopen and inverse tests. Inject one failure and verify original identity, nets, geometry and rules afterward. Unsupported primitives or an unknown current state must stop recovery. Record each stage as PASS, FAIL or NOT_RUN with evidence; a passing schematic move cannot substitute for the entire benchmark.

Use [the fresh-session benchmark](28-fresh-session-benchmark.md) for the next whole-board test. Keep its stage outcomes NOT_RUN until observed.
