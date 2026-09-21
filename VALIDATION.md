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
