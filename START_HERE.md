# Getting Started

This package includes the PCB workflow skill, the complete documentation for EasyEDA API Skill 1.1.36, the bridge service, and its ws runtime dependency. The schematic enhancement methods, native-format validator and adapted PCB inspection toolkit are also bundled. Their versions, runtime packages and original notices are listed in [the third-party inventory](THIRD_PARTY_NOTICES.md). No separate prerequisite skill installation, npm install, or documentation generation is required.

## Updating an existing installation

Use the [v1.8.0 Release](https://github.com/Zero1683/PCB-Design-Skill/releases/tag/v1.8.0)
for this update. The repository's `main` branch tracks subsequent development.
Release downloads remain tied to their tags. In a Git checkout, preserve
local modifications and run `git pull --ff-only`. For a ZIP installation, extract
into a fresh directory and register that complete folder; do not replace only
SKILL.md or mix files from different package revisions. Preserve project work and
local runtime configuration outside the replacement folder.

Verify a fresh extraction with `python -X utf8 scripts/release_manifest.py verify --root <extracted-folder>` before generating runtime files. Start a new agent
conversation using the updated skill. If a bridge is already running, finish
active operations and follow the bridge-specific update instructions below.
A new conversation alone does not reload the bridge process.

## First Use

1. Install the full package as **one skill**, including `vendor/easyeda-api/`, `vendor/easyeda-schematic-net-fanout/`, `vendor/easyeda-pro-format-skill/` and `vendor/pcb-skill-toolkit/`. No second prerequisite skill is required. Extract the entire folder to your working drive and preserve its directory structure. On Windows, D: is recommended; paths may contain Chinese characters and spaces.
2. Install Node.js 18 or later and an EasyEDA desktop client that supports extensions if they are not already available. This package does not include a Node.js installer or the EDA client.
3. Install and enable the **Run API Gateway** extension in EasyEDA. The upstream package does not include an `.eext` file, and this package does not supply a fabricated substitute. Search for the extension by name in the client's extension marketplace. The upstream URL is https://jlc-ext.com/item/oshwhub/run-api-gateway .
4. On Windows, double-click `start-easyeda.cmd`. On other systems or in an agent terminal, run `node scripts/easyeda_bridge.mjs start` with this folder as the working directory.
5. `EDA_CONNECTED` means connected. `WAITING_FOR_EDA` means the bridge has started; open the client and enable the extension. `BRIDGE_NOT_FOUND` means the service was not found; check the reported log path and whether the port is occupied.
6. Register this folder in an AI tool that supports skills, then invoke `$pcb-design-to-bringup`. Alternatively, ask the agent to read this folder's `SKILL.md`. Do not load another external copy of easyeda-api.

## Native-format validation and optional backends

The official native-format skill and its locked validation dependencies are
bundled at `vendor/easyeda-pro-format-skill/`. Use the file-input wrapper described
in [reference 17](references/17-easyeda-native-format.md); no npm install is needed.
It checks a typed primitive, not a complete project or manufacturing readiness.

The community easyeda-agent CLI/Connector and easyeda-mcp-pro are optional external
backends. They are not installed by the main package. Read [backend selection](references/16-easyeda-operation-backends.md)
before choosing one, including versions, connector pairing and licensing. Keep
the default API path unless an operation benefits from a verified alternative.

## Included operation layers

The main skill loads the API reference and bridge for EasyEDA operations, then
[schematic methods](references/15-easyeda-schematic-methods.md) when drawing or
revising schematics. The methods adapt the upstream enhancement recipes while
retaining placement-before-wiring, the two supported drawing formats and native
verification. Keep the entire vendor directory; there is no second installation
or extra bridge to start.

## macOS and skill discovery

Use the same complete folder on macOS. For example, place it at `~/.agents/skills/pcb-design-to-bringup` (or link a folder on your chosen working drive there), then open Terminal in that folder:

```sh
node scripts/easyeda_bridge.mjs status
node scripts/easyeda_bridge.mjs start
```

Run `start` only when no bridge is available. After enabling Gateway, use the actual port and window ID printed by status:

```sh
node scripts/eda_probe.mjs <port> <windowId>
```

`API_RESPONDED` confirms a read-only call worked. A null project is normal before creating one. It does not verify editing or autorouting. Proceed with the bundled API workflow, not a sequence of UI clicks merely because Gateway installation required the UI.

Codex normally detects newly installed skills automatically. If the skill does not appear, check the folder and explicitly read its `SKILL.md`; restart Codex only if discovery remains stale. Restart EasyEDA only when the extension/client requests it or a diagnosed connection problem requires it, after saving open work. These are separate applications and separate checks. See [official skill discovery guidance](https://learn.chatgpt.com/docs/build-skills).

A design request normally ends with the reviewed PCB/manufacturing package for the user to order. It does not authorize component purchasing or supplier checkout.

## Status and Runtime Files

`node scripts/easyeda_bridge.mjs status` queries status without starting a service. `doctor` also reports the Node version, service port, connection state, and window state. The launcher listens only on the local machine, reuses an existing bridge, and does not terminate user services, select a project, or modify the PCB.

Runtime logs are stored in this package's `.runtime/` directory by default. Set `PCB_SKILL_STATE_DIR` to a writable directory on your working drive if needed; set it when the package directory is read-only. Verify the release package before its first run, or store runtime state outside the package so generated logs are not reported as extra files.

See [EDA execution](references/06-easyeda-execution.md) for the full tool workflow and [third-party notices](THIRD_PARTY_NOTICES.md) for provenance. Python 3.10+ runs the project-record, inspection and release-verification helpers;
it is not required to start the bridge. The bundled PCB toolkit's raster and copper
clearance tools additionally need NumPy in the same Python environment; other
tools are standard-library based. NumPy and an external autorouter are not bundled.
See [inspection tools](references/18-pcb-inspection-toolkit.md) for scoped use.

## Updating an already running bridge

Updating files does not reload a running Node process. `status` reports `bridgeUpdateRecommended` if an existing service lacks this package's integration revision. Finish active EDA operations and preserve open work, then restart only the identified bridge from the updated package. The launcher does not terminate existing services automatically. Restarting Codex alone does not reload a detached bridge.
