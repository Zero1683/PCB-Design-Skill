# Unreleased: reconciled data and isolated recovery

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
