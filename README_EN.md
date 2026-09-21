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

<p align="center"><a href="#recent-updates">Recent updates</a> · <a href="#installation">Installation</a> · <a href="#capabilities">Capabilities</a> · <a href="#usage">Usage</a> · <a href="#documentation">Documentation</a></p>
<p align="center"><a href="README.md">简体中文</a> · <strong>English</strong></p>

---

Turn hardware requirements into circuit designs, PCB projects, and manufacturing files, with procedures for footprint verification, layout review, and board bring-up. Bundled EasyEDA API documentation, schematic methods, a local bridge, and runtime dependencies support live operations in the EasyEDA desktop client. The API layer supplies operation interfaces; the methods library covers functional blocks, batch placement, selective net fanout, and revision cleanup.

## Recent updates

Recent work covers schematic drafting, EDA operations, independent inspection and recovery. **v1.5.2 adds layout batch preflight, structured repair reports and retry control, alongside data reconciliation, layout planning and operation recovery.** Download the complete release package or clone the repository.

| Area | Additions |
|---|---|
| Schematic drafting | Two supported formats: freeform functional sections or sections within a sheet frame. Review unwired placement before connecting components; apply boundary, text-spacing and common layout fixes; add measured block planning and post-apply comparison |
| EDA operations | Bundled official API, schematic methods, native-format documentation and validation dependencies; batch placement, net fanout and explicit backend selection |
| PCB and manufacturing inspection | Supported native extraction, component-clearance and escape-space screening, Gerber/drill/mask checks, and DSN/SES routing helpers |
| Electrical and fabrication calculations | Associate manufacturer sources, calculation conditions, native rules and export checks with one revision; expand power, return-path, thermal, escape-channel, mask-web and annular-ring checks |
| Data access | Reconcile components and pin nets across two PCB models; provide summaries, paged queries and revision deltas while retaining full inputs and rejecting missing or conflicting records |
| Operation recovery | Checkpoints and isolated candidates for complete closed-file projects; preserve failed work and restore the candidate. Changed accepted files or evidence produce a `STALE` status |

See the [operation guide](references/20-data-and-recovery.md) for commands, examples and scope, the [changelog](CHANGELOG.md) for changes, and [validation records](VALIDATION.md) for test results. Live EDA rollback is not implemented; token savings have not been benchmarked.

## Installation

Download the [latest release](https://github.com/Zero1683/PCB-Design-Skill/releases), or clone the repository:

```sh
git clone https://github.com/Zero1683/PCB-Design-Skill.git pcb-design-to-bringup
```

Place the complete folder in your client's skill directory, or ask your agent to read [SKILL.md](SKILL.md). Keep `references/`, `assets/`, and `vendor/` with the entry file.

**Skill name:** `$pcb-design-to-bringup`

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

Reconcile component/pin data across PCB models, query bounded summaries/pages and inspect deltas while retaining raw inputs locally. Complete closed-file projects can use isolated candidates with phase results and hash-guarded recovery that preserves the failed copy. Live EDA rollback needs separate validation. See [usage](references/20-data-and-recovery.md).

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

For v1.5.2, all 11 new batch/repair cases and reruns of 27 data/recovery plus 14 layout cases passed: 52 total. These use offline synthetic data and local files.

All 14 new synthetic layout tests passed, covering bounds, obstacles, stale plans and readback changes. Live EDA save/reload integration has not been tested.

The v1.5.0 release rerun includes 81 Python cases: 80 passed and one was skipped because Windows denied symbolic-link creation. All 8 Node format cases and isolated simulated bridge checks passed. Integration-time results for 21 toolkit self-tests are listed in [validation records](VALIDATION.md).

These tests cover scripts and synthetic data. The new toolchain has not completed live EDA end-to-end, macOS, external-router interoperability or physical manufacturing validation. Native extraction has format limits; the new adapter reconciles toolkit board data and normalized snapshots under one baseline, with real-project validation still pending. Helpers do not replace an impedance solver or physical acceptance.

In v1.5.1, all 27 new data/recovery tests passed, along with a rerun of 21 PCB toolkit tests and the importer self-test. These results are separate from the v1.5.0 counts above.

See the [changelog](CHANGELOG.md) for the complete update.

## Contributing

Report problems through [Issues](https://github.com/Zero1683/PCB-Design-Skill/issues), or submit a pull request for workflow, documentation, or tool integration improvements. Include software versions, reproduction steps, and sanitized logs. For hardware reports, include part numbers, board revision, and measurement conditions.

## License

Original workflow content, templates, and scripts use the [MIT License](LICENSE). Bundled components retain their original notices and licenses. See [third-party notices](THIRD_PARTY_NOTICES.md).
