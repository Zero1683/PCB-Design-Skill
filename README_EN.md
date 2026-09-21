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

<p align="center"><a href="#installation">Installation</a> · <a href="#capabilities">Capabilities</a> · <a href="#usage">Usage</a> · <a href="#documentation">Documentation</a></p>
<p align="center"><a href="README.md">简体中文</a> · <strong>English</strong></p>

---

Turn hardware requirements into circuit designs, PCB projects, and manufacturing files, with procedures for footprint verification, layout review, and board bring-up. Bundled EasyEDA API documentation, a local bridge, and runtime dependencies support live operations in the EasyEDA desktop client.

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

## Capabilities

| Module | Scope |
|---|---|
| Circuit design | Requirements, power budgets, part selection, pin assignment, and schematic review |
| Footprint verification | Exact-part datasheets, pad dimensions, pin numbering, and assembly orientation |
| PCB layout | Component clearance, critical loops, differential signals, return paths, and ground copper |
| Manufacturing | Gerber, BOM, placement, and stencil consistency checks; release baselines |
| Board bring-up | Unpowered measurements, current-limited power-up, reset, programming, and functional tests |
| EDA tools | Bundled EasyEDA API Skill 1.1.28, bridge server, references, and `ws` dependency |

The engineering workflow also applies to other EDA tools through their native interfaces and checks.

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
| Schematics and footprints | Connections, component ratings, pin mapping, and dimensions |
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
| [Placement and routing](references/03-layout-routing.md) | Layout, critical nets, and ground copper |
| [Manufacturing and assembly](references/04-release-assembly.md) | Release files, stencils, and soldering |
| [Board bring-up](references/05-bringup-debug.md) | Power-up, measurements, and fault isolation |
| [EDA operations](references/06-easyeda-execution.md) | API calls, units, state, and result checks |
| [Project templates](assets/) | PROJECT, CHECKS, and HANDOFF |

Engineering references are primarily in Chinese. Upstream API documentation retains its original language.

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
python scripts/init_project.py --output /path/to/new-project --name MyPCB
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

Release testing covered independent extraction, paths containing Chinese characters and spaces, dependency loading, bridge startup, and repeated starts. All 11 helper tests passed. The bridge was verified through `WAITING_FOR_EDA`; the full workflow with a connected EDA client remains untested. Each PCB project requires its own electrical review and hardware acceptance tests.

## Contributing

Report problems through [Issues](https://github.com/Zero1683/PCB-Design-Skill/issues), or submit a pull request for workflow, documentation, or tool integration improvements. Include software versions, reproduction steps, and sanitized logs. For hardware reports, include part numbers, board revision, and measurement conditions.

## License

Original workflow content, templates, and scripts use the [MIT License](LICENSE). Bundled components retain their original notices and licenses. See [third-party notices](THIRD_PARTY_NOTICES.md).
