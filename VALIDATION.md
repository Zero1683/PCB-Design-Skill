# v1.8.2-dev validation

2026-09-23, Windows, Python 3.12 and Node 22.23.2. Full regression passed
**451 Python tests and 81 Node tests, zero skips**, plus isolated bridge smoke.
Afterward the assembly coordinate schema was tightened to explicit mm/origin/axes/
angle-view/rotation/bottom fields; all 18 project-review tests and all 10 local
runner tests passed again. No live supplier upload, physical assembly or new
native EDA write was performed.

The 18 new tests cover normal assembly data, missing/duplicate/unexpected/DNP
references, wrong parts/poses, browser edits, units/nonfinite values/tolerances,
state coverage and driver contention, variant selection and generator evidence,
type-sensitive configuration changes, exact allowed port deltas, release roles,
file drift, baseline/source binding, cache invalidation and G5 blocking.

Independent forward evaluation reproduced and verified correction of a variant
iteration defect and Python numeric/boolean equality in nested configuration
comparisons. Normal four-review input, deliberately wrong data, cached reuse and
changed-source rejection were exercised. Final coordinate-schema hardening was
covered by targeted regression. Normalized observations still require genuine
source extraction: hashes establish integrity, not origin or physical correctness.

Existing native PCB routing/rollback and complete-board benchmark limitations
remain. The new helper compares declared operating states and frozen data; it is
not a transient solver, pad-overlap solver, supplier-browser adapter or full
mechanical acceptance tool. Project applicability and coverage remain in existing
requirements; optional absent plans are not automatically generated or certified.

# v1.8.1-dev validation

2026-09-23, Windows, Python 3.12 and Node 22.23.2. The unified run passed
**433 Python tests and 81 Node tests with zero skips**, followed by the isolated
bridge smoke test using simulated clients. No new live EDA or physical-board
acceptance was performed in this update.

New coverage includes accepted exact/maximum dimensions, stale contracts and source
hashes, actual linear manufacturing-outline comparison, malformed/unsupported
outline rejection, cache invalidation after input/rule/code changes, report tampering,
error non-caching, indirect managed-directory references and existing locks.
An independent adversarial review reproduced two false-acceptance paths before
correction: an indirectly referenced cache-directory source and incomplete Gerber
commands. Both now have regression cases; unsupported files cannot pass G5 by
silently inheriting parser defaults.

[Local measurement](assets/local-efficiency-measurement.json): a synthetic fixture
of 150 bodies in 50 overlapping groups returned 604 bytes while retaining its
19,572-byte full failure report. The unchanged repeat reused the result. The
entrypoint changed from 24,719 to 16,317 file bytes. These are byte measurements,
not tokenizer measurements or complete-board quota benchmarks. Assembly height
remains a sourced observation; this update does not add a 3D collision solver.

# v1.8.0 validation

2026-09-22, Windows, Python 3.12, Node 22.23.2. Unified regression completed:
**409 Python tests and 81 Node tests passed, with no skips**, followed by the
isolated bridge smoke test with simulated clients. Earlier runner attempts exposed
legacy test working-directory/CLI requirements; those were fixed in the unified
entrypoint rather than excluding the tests.

The microstrip implementation matches 48 independently generated scikit-rf 1.8.0
quasi-static reference vectors (absolute Z tolerance 1e-6 ohm, effective permittivity
1e-8). I2C tests include TI's published example and invalid inputs. These checks
establish model implementation agreement, not physical impedance tolerances.
Seeded geometry comparisons cover 80 boards at three clearance values, plus
boundary/nested/side cases. A 5,000-component sparse fixture avoids irrelevant
pair checks. A separate 1,500-component timing run is recorded without generalizing
its speedup to complete PCB design.

Real EasyEDA test1, client 3.2.149.88089769: 12 existing parts plus a frame on an
unwired schematic. Preserved the pre-test document source. Collision and boundary
violations returned REJECTED before mutation. A 5-unit C3 move returned APPLIED;
save/close/reopen returned RELOADED_MATCH; rollback returned ROLLED_BACK. A new
capture exactly matched original captured component/pin/property/geometry facts.
The page was saved by the authorized persistence test. The maintenance authorization
record binds only this batch and grants no new-design gate.

See [machine-readable scope and evidence hashes](assets/validation-v180/summary.json).
Raw native captures remain with the local test records; hashes alone are not an
independently replayable native project. Synthetic suites also cover changed
decisions, wrong project/baseline, stale calculator observations, unit mismatches,
out-of-domain models, changed maintenance plans and source evidence.

Whole-board G0-G5 novice-session acceptance, native PCB writes/routing rollback,
browser-calculator end-to-end operation and manufactured-board performance remain
outside this run. No such capability is inferred from the software tests.

# v1.7.0 release packaging

2026-09-22. This release packages the previously validated software and refreshed
documentation. The complete ZIP and its SHA-256 sidecar are release assets.
The staged payload and a fresh ZIP extraction are checked with release_manifest.py;
all bundled files are bound to the v1.7.0 manifest. The latest engineering test
results and their limits are retained below; packaging adds no new hardware claims.

# Documentation refresh on main

2026-09-22. Updated both READMEs, setup/update instructions, third-party notices
and the change summary against the checked-in package. Verified four bundled
source packages and seven runtime package versions, retained original notices,
and separated external-only backends. All 186 local links checked before this
entry resolved; skill frontmatter and whitespace checks passed. This is a
documentation/package update; the 356-case software run below remains the latest
code regression result. No runtime dependencies or engineering behavior changed.

# Unreleased: physical connectivity and mask coverage

2026-09-22, Windows, Python 3.12 and Node 22. **356 automated cases passed**:
the prior 254-case acceptance suite, 40 routing-physics, 45 mask-geometry and
17 physical-assertion/entry regressions. The mask suite includes 1,000 generated
circle/rectangle comparisons against independent mathematical oracles. Seventeen
other toolkit self-test commands also completed without skipped checks. Skill
frontmatter and whitespace validation passed.

NPTH no longer connects copper layers, and explicit via spans constrain actual
reach. All repeated-number lands participate in connection/isolation assertions.
Protected routes are compared with baseline geometry, while equivalent straight
segmentation and polygon ring start/winding remain accepted. Mask inspection uses
actual opening unions, handling offset, concave and jointly covering openings.
Empty coverage, missing plating, unverified native span encodings and unsupported
mask semantics are not promoted to PASS.

Independent CLI review found four additional defects during this update: polygon
vertex sorting erased protected shape topology; zero clearance accepted overlapping
nets; zero-area polygons counted as pads; and the name RoundRect overrode a macro's
actual outline. All four were reproduced, corrected and independently rechecked.
Additional controls cover repeated lands in both orders, NPTH/through/blind-via
connections, positive opening unions, narrow slits and malformed parameters.
Raw original and repaired outcomes remain in independent-physics-review and
physics-fix-validation under the task workspace.

The first broad regression invocation used the read-only repository as its scratch
working directory and timed out; rerunning from the writable task directory passed.
No test assertions or production rules were relaxed to obtain these results.

Limits: physical pad copper still does not subtract drill voids, and actual pours
are excluded. Legacy neutral vias without declared type/span still mean through.
Array-format drilled pads/vias and record-format blind/rule-based vias or hidden
inner lands need a verified adapter. Mask macros support literal exposed outlines;
parameterized/compound RoundRect, stroked openings, compound regions and region
arcs require another capable checker. Partial openings require an explicit policy
and separate solderable-area review. These are local software checks: no live EDA
write, whole-board benchmark, physical-board test or GitHub publication occurred.

# Unreleased: adversarial acceptance fixes

2026-09-22, Windows, Python 3.12 and Node 22. **254 automated cases passed**:
37 outline/public-CLI, 22 physical-pad identity, 13 report provenance, 14 evidence
bindings, 13 bounded checker execution, 21 toolkit, 14 circuit checks, 1 registry
gate sweep, 10 requirement coverage, 11 cost, 16 substitutions, 27 data/recovery
and 55 native-runtime/constraint mocks. Skill frontmatter and whitespace checks
passed. An independent read-only review additionally ran all five report-producing
CLIs with positive and negative inputs (10 executions); outcomes matched.

The four original reproduced defects are fixed. A missing 5 mm outline segment
now exits 2; copper at 0.1 mm against a requested 0.3 mm edge margin exits 1;
the original conflicting repeated-pad map exits 2; a genuine archived report with
an old baseline is rejected even when its surrounding binding claims the current
baseline. The outline dimensions follow the drawing centreline without subtracting
pen width.

Adjacent regressions cover shuffled/reversed valid loops, concave notches,
whole copper edges and slot centrelines, tangency and exact threshold acceptance,
empty inputs, malformed numeric rules, duplicate element identities and JSON keys,
legitimate repeated-number same-net lands, contradictory schematic pin memberships,
report input drift and foreign project/document IDs. All-unfitted body checks are
not accepted as successful screenings; a COMPLETE_QUOTE summary cannot hide an
UNPRICED row. Input hashes cover the exact bytes parsed, including a UTF-8 BOM.
The first constraints metadata test revealed strict geometry rejecting baseline_id;
the CLI now separates that metadata before evaluating the unchanged geometry schema.

The outline reader supports one simple ring. Internal cutouts, multiple rings and
self-intersections remain explicitly unsupported. Gerber arcs and some rounded
apertures are approximated; close curve clearances still need independent native
or exact checks. Missing data is not converted into geometric acceptance. Recorded
hashes establish local association, not execution authenticity, electrical correctness
or the identity of an unlabelled native export.

No live EDA writes, whole-board G0-G5 run, physical-board verification or publication
were performed in this update. Public v1.6.0 is unchanged. Local raw regression logs
and original reproductions are retained in the task workspace's
acceptance-fix-validation and outline-fix-work directories.

# Unreleased: current-design evidence and conservative substitutions

2026-09-22, Windows, Python 3.12 and Node 22. This local update passed 147 automated cases: 55 native-runtime/constraint mocks, 14 evidence-binding, 10 requirement-coverage, 1 full-registry gate sweep, 13 bounded-check execution, 16 substitution review, 11 cost arithmetic, 11 release/helper and 16 workflow cases. Skill frontmatter validation passed. One test invocation initially omitted its required --workdir argument; rerunning with the correct argument passed all 13 cases.

The registry sweep removes every selected mandatory row in turn. Other cases cover stale native files and reports, revised manifests with old bindings, N_A reclassification, whitespace status bypass, junction roots, failing reports claimed as PASS, tool/input drift during execution, timeout and exit/report disagreement. Four supported checks run as real local subprocesses; native EDA runtime tests in this update use mocks.

Independent review reproduced savings obtained solely by reducing spare quantities. The fix derives the before/after BOM delta, requires every changed SKU/quantity to be reviewed, rejects an unchanged supporting-BOM claim when data differs, and requires separate decision evidence for reduced total spares. Sixteen substitution cases verify these controls along with requirement completeness, raw quote correspondence, stock and identity. Neither retained captures nor manual assessments establish supplier authenticity or electrical equivalence by themselves.

The bridge version diagnostic now reads the bundled package version. Apply, replay, resume and save/reopen share actual-geometry acceptance; returning to a known defective repair baseline remains explicitly distinguishable from a valid design.

No live EDA modification, current distributor query or complete G0-G5 board benchmark was performed for this update. The user will run that benchmark in a fresh task using reference 28. No public release is made by this local sync; v1.6.0 remains the published release. Local binding guarantees cover declared saved files, not unlisted sources or unsaved native state.

# Unreleased: component cost planning

2026-09-22. The new G0/G1 intake-to-BOM quote workflow and G5 price reconciliation are linked from SKILL.md, both READMEs and both project templates. Cost reduction preserves the confirmed feature/performance baseline and requires explicit agreement for reductions.

Eleven synthetic calculation regressions passed: MOQ vs consumption, order increments and tiers, spares, lower-MOQ cash savings, missing quotes, insufficient/unknown stock, mixed currency/tax/pack rejection, duplicate SKU aggregation, uncovered price tiers, invalid fields and nonmutation. Three CLI smoke cases returned the documented codes 0/1/2 with UTF-8 JSON for complete/missing quotes. Skill validation and whitespace checks passed.

No live distributor quote, pricing API integration, checkout or EDA operation was performed for this change. Agents must collect current quotes through available read-only tools; the calculator verifies declared arithmetic, not market prices, complete BOM coverage or electrical equivalence. This remains an unpublished local development update.

# Unreleased: repair correctness and requirement coverage

2026-09-22, Windows, Node 22.23.2 and Python 3.12. 131 relevant regression cases passed: 34 guarded native-runtime mocks, 10 constraints, 10 requirement/evidence coverage, 8 output-budget, 52 data/layout/batch, 16 workflow and 1 existing design-gates scenario. Skill frontmatter validation passed. These are software checks, not board acceptance.

Independent review reproduced four runtime faults: unchecked final spacing within bbox comparison tolerance, intermediate collisions, stale successful replay after external edits, and replay on a different document. It also demonstrated separator-only CSV evidence paths passing without a file. Regressions now cover these paths. Final native captures and actual spacing are rechecked; ordered intermediate states are preflighted before writing; replay reads native state and identity; evidence lists must contain files.

Native validation ran on authorized test1, with 12 parts, one sheet and no wires/buses. An unfilled rectangle reported FillStyle=null and FillColor=null; a separate Solid probe reported Solid and its color. Contained movement, save/close/reopen, explicit inverse restoration, source-rule rejection and scoped allowed-region repair passed. Final capture exactly matched the pre-test snapshot after all temporary graphics were removed.

The final repeat encountered one native `cmdKey` exception. The runtime reported ROLLED_BACK and its captured source/restored states matched. A fresh capture and new batch then passed repair, save/reopen and rollback. A rectangle deletion returned true while readback still listed it; deletion using the fresh native object and subsequent capture confirmed removal. Native API return values alone were not accepted as restoration evidence.

Local audit records are retained in `review-fix-live` and `review-fix-live-final` in the task workspace. The final directory includes original/framed captures, move-journal, rejected-source journal, failed repair journal, successful repair-retry journal and restored-confirmed capture. Native injected external-edit and intermediate-collision scenarios remain mock tests; the native exception above is an observed API failure, not a controlled failure benchmark.

Requirement coverage verifies declared mappings and current source/report hashes only. Whole-board G0-G5 benchmarking, PCB native writing/routing rollback, full 3D checks and hardware acceptance remain pending. The capability matrix and next benchmark are in reference 25. This update is a local development build; v1.6.0 remains the published release.

# Unreleased: constraints, resume and bounded context

2026-09-22, Windows. 28 Node tests (18 guarded runtime, 10 pure geometry constraints), 8 output-budget tests, and 52 adjacent Python cases passed: 88 total. The standalone PCB constraint CLI passed on the provided example. Skill frontmatter validation passed.

Independent read-only review found two concrete issues: text-mode stdout exceeded a byte budget on Windows and could use a non-UTF-8 codepage; changed constraint files blocked read-only inspection. Both were fixed. CLI output now writes UTF-8 bytes plus a single newline; status/resume remain readable while changed constraints block mutation. The reviewer also exercised 1000 randomized pagination cases without skipped/duplicate records or stalled cursors.

New constraints and resume behavior were tested with native API mocks and exported synthetic geometry. The connected EDA was on a different project, so no native writes were performed for this update. Prior v1.6 native results below do not validate these new paths. PCB routing mutation/rollback, full 3D checking, complex-board acceptance and token savings remain unverified.

# v1.6.0: guarded native operations

2026-09-21, Windows, Node 22.23.2, connected EasyEDA client and bundled API reference. Authorized test1 page contained 12 parts, one sheet, no wires or buses. Native capture, collision and bounds rejection, property-preserving move, save/close/reopen, explicit rollback with save, and exact restored snapshot comparison passed.

The first coordinate-only native modify changed SupplierId and cleared several OtherProperty values. Readback caught it and blocked blind recovery. The affected test component was explicitly restored from the original snapshot and exact comparison passed. The adapter now sends all documented writable properties for both forward and inverse operations. The corrected native sequence passed again.

14 Node regression cases cover prewrite rejection, stale inputs, unsupported fields/wired pages, duplicate IDs, property preservation, injected second-write failure with automatic compensation, concurrent changes, inverse failure, idempotency, wrong target, reload mismatch and serialized execution. Automatic mid-batch failure compensation uses mocks; native validation exercised explicit rollback. No PCB routing rollback, global interception, token benchmark or electrical acceptance was performed.

# v1.5.2: batch preflight and repair feedback

2026-09-21, Windows/Python 3.12. Eleven new cases exercise full-target preview,
stale source rejection, scoped geometry proposals, protected-fact and persistence
failures, unchanged/repeated/bounded retries, adapter revision, idempotent ledger
recording, corruption rejection and CLI behavior. Adjacent data/recovery (27)
and layout (14) tests are rerun for publication: 52 cases total.

Independent read-only review ran the initial 10 cases and found no additional
concrete defect beyond the adapter revision issue being addressed: a corrected
adapter must be distinguishable from an unchanged plan/adapter retry. Explicit
adapter IDs now participate in that decision and are covered by tests.

An initial subprocess-test encoding mismatch on a Chinese Windows path was fixed
by explicit UTF-8 in both child execution and output decoding; CLI output is now
asserted as well as exit status. The corrected 11-case suite passed cleanly.

No native API interception, adapter capture/application, live save/reload,
physical manufacturing, supplier query or token-saving benchmark was performed.
Reports and ledgers contain declared observation evidence, not independent proof
of native execution or electrical correctness. Existing v1.5.1 records follow.

# v1.5.1: measured schematic layout execution

Windows synthetic validation, 2026-09-21: 14 new tests passed, covering both
formats, deterministic block placement, obstacles, stale input, CLI exits,
identity/pin/property drift, missing frames and reload-like position loss.
Independent read-only review also screened 30,000 random packing cases: all
27,465 successful plans obeyed tested bounds/frame/obstacle clearances. It found
unprotected extra object fields and tolerance permitting a frame outside bounds;
both were corrected with regression tests. An initial obstacle-row packing failure
was corrected before the final test run.

The source fixture and readbacks are synthetic. No native EDA writer/extractor,
client save/reopen, electrical correctness, physical PCB or token saving was
validated in this update. Commands plan rigid, already arranged unwired blocks;
they do not automatically solve local circuit layout or wired pages.

# v1.5.1: reconciled data and isolated recovery

Validated on Windows, 2026-09-21. This section covers the current working update; older release records follow.

- 27 new data/operation regression tests passed (`scripts/test_data_operations.py`). They cover lossless input round trips, observed/intent separation, repeated-pad and NC handling, pagination/deltas, stale data/report rejection, evidence preservation, candidate recovery and interruption between directory renames.
- 21 existing PCB toolkit regression tests passed after the additive native component ID field. The importer self-test passed for both supported synthetic record dialects.
- Independent read-only review found three defects: repeated pads borrowing a missing element net, broken archived evidence paths, and status reporting historical acceptance after file changes. All three were corrected and have passing regression cases.
- Recovery preserves the source and failed candidate. It operates only on isolated, closed-file project bundles; declared dependency completeness and reopen evidence still need actual native validation.
- No live EasyEDA operation, native project recovery, macOS execution, physical board, or measured token-saving benchmark was tested. Synthetic checks do not establish electrical acceptance.

# Validation record: 1.3.0

Date: 2026-09-21. Local platform: Windows; Node.js 22.23.2. These results describe the skill package and helper behavior, not a certified PCB design.

| Area | Result | Evidence/method | Limit |
|---|---|---|---|
| Skill structure | PASS | System skill validator | Frontmatter/structure only |
| Existing helpers | PASS, 11 tests | `python -X utf8 scripts/test_helpers.py --workdir <temp-root>` | Initialization and release integrity |
| Workflow helpers | PASS, 16 tests | `python -X utf8 scripts/test_workflow.py --workdir <temp-root>` | Known arithmetic, record rejection, normalized exports, envelope screening, localization and fake-bridge probe |
| Actual bridge server with simulated clients | PASS in 1.2.0; unchanged code, not rerun for 1.3.0 | `node scripts/test_bridge.mjs --workdir <temp-root>` | Window switching, nonexistent-window isolation and explicit-window request routing; no EDA client |
| Local live connection | BLOCKED at the previous check; not re-probed for 1.3.0 | Existing bridge reported `WAITING_FOR_EDA`, zero windows | No client connection; old running bridge also reports upgrade recommended |
| Live project creation/edit/routing/export/reopen | NOT_RUN | Procedure in reference 11 | Must be tested in a disposable connected project |
| macOS end-to-end | NOT_RUN | Cross-platform commands documented | Windows execution and a Mac scenario review do not establish macOS execution |

## Circuit intent and reuse in 1.3.0

Added independent pin-relationship checks, normalized component/pin revision differences, and reusable-block guidance. Native EDA remains the implemented design source. All new runtime code uses Python's standard library; no PCBDL runtime, copied source, exporters, or component libraries were introduced.

- Reran the 11 helper tests and 16 workflow tests: PASS.
- Added and ran 14 circuit-check regression tests: PASS, including CLI exit codes. Cases cover changed net names, wrong connections, merged rails, unexpected DNP branches, disconnected endpoints, intentional NC violations, missing endpoints, partial/stale/BOM inputs, invalid rules and duplicate JSON keys, component additions/removals, BOM exclusion changes, and revision comparison guards.
- Skill structure validator passed. Checked 84 local Markdown link targets: all exist.
- An independent read-only agent reviewed the tools and relevant guidance and reran the 14 new tests. It found no substantive incorrect PASS behavior within the declared scope or conflict with native-EDA authority and staged schematic drafting.

The inputs were synthetic fixtures. No connected EDA extraction, native ERC/DRC, physical routing, or real hardware was tested for this update. Coverage declarations and source authenticity still require review. Passing declared pin relationships does not establish ratings, timing, impedance, or continuity of fabricated copper. Revision reports compare declared component properties and pin nets only.

## Schematic drafting update in 1.2.1

- Compared the drafting reference against all eight supplied organization rules. Included the original visual example with its provenance and licensing scope. No fixed minimum package size was introduced.
- Added G2-A component/placement review before wiring and G2-B connection/electrical/drawing review. Zero wire/bus counts belong to the scoped placement snapshot only; existing wired designs are reviewed in place.
- Reran the structure validator and all 27 Python helper/workflow tests: PASS. Initialized English and Chinese records in isolated temporary directories: both contain the same 36 check IDs/stages/applicability values, all initially NOT_RUN. The record checker correctly leaves the five new checks pending. Temporary records were removed afterward.
- Checked 75 local Markdown link targets: all exist. Inspected the supplied image and confirmed it is a wired presentation example, not a placement-only snapshot.

An independent agent read the skill and relevant references, without the scenario acceptance table, and described its actions for three requests: creating a complete new schematic from approved selections, reviewing an existing wired schematic read-only without placement history, and adding a sensor block while preserving existing wiring. It retained the requested scope, required placement evidence before new wiring, continued without an extra approval gate, preserved existing connections, and did not invent missing historical evidence. No blocking instruction conflict was found.

This was a read-only behavioral review. The agent did not create a schematic or operate EDA. Native wire counts, rendered drawing quality, ERC, and cross-platform drafting remain untested on a connected client for this release.

## Independent scenario review in 1.2.0

An independent agent was given the skill and two realistic requests without the acceptance notes or prior conclusions. It read the needed files without modifying files or accessing EDA:

1. A MacBook beginner has installed EasyEDA and Gateway and wants a 30 × 40 mm USB-powered temperature/humidity board, manufacturing files only, self-purchased parts.
2. An existing board has reviewed power/USB routes and needs ordinary GPIO/I²C routing plus supply review, with only a multimeter available.

The proposed actions loaded the bundled API, separated setup from project creation, kept the G5 stopping point, avoided purchasing, preserved existing critical routes, and selected explicit ordinary nets for native autorouting. Electrical reasoning separated known trace drop from missing via/contact resistance. Under the stated example assumptions, the 100 mm total copper path gives 98.514 mΩ and 29.554 mV at 0.3 A, without declaring the full path passed.

The review identified and the package addresses:

- An undefined variable in the bridge window-selection success response. Fixed and covered by the simulated-client regression.
- Two stale `openProject(projectPath)` instructions. Corrected to UUID and documented in third-party patch notes.
- No documented router completion-status API. Instructions now require verified installed-version semantics or native UI completion observation before further mutation; actual lifecycle verification remains pending.

This is a dry-run behavioral assessment, not measured design quality, hardware performance, or token savings. The additional scenarios in reference 11 remain a test plan until independently executed.

## Reproducing package checks

Run from the package root; choose a writable temporary directory on your working drive:

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/temp-root
python -X utf8 scripts/test_workflow.py --workdir /path/to/temp-root
python -X utf8 scripts/test_circuit_checks.py --workdir /path/to/temp-root
node scripts/test_bridge.mjs --workdir /path/to/temp-root
```

The bridge regression starts and stops only its own isolated temporary server. It uses simulated clients and does not select or modify an actual EDA project. The workflow probe test briefly uses an unoccupied local bridge-range port; it skips that test if all ports are occupied.

## Local visual-gate correction, 2026-09-21

Reviewed the ESP32-C3 USB development-board trial log and supplied schematic images. The trial exposed dense overlapping pin/net text, missing graphical block separators, late off-sheet attribute repair, and a gap between body-envelope screening and pad/silkscreen validation. Its CHECKS record explicitly leaves schematic presentation and final ERC unresolved; it is not evidence of successful visual acceptance.

Added early page/block/text gates, distinct positive pad/silk/mask clearance checks, bounded coordinate repair, six bilingual check-template rows, and a standard-library conservative object-bounds screen. The screen consumes normalized native-derived geometry; it is not an EasyEDA extractor and cannot certify coverage or text readability.

Validation: Python 3.12.14 ran 49 tests: 48 passed, one existing symlink test skipped because Windows denied symlink creation. All 8 new geometry regression tests passed. Existing 16 workflow and 14 connectivity tests passed; 10 of 11 existing packaging tests passed with that one skip. System skill structure validator passed using the system Python environment. The older default Python cannot execute some existing Python 3.10+ helpers; use the documented supported runtime. No dependencies installed.

No live EDA repair or new end-to-end board run was performed for this correction. The existing PCB project and manufacturing artifacts were not modified. This is a local skill revision, not a published release or a claim that the trial board is now fixed.

## Schematic presentation modes, 2026-09-21

Both free-layout without a standard outer frame and partitioned standard sheets are supported. Boundary checks use the selected custom export rectangle or the inner sheet frame, respectively; metadata reservation is conditional. Updated routing instructions and bilingual check labels without changing geometry code. No live EDA changes were made.

## Strict format gates and bounded repair, 2026-09-21

Only free-layout and framed-layout are permitted for new/redrafted schematics. Added a required SCH-FORMAT record and --design-gates profile to reject missing/non-PASS/wrong-stage required gates or other formats. Added common drafting remedies and item-specific harmless-warning dispositions. Unreadable content, missing partitions, overlaps, electrical uncertainty and manufacturing defects are not minor-warning exemptions.

Validation: new design-gate regression covers both allowed modes, disallowed mode, omitted gate, G2-only scope, N_A bypass, wrong stage and stale baseline; passed. All 16 existing workflow tests and skill structure validation passed. No live EDA test performed.

## Trial-driven early checks and release workflow, 2026-09-21

Added PART-IDENTITY at G2, ROUTING-READY at G3, and RELEASE-FREEZE at G5 to the strict design profile and bilingual templates. Selection verification must independently resolve the supplier specification, including displayed 22-ohm versus selected 220-ohm mismatches. Routing readiness covers native outline recognition, actual rules and tool capability. API bulk edits require one-object persistence/protected-field review. Release guidance consolidates defects, freezes a reviewed candidate, and maps each mutation to affected rechecks.

Validation on Python 3.12.14: 39 tests passed (1 expanded gate regression, 16 workflow, 14 connection/revision and 8 geometry tests). The gate regression now removes every required gate in turn to verify rejection, and retains both valid formats, G2 scope, N_A/wrong-stage/stale-baseline rejection cases. Skill structure validation and git diff whitespace checks passed. These checks exercise helper behavior and record contracts, not live EDA correctness; no new end-to-end design or hardware test was performed. No PCB files or external repository were modified by this local update.

## Bundled schematic methods integration, 2026-09-21

Bundled easyeda-schematic-net-fanout 1.2.0 at upstream commit
`0c4b9a0ad94d532923dee5c828a6efa7444f4506`. Added reference 15 as the
integration adapter, routed it from the entrypoint and EDA/drafting references,
and updated both READMEs, setup, provenance and scenario definitions.

- Main skill and bundled enhancement entrypoint passed the local structure validator.
- Checked 102 first-party Markdown file links: all targets exist.
- The three vendored upstream files match the reviewed installed snapshot byte-for-byte
  (including its documented compatibility-metadata relocation).
- Reviewed the new paths for placement-only staging, dense rotated labels and
  partially completed batches: the adapter retains G2-A before fanout, geometry
  verification, independent pin nets and ownership-aware cleanup. This was an
  author review; the added behavioral scenarios have not been independently run.
- No runtime implementation changed in this update; helper suites were not rerun.
  Prior helper results above retain their original scope.

No bridge was started and no live EDA project, manufacturing output or hardware
was modified or tested. Connected-client probes and native render/save/reopen
remain required before claiming live integration acceptance.

## GitHub publication check, 2026-09-21

Reran all five Python suites on Python 3.12.14 before publishing the combined
visual-gate and schematic-methods update: 50 cases, 49 passed, one skipped.
The skipped case is test_reject_symlink: Windows returned WinError 1314 while
creating its fixture. No symlink-rejection PASS is claimed for this run.
Suite totals: helpers 11 (10 passed, one skipped), workflow 16, circuit checks
14, design gates 1, visual geometry 8. Native EDA and physical hardware were not
tested. Main and enhancement skill structure checks and diff whitespace checks
passed during integration. The package manifest is regenerated from a clean
snapshot excluding .git and runtime/cache data, then verified before commit.

## Operation foundations integration, 2026-09-21

Updated official API documentation to 1.1.36 and bundled official native-format
references, schemas and validator at the commits recorded in UPSTREAM.md. Removed
17 obsolete API reference pages removed upstream. The API bridge runtime remains
byte-identical to v1.4.0, retaining the selected-window response and health fixes.
Community CLI/MCP projects were source-reviewed only, not installed or executed.

The strict primitive wrapper passed all 8 Node regression cases, covering explicit
document/type dispatch, unsupported pairs, outer metadata, DOCHEAD domain, invalid
input, schema/native discrepancy preservation and CLI error behavior. Simulated
bridge tests passed; they use isolated ports and fake EDA clients. Main and format
skill structure checks passed. No Python implementation changed; the 50-case run
above retains its original scope. All 114 first-party Markdown file targets exist. Package byte integrity is
verified against a clean snapshot during final synchronization.

No live EDA project was edited or tested. Full-document import/save/reopen, actual
backend interoperability, electrical correctness and hardware remain untested by
this update. Primitive schema success certifies only the stated schema scope.

## Adapted PCB inspection toolkit, 2026-09-21

Bundled the script subset of daishuge/pcb-skill at
6e939b64907e3c63236c7522c511af5d7d1afaad, preserving MIT attribution. The upstream
skill, setup/approval automation and purchase workflow are not included. Our
existing workflow and applicability remain unchanged. Source and local changes
are recorded in vendor/pcb-skill-toolkit/UPSTREAM.md; reference 18 routes usage.

Regressions first reproduced false assertion passes, ignored Gerber polarity,
stale-output completion and missing-footprint/multiple-PCB loss on the original
implementation. The adapted code now rejects these cases. The Windows process
probe was tested on a spawned disposable child: checking it did not terminate it;
after explicit test cleanup it was reported gone. No live user process was signaled.
Unsupported Gerber polarity, transforms, aperture holes and macros fail explicitly;
this is fail-closed coverage, not an implementation of those formats.

Validation on Python 3.12: all 21 new regression cases passed. The original five
Python suites were rerun with their documented CLI options: 50 cases, 49 passed,
one skipped because Windows denied symbolic-link creation (WinError 1314).
All 21 bundled script self-tests passed, including the two NumPy-dependent tests;
NumPy was already available and no package was installed. These are synthetic
fixtures, not 21 real boards. Main skill structure and diff whitespace checks pass.
Link and package integrity checks accompany final synchronization.

Initial generic unittest discovery omitted an existing suite's required workdir,
and one suite was then given an unsupported workdir option; these harness invocation
errors were corrected without changing existing tests. The results above are from
the successful documented invocations.

No EDA project, live bridge, supplier account or hardware was touched. Native
export coverage on a new real board, client import/save/reopen, macOS execution,
external router interoperability and physical manufacturing acceptance remain
unverified. The Windows process probe has direct local runtime evidence only.

## Engineering constraint review, 2026-09-21

Reviewed the article text supplied by the user against manufacturer/tool references.
Added reference 19 and links from the entrypoint and G1-G5 instructions, keeping
the existing EDA backend and schematic formats. English/Chinese project records
now carry critical-source/calculation/rule/readback fields and four scoped checks:
STACKUP-RULES, DENSE-ESCAPE, THERMAL-PATH and MFG-APERTURES.

Added sourced first-order mask-pair, straight escape-channel and circular annular-ring
calculations to the existing helper. Negative margins are preserved as results;
CALCULATED is not a fabrication or electrical approval. The example values are
synthetic and include an infeasible channel. No impedance or thermal solver was added.

Executed on Python 3.12: 10 new arithmetic/CLI regression cases passed; workflow
16 passed; helpers 10 passed with one skipped Windows symlink fixture (WinError 1314);
design gates 1 passed. Total this run: 38 cases, 37 passed, one skipped. Tests cover
two-sided expansion, lost mask dams, negative expansion, invalid inputs, unequal
pads/multiple traces, infeasible clearance, radial offsets, explicit hole basis,
source requirements and output status. Main skill structure and git diff --check passed.
First-party links, English/Chinese check IDs and installed package hashes are checked
during synchronization. Added behavioral scenarios are specifications, not executed
agent evaluations. Native EDA, real exports and physical hardware were not tested.

## v1.5.0 release rerun, 2026-09-21

All seven first-party Python suites were rerun: helpers 11 (10 passed, one Windows
symlink-permission skip), workflow 16, circuit checks 14, design gates 1, visual
geometry 8, inspection toolkit 21 and fabrication arithmetic 10. Total: 81 cases,
80 passed and one skipped. All 8 Node format-validation cases passed. Simulated
bridge window selection/isolation/routing passed with --workdir after correcting
an initial invocation that omitted this required option. No runtime fix was needed.
Package files, staged Git inventory and archive hashes are checked before publication.
No live EDA or physical hardware validation is claimed.

## v1.5.1 publication check

All 27 data/recovery and 14 schematic-layout tests reran successfully for publication.
The release ZIP is rebuilt from the manifest inventory and verified after extraction.
Existing 21 toolkit tests and importer self-test passed during this version development.
No new live EDA or hardware validation is claimed.
