<p align="center">
  <img src="assets/logo.svg?v=2" width="156" height="156" alt="PCB Design to Bring-up logo">
</p>

<h1 align="center">PCB-Design-Skill</h1>

<p align="center"><strong>PCB engineering for AI agents</strong></p>
<p align="center">Schematic design · PCB layout · Manufacturing · Board bring-up</p>

<p align="center">
  <a href="https://github.com/Zero1683/PCB-Design-Skill/releases"><img src="https://img.shields.io/github/v/release/Zero1683/PCB-Design-Skill?style=flat-square&amp;label=release&amp;color=333333" alt="Latest release"></a>
  <a href="https://github.com/Zero1683/PCB-Design-Skill/stargazers"><img src="https://img.shields.io/github/stars/Zero1683/PCB-Design-Skill?style=flat-square&amp;color=333333" alt="GitHub stars"></a>
  <a href="https://github.com/Zero1683/PCB-Design-Skill/issues"><img src="https://img.shields.io/github/issues/Zero1683/PCB-Design-Skill?style=flat-square&amp;color=333333" alt="Open issues"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-333333?style=flat-square" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/EasyEDA-bundled-333333?style=flat-square" alt="EasyEDA tools bundled">
</p>

<p align="center"><a href="#recent-updates">Recent updates</a> · <a href="#bundled-third-party-tools">Third-party tools</a> · <a href="#installation">Installation</a> · <a href="#capabilities">Capabilities</a> · <a href="#usage">Usage</a> · <a href="#documentation">Documentation</a></p>
<p align="center"><a href="README.md">简体中文</a> · <strong>English</strong></p>

---

Turn hardware requirements into circuit designs, PCB projects, and manufacturing files, with procedures for footprint verification, layout review, and board bring-up. Bundled EasyEDA API documentation, schematic methods, a local bridge, and runtime dependencies support live operations in the EasyEDA desktop client. The API layer supplies operation interfaces; the methods library covers functional blocks, batch placement, selective net fanout, and revision cleanup.

## Recent updates

**v1.8.2-dev (local development build)** integrates sourced reviews for populated references, BOM and submitted/imported placement, declared operating states, active generator variants, allowed derivative-board changes, and release artifact roles/revisions/hashes. The local batch runner returns bounded summaries. Methods were reviewed from Keitark/pcba-design-skills and implemented locally without adding vendor runtimes. See [schemas and scope](references/36-project-reviews.md).

Actual source exports and adapter evidence are required. These checks do not inspect supplier web previews, prove physical assembly or startup transients, or replace ERC/DRC, fabrication parsing and visual review.

**v1.8.1-dev (local development build)** adds offline check batches and accepted-dimension checks. Full reports stay on disk; callers receive bounded summaries. Changed inputs, rules, checker code or referenced evidence invalidate reuse. Live EDA state, DRC and shop prices are not cached as current observations. The entrypoint loads operation-specific documentation on demand. See [local execution](references/33-local-execution.md) and [mechanical dimensions](references/34-mechanical-envelope.md).

A synthetic 150-component check produced a 19,572-byte full report and a 604-byte returned summary; an unchanged repeat reused the report. All detected failures remain in the full report. These measurements establish output size and cache reuse, not model-token or complete-board quota savings.

The v1.8.0 release passed 409 Python tests, 81 Node tests and an isolated bridge smoke check without skips; real test1 checks covered native movement, rejection, save/reopen and rollback.

**v1.8.0** adds beginner-facing requirements, automated calculations and guarded-operation validation. See [validation](VALIDATION.md) for evidence and [changelog](CHANGELOG.md) for version history.

- **Define the object first.** Recover purpose, carrier/enclosure, board dimensions, power, accessible controls/connectors and assembly preferences; show a dimensioned plan and component estimate. Reuse existing answers and delegation. The agent researches engineering parameters.
- **Automate applicable calculations.** Add I²C pull-up checks and bounded microstrip impedance/width synthesis. Unsupported geometry requires an applicable manufacturer tool. Browser results retain displayed inputs, units and warnings.
- **Separate new design from scoped maintenance.** New-design moves require the plan record; authorized maintenance binds its exact batch without a fresh product interview. Native identity, geometry, collision and recovery checks still apply.
- **Make failures actionable.** Pin-net errors identify affected objects and repair hints. Body-envelope screening prunes irrelevant pairs while retaining the prior predicate. The unified runner treats skipped checks as incomplete validation.

This update reviewed workflow and diagnostic methods in `specs-to-pcb`, `circuit-synth` and `atopile` without adding their runtimes. The four bundled toolsets are unchanged. See [review decisions](references/32-adversarial-improvement.md).

| Area | Current capability |
|---|---|
| Requirements and component estimates | Organize functions, interfaces and assembly constraints, derive the BOM and query 立创商城 prices; separate consumption cost from actual purchases after MOQ and order increments |
| Compatible substitutions | Review each confirmed requirement, specifications, quantities, spares and quote changes; preserve functions and performance unless a reduction is explicitly accepted |
| Schematic drafting | Use freeform functional sections or sections within a sheet frame; inspect unwired placement before wiring, including bounds, text, pins and section layout |
| Guarded EDA operations | Move components on unwired pages with preflight, stepwise readback, save/reopen and guarded rollback; bind placement locks, allowed regions, keepouts and height rules |
| PCB geometry | Check outline closure, concave and slot edge clearances, spacing, repeated-number lands, plating and via spans; compare protected routing against baseline geometry |
| Manufacturing artwork | Inspect supported Gerber opening unions, offset and combined openings, and actual macro definitions; empty or unsupported scopes remain NOT_CHECKED |
| Acceptance evidence | Use the G0–G9 minimum check registry and bind checks to requirements, design baselines, actual input hashes and report hashes; changed designs invalidate old evidence |
| Data and recovery | Read summaries, pages and differences within output byte budgets; retain full source data, block unchanged retries and restore checkpoints within verified scope |

Price research is read-only. Design requests normally deliver reviewed PCB and manufacturing files for the user to order. Whole-board G0–G5 testing and the limits of native PCB writing/routing rollback are documented in the [fresh-session benchmark](references/28-fresh-session-benchmark.md).

## Bundled third-party tools

The complete package contains **four tool or methods packages**. This project owns design sequencing and acceptance criteria; these components provide EDA operations, format handling and independent inspection.

| Project | Bundled version / snapshot | Integration role |
|---|---|---|
| [easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) | 1.1.36 · `ccfaf28` | Official API documentation and a locally patched bridge runtime; default EasyEDA operations through Run API Gateway |
| [easyeda-enhanced-schematic-skill](https://github.com/easyeda/easyeda-enhanced-schematic-skill) | 1.2.0 · `0c4b9a0` | Official schematic recipes for functional sections, batch placement and selective net fanout; stored as `easyeda-schematic-net-fanout` |
| [easyeda-pro-format-skill](https://github.com/easyeda/easyeda-pro-format-skill) | 1.0.0 · `bee647f` | Official native-format definitions, examples and typed validation; native import and electrical connectivity remain separate checks |
| Adapted subset of [pcb-skill](https://github.com/daishuge/pcb-skill) | `6e939b6` | Community extraction, placement, physical connectivity, manufacturing and DSN/SES helpers; local fixes are recorded in `vendor/pcb-skill-toolkit/UPSTREAM.md` |

**Seven runtime dependencies** are also bundled: `ws 8.21.3`, `ajv 8.20.0`, `ajv-formats 2.1.1`, `fast-deep-equal 3.1.3`, `fast-uri 3.1.7`, `json-schema-traverse 1.0.0`, and `require-from-string 2.0.2`. The shipped bridge and format validator do not require `npm install`.

**External integrations:** [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) and [easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) are optional community backends. Their source, connectors and services are not bundled or installed automatically. Node.js, Python, the EasyEDA desktop client, Run API Gateway, NumPy and external autorouters must be supplied separately when needed.

See the [third-party inventory](THIRD_PARTY_NOTICES.md) for licenses, file locations, full source pins and local modifications. Versions above identify the snapshots retained in this repository.

## Installation

Download the [complete v1.8.0 package](https://github.com/Zero1683/PCB-Design-Skill/releases/download/v1.8.0/PCB-Design-Skill-v1.8.0.zip). To track development, clone the repository:

```sh
git clone https://github.com/Zero1683/PCB-Design-Skill.git pcb-design-to-bringup
```

Place the complete folder in your client's skill directory, or ask your agent to read [SKILL.md](SKILL.md). Keep `references/`, `assets/`, and `vendor/` with the entry file.

**Skill name:** `$pcb-design-to-bringup`

For an existing Git checkout, preserve local work and run `git pull --ff-only`. For ZIP installs, extract a fresh complete copy, point the skill installation to it and start a new conversation. Do not replace only `SKILL.md`. Versioned packages remain available under [Releases](https://github.com/Zero1683/PCB-Design-Skill/releases). Follow the [update guide](START_HERE.md#updating-an-existing-installation) for a running bridge.

### Connect EasyEDA

Install Node.js 18+, an extension-capable EasyEDA desktop client, and **Run API Gateway**. Enable the extension and start the bridge from this project directory:

```sh
node scripts/easyeda_bridge.mjs start
```

On Windows, run `start-easyeda.cmd`. The required `ws` dependency is bundled, so `npm install` is unnecessary. See [setup instructions](START_HERE.md) for configuration details.

| Status | Action |
|---|---|
| `BRIDGE_NOT_FOUND` | Start the bridge; check logs and occupied ports |
| `WAITING_FOR_EDA` | Open the desktop client and enable Gateway |
| `EDA_CONNECTED` | Verify the target window and project before operating |

Node.js, the desktop client, and Gateway require separate installation. Python 3.10+ is used for project initialization, file verification, and helper tests.

## Design workflow

Design requests finish with a reviewed, routed PCB and manufacturing files for the user to order. Component sourcing may include datasheet and stock checks; purchasing, carts, orders and payments require a separate request.

- **API first:** the bundled EasyEDA skill handles supported project/editing operations. UI interaction is limited to setup, visual inspection and specific unsupported operations.
- **Setup verification:** discover the skill, connect Gateway, then run the read-only API probe. A restart is a recovery option for stale discovery, not a mandatory installation step. macOS uses the same Node launcher.
- **Mixed routing:** plan critical power and sensitive routes, use native autorouting for suitable ordinary nets, preserve existing routes, and verify actual results.
- **Electrical review:** calculate power budgets, losses, DC path drop and simplified transient targets; use the actual stackup for controlled impedance. Request missing inputs or user-operated calculator results with exact fields and units.
- **Circuit reuse and revision checks:** record module interfaces and operating assumptions, check independent pin relationships against actual EDA exports, and list component/connection changes between revisions.
- **Evidence tools:** validate check records, compare normalized schematic/PCB/BOM exports, and screen component body envelopes. These tools supplement native DRC and visual review.

## EDA operation foundations

Official API Skill 1.1.36, schematic methods and official Format Skill 1.0.0 are bundled. Use the API for supported live operations and explicit document-type validation for native-source work. This project's workflow retains design sequencing, electrical review, drawing standards and delivery criteria.

The community easyeda-agent is an optional typed CLI/Connector backend. easyeda-mcp-pro remains external: the reviewed version uses a noncommercial license and is not included in this project's MIT code package. Neither backend is installed automatically. See [backend selection](references/16-easyeda-operation-backends.md) and [native-format operations](references/17-easyeda-native-format.md).

## Capabilities

| Module | Scope |
|---|---|
| Circuit design | Requirements, power budgets, part selection, pin assignment, and schematic review |
| Footprint verification | Exact-part datasheets, pad dimensions, pin numbering, and assembly orientation |
| PCB layout | Component clearance, critical loops, differential signals, return paths, and ground copper |
| Manufacturing | Gerber, BOM, placement, and stencil consistency checks; release baselines |
| Board bring-up | Unpowered measurements, current-limited power-up, reset, programming, and functional tests |
| EDA tools | Bundled EasyEDA API Skill 1.1.36, schematic enhancement methods 1.2.0, Format Skill 1.0.0, and bridge/validation runtime dependencies |

The engineering workflow also applies to other EDA tools through their native interfaces and checks.

## Independent PCB inspection tools

An adapted community toolkit adds native PCB extraction, body/escape-space
screening, physical connection assertions, Gerber/drill/mask checks and optional
DSN/SES routing utilities. Run `python scripts/pcb_toolkit.py --help`. Supply actual
project rules and layers; unsupported semantics and missing objects cannot pass.

The existing workflow and applicability remain unchanged. See [usage and coverage](references/18-pcb-inspection-toolkit.md).
Most tools require only Python 3.10+; raster and copper-clearance tools additionally
require NumPy, which is not bundled.

## Engineering constraints and calculations

Track critical sources, calculation conditions, native rules and export checks. Review dense escapes, return paths and thermal design, with reproducible mask opening/web, escape-channel and annular-ring arithmetic. See [engineering constraints](references/19-engineering-constraints.md).

## Schematic layout planning

Pack locally arranged functional blocks into a defined sheet using measured component and text bounds. Preserve internal positions and orientation, and produce fixed anchor targets, frames and title envelopes. Check source freshness before applying; compare observations after application and save/reload for position, property, pin and annotation changes. Supports the two schematic formats and unwired G2-A scopes; the selected backend performs native EDA operations. See the [layout execution guide](references/21-layout-execution.md).

## Reconciled data and operation recovery

Reconcile component/pin data across PCB models, query bounded summaries/pages and inspect deltas while retaining raw inputs locally. Complete closed-file projects can use isolated candidates with phase results and hash-guarded recovery that preserves the failed copy. Live recovery was tested for unwired schematic movement on test1; other operations require separate validation. See [usage](references/20-data-and-recovery.md).

## Batch preflight and repair feedback

Check the complete layout target before writing, then turn readback differences into reports containing objects, expected/actual values and scoped proposals. A persistent ledger blocks unchanged plan/adapter retries, detects repeated failures and bounds unsuccessful attempts. Pin/property drift requires investigation; post-reload failures prioritize persistence checks. This covers measured G2-A layouts and does not execute repairs or intercept arbitrary EDA APIs. See the [operation guide](references/22-batch-repair.md).

## Usage

### Design a new PCB

```text
Use $pcb-design-to-bringup to design a sensor board.
Use USB-C power and top-side components for stencil and hot-plate assembly.
Define the power architecture, parts, and interfaces, then create the schematic and PCB.
```

### Review an existing project

```text
Use $pcb-design-to-bringup to review the current PCB.
Focus on power loops, USB differential routing, footprints, and assembly clearance.
Keep the project read-only. Report locations, evidence, and suggested changes.
```

### Prepare for fabrication

```text
Use $pcb-design-to-bringup to review the manufacturing package.
Check Gerber, BOM, and placement files against the current project.
Review the outline, drilling, solder mask, and stencil, and list unresolved issues.
```

## Workflow

| Stage | Review focus |
|---|---|
| Requirements and parts | Power, mechanics, interfaces, cost, and assembly constraints |
| Schematics and footprints | Review unwired component placement, then connect; verify electrical design, readability, pins, and footprints |
| Placement and routing | Physical outlines, power loops, signal integrity, and connectivity |
| Fabrication and assembly | File revisions, process settings, orientation, and test points |
| Power-up and verification | Voltage, current, boot state, communication, and functional tests |

Record conditions, results, and open items at each stage. Verify footprints against manufacturer drawings and calculate impedance from the actual stackup and routing geometry. Read back and review API edits. Keep design checks and hardware test results separately.

## Documentation

| Document | Contents |
|---|---|
| [SKILL.md](SKILL.md) | Agent entry point, execution rules, and stage criteria |
| [Setup guide](START_HERE.md) | Environment setup, bridge startup, and connection diagnostics |
| [Circuits and footprints](references/02-circuit-and-library.md) | Parts, pins, and footprint verification |
| [Schematic drafting](references/12-schematic-drafting.md) | Functional blocks, two-stage drafting, wiring and annotations, visual reference, and acceptance evidence |
| [Circuit intent and reuse](references/13-circuit-intent-and-reuse.md) | Pin relationship checks, module assumptions, revision differences, and native readback |
| [Placement and routing](references/03-layout-routing.md) | Layout, critical nets, and ground copper |
| [Manufacturing and assembly](references/04-release-assembly.md) | Release files, stencils, and soldering |
| [Board bring-up](references/05-bringup-debug.md) | Power-up, measurements, and fault isolation |
| [EDA operations](references/06-easyeda-execution.md) | API calls, units, state, and result checks |
| [Schematic methods](references/15-easyeda-schematic-methods.md) | Block drawing, batch placement, selective fanout, compatibility probes, and revision cleanup |
| [Project templates](assets/) | PROJECT, CHECKS, and HANDOFF |
| [Electrical analysis](references/09-electrical-analysis.md) | Power, voltage drop, transient budgets, and impedance handoff |
| [Validation tools](references/10-validation-tools.md) | Evidence and normalized export contracts |
| [Validation scenarios](references/11-validation-scenarios.md) | Behavioral evaluation and live EDA acceptance |
| [Operation backends](references/16-easyeda-operation-backends.md) | Official API and optional backend selection and handoff |
| [Native formats](references/17-easyeda-native-format.md) | Native input, typed validation and import limits |
| [PCB inspection](references/18-pcb-inspection-toolkit.md) | Inspection commands, coverage and unsupported geometry |
| [Engineering constraints](references/19-engineering-constraints.md) | Manufacturer sources and electrical/fabrication calculations |
| [Data and recovery](references/20-data-and-recovery.md) | Model reconciliation, paged reads and checkpoint recovery |
| [Layout execution](references/21-layout-execution.md) | Measured block planning and post-write comparison |
| [Batch preflight](references/22-batch-repair.md) | Batch checks, differences and bounded retries |
| [Live writes](references/23-live-eda.md) | Native movement, readback, persistence and guarded recovery |
| [Executable constraints](references/24-executable-constraints.md) | Placement, region, keepout and height rules |
| [Requirement coverage](references/25-requirement-coverage.md) | Requirement, check and evidence mappings |
| [Component cost planning](references/26-component-cost-planning.md) | Component quotes, MOQ and compatible substitutions |
| [Current-design evidence](references/27-current-design-evidence.md) | Design baselines, source hashes and report bindings |
| [Fresh-session benchmark](references/28-fresh-session-benchmark.md) | Whole-board testing in a fresh task and result records |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | Sources, licenses, pins and local modifications |

The core skill and engineering references are in English. Project records have English and Chinese templates; replies follow the user’s language. Integration corrections to upstream material are listed in the third-party notices.

<details>
<summary><strong>Helper commands and runtime configuration</strong></summary>

Query connection status:

```sh
node scripts/easyeda_bridge.mjs status
node scripts/easyeda_bridge.mjs doctor
```

The bridge listens on `127.0.0.1`, using an available port from `49620` to `49629`. Logs default to `.runtime/`; set `PCB_SKILL_STATE_DIR` to use another writable directory. Keep bridge access local to the machine.

Initialize records in a directory that does not yet exist:

```sh
python scripts/init_project.py --output /path/to/new-project --name MyPCB --lang en
```

Run helper tests using an existing writable directory:

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/workdir
```

Verify a freshly extracted Release ZIP:

```sh
python -X utf8 scripts/release_manifest.py verify --root /path/to/pcb-design-to-bringup
```

Verification checks SHA-256 hashes, missing files, and extra files. Use a separate archive extraction so `.git/` and `.runtime/` are not reported as additional content.

</details>

## Validation status

The latest software run on 2026-09-22 passed **356 regression cases**, plus **17 toolkit self-test commands with no skips**. The total includes 40 routing-physics, 45 mask-geometry and 17 physical-assertion/entry cases. Mask tests contain 1,000 generated comparisons against independent mathematical oracles. Four additional defects found by independent CLI review were corrected and independently rechecked.

| Evidence level | Current status |
|---|---|
| Scripts and synthetic data | Geometry, report binding, gates, costing, substitution and recovery regressions passed; native-runtime mock tests are included |
| Native EDA integration | test1 covered unwired schematic movement, collision/bounds rejection, save/reopen, scoped repair and restoration |
| Pending benchmarks | A fresh-session whole-board G0–G5 run, the full macOS workflow, external-router interoperability and physical manufacturing after these changes |

Native PCB writing and routing rollback are not implemented. Actual pours, drill-void subtraction, some native hole encodings and parameterized Gerber macros remain outside supported inspection scope. See the [inspection guide](references/18-pcb-inspection-toolkit.md). Script success applies only to measured coverage; whole-board handoff still requires native checks and engineering acceptance.

Detailed evidence and historical results are retained in [VALIDATION.md](VALIDATION.md).

## Contributing

Report problems through [Issues](https://github.com/Zero1683/PCB-Design-Skill/issues), or submit a pull request for workflow, documentation, or tool integration improvements. Include software versions, reproduction steps, and sanitized logs. For hardware reports, include part numbers, board revision, and measurement conditions.

## License

Original workflow content, templates, and scripts use the [MIT License](LICENSE). Bundled components retain their original notices and licenses. See [third-party notices](THIRD_PARTY_NOTICES.md).
