# Getting Started

This package includes the PCB workflow skill, the complete documentation for EasyEDA API Skill 1.1.28, the bridge service, and its ws runtime dependency. No separate easyeda-api skill installation, npm install, or documentation generation is required.

## First Use

1. Extract the entire folder to your working drive and preserve its directory structure. On Windows, D: is recommended; paths may contain Chinese characters and spaces.
2. Install Node.js 18 or later and an EasyEDA desktop client that supports extensions if they are not already available. This package does not include a Node.js installer or the EDA client.
3. Install and enable the **Run API Gateway** extension in EasyEDA. The upstream package does not include an `.eext` file, and this package does not supply a fabricated substitute. Search for the extension by name in the client's extension marketplace. The upstream URL is https://jlc-ext.com/item/oshwhub/run-api-gateway .
4. On Windows, double-click `start-easyeda.cmd`. On other systems or in an agent terminal, run `node scripts/easyeda_bridge.mjs start` with this folder as the working directory.
5. `EDA_CONNECTED` means connected. `WAITING_FOR_EDA` means the bridge has started; open the client and enable the extension. `BRIDGE_NOT_FOUND` means the service was not found; check the reported log path and whether the port is occupied.
6. Register this folder in an AI tool that supports skills, then invoke `$pcb-design-to-bringup`. Alternatively, ask the agent to read this folder's `SKILL.md`. Do not load another external copy of easyeda-api.

## Status and Runtime Files

`node scripts/easyeda_bridge.mjs status` queries status without starting a service. `doctor` also reports the Node version, service port, connection state, and window state. The launcher listens only on the local machine, reuses an existing bridge, and does not terminate user services, select a project, or modify the PCB.

Runtime logs are stored in this package's `.runtime/` directory by default. Set `PCB_SKILL_STATE_DIR` to a writable directory on your working drive if needed; set it when the package directory is read-only. Verify the release package before its first run, or store runtime state outside the package so generated logs are not reported as extra files.

See [EDA execution](references/06-easyeda-execution.md) for the full tool workflow and [third-party notices](THIRD_PARTY_NOTICES.md) for provenance. Python is used only by the project-record and release-verification helpers; it is not required to start the bridge.
