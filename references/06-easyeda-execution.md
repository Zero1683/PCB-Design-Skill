# Tool integration: EasyEDA and other environments

The complete EasyEDA API Skill, bridge implementation, and ws runtime dependency are bundled. Resolve paths relative to this skill's root; do not depend on installation directories on the author's machine. Do not copy old project document IDs, ports, or unverified API signatures.

## EasyEDA

Read the bundled [easyeda-api/SKILL.md](../vendor/easyeda-api/SKILL.md), then use its index to load the API classes, interfaces, enums, or format references needed for the current operation. Tool documentation defines accurate calls; this skill defines engineering checks and delivery criteria. A missing external easyeda-api installation is not a blocker because the package is bundled.

Integrated startup conventions:

1. From this skill's root, run `node scripts/easyeda_bridge.mjs status`. If a connection is needed and no bridge exists, run `node scripts/easyeda_bridge.mjs start`. Windows users may double-click `start-easyeda.cmd`.
2. Do not run `npm install` or the upstream README's documentation build. ws and generated references are already present. Node.js 18+ and the EasyEDA desktop client remain external prerequisites. See [setup](../START_HERE.md).
3. Interpret upstream `$CLAUDE_SKILL_DIR` as the absolute path to this package's `vendor/easyeda-api`; do not modify global user environment variables. This package's cross-platform Node launcher replaces upstream shell startup examples. Other API semantics remain as documented upstream.
4. The launcher verifies service ID `easyeda-bridge` and reports the actual port and windows; do not assume port 49620. `WAITING_FOR_EDA` means the user should enable Run API Gateway in the desktop client, not that another bridge must be started.
5. With multiple services/windows, identify the target from the task. Explicitly use the selected service and `windowId` in later calls rather than relying on the active-window default. Connection alone does not identify the intended project.

## Schematic operating methods

For schematic creation or revision, read [schematic methods](15-easyeda-schematic-methods.md) alongside the relevant API classes. It adapts the bundled [enhancement recipes](../vendor/easyeda-schematic-net-fanout/SKILL.md) for block layout, batch placement, selective labels, partial-failure recovery and protected edits. Use one shared bridge and the same selected window/document. Follow the adapter before upstream examples: exact-part mapping, measured geometry, G2-A before G2-B, and native acceptance remain required. Upstream recipes are supplementary operating guidance, not a second governing workflow or a complete layout/electrical checker.

## Installation completion and routing to tools

The main skill, `vendor/easyeda-api` and `vendor/easyeda-schematic-net-fanout` ship together. Read the vendor entrypoint directly by path; nested discovery as a second installed skill is unnecessary. Missing discovery is not evidence that computer use is the only tool.

Separate three states:

1. **Skill discovered:** if absent from Codex's skill list, first check the complete folder and registration path. Explicitly read `SKILL.md` and its bundled API entrypoint to continue. Codex normally detects skill changes automatically; restart Codex only if discovery still does not update. Do not restart or terminate an active task yourself. Save a short resumption instruction first.
2. **Bridge healthy:** run `status`, or `start` if absent. `WAITING_FOR_EDA` needs the Gateway extension, not repeated bridge launches or Codex restarts.
3. **API responsive:** after enabling Gateway, select the reported port/window and run `node scripts/eda_probe.mjs <port> <windowId>`. A reply with no current project is valid before creating one. Check project/document identity before editing. An `EDA_CONNECTED` label alone is insufficient.

If the extension itself requests an EDA restart, have the user save work and restart that client, then rerun status and the probe. Do not prescribe an unconditional Codex or EDA restart. Mac users run the same Node commands in Terminal; `.cmd` is Windows-only. A macOS permission dialog or unsupported extension version is a setup issue, not permission to abandon the API workflow silently.

On package upgrades, inspect `bridgeUpdateRecommended`: existing Node services retain their old code until restarted. Finish active operations and preserve work before restarting the identified bridge; do not kill unrelated processes. Restarting Codex is not a bridge upgrade.

Official Codex discovery reference: [Build skills](https://learn.chatgpt.com/docs/build-skills), checked 2026-09-21.

## Project creation and permitted UI fallback

| Operation | Preferred route | When UI is appropriate |
|---|---|---|
| Install client/Gateway, login | Existing installer/extension workflow | Setup UI and login interaction |
| Discover service/project | Launcher, read-only probe, documented getters | Inspect a connection/permission dialog |
| Create/open project | `eda.dmt_Project.createProject`, `getProjectInfo`, `openProject` | Specific unsupported, failed, or beta-restricted operation |
| Add/edit schematic/PCB | Document-specific APIs after identity checks | A documented gap or verified error |
| Route ordinary nets | Native autorouter via API when supported | Native autorouter UI when API cannot be used |
| Visual/manufacturing preview | Export API plus viewer | Inspect rendered geometry and dialogs |
| Ordering/procurement | Deliver files and settings to user | Only if the user explicitly requests ordering work |

Read [DMT_Project](../vendor/easyeda-api/references/classes/DMT_Project.md) for exact arguments. `createProject` returns a UUID or `undefined`; use that UUID with `getProjectInfo` and `openProject`, not a filesystem path. Check existing projects after a timeout before repeating creation. The bundled document marks creation **beta** and warns against production use: validate in a disposable test project first; if the installed client's restriction applies, use the UI for that step and resume API editing afterward. Do not claim method presence proves support for writes.

`openProject` is documented to discard unsaved changes in the previously opened project. Preserve authorized work before switching; if saving unrelated work is outside scope, have its owner save it rather than silently losing it. Use the documented project/document creation APIs for the installed version, then read back actual IDs; do not invent empty-board helper calls.

For a UI fallback, state the operation, observed API limitation/error, and return condition briefly. Capture the resulting project identity through the API afterward. Do not use a fallback as permission for unrelated websites, checkout, account changes, or purchasing.

Operational procedure:

Read-only tasks skip writes, repours, saves, and record initialization. If a check automatically writes locks, caches, or reports, use read-only exports or in-memory analysis instead. Use an isolated working copy only when creating one is allowed, and state its relationship to the original.

1. Check bridge health against current tool documentation. Verify service identity and distinguish absent service, disconnected desktop, and wrong window/document.
2. Verify project, window, document type, and identifier. Ask which target when multiple windows cannot be resolved from scope; never edit another open board by accident.
3. Read schematics/PCB, components, footprints, nets, and rules. Save a pre-edit snapshot for authorized edits.
4. Check exact signatures, units, rotation/mirroring, and return shapes for the operation. Prefer official APIs; source-file changes require current format documentation.
5. Work in small batches and inspect results. Reread objects and verify actual values, component counts, and net names.
6. Rebuild pours as needed, run relevant checks, inspect the actual view, and save.
7. Export the post-edit snapshot and differences, retaining a rollback path.

HTTP 200 alone is not success: payloads may be null, wrapped errors, or incomplete asynchronous work. After a timeout, read the result before retrying to avoid duplicate traces, parts, vias, or copper regions. Stop repeating after three identical errors without new evidence; investigate documentation, permissions, and connection rather than retrying indefinitely.

## Data and coordinates

- Verify mm, mil, or internal units; origin and Y-axis direction; local-footprint to board transforms; rotation and bottom-side mirroring.
- Resolve layer IDs from current enums rather than treating old numeric IDs as cross-tool constants.
- Footprints may contain multiple pads with the same number. Preserve each physical instance while correctly mapping electrical pins.
- Source documents may include history, deletion markers, and multiple versions of one ID. Read final effective state rather than treating all records as existing primitives.
- Direct source editing is a high-impact operation: preserve a baseline, check parsing round trips, make the smallest required changes, reopen, and run DRC. Do not globally replace net names or pin numbers as raw strings.

## Screenshots

Use screenshots to check geometry, orientation, silkscreen, and visible anomalies. They do not prove hidden net names, full-project connectivity, or actual impedance. Preserve needed whole-board views and critical power/USB/fine-pitch details.

Inspect the first placement visually for widespread overlap and outline errors before continuing routing. Do not leave first inspection to the user. Already authorized design work does not require approval at each step; a request to review without changes immediately switches the task to read-only.

## Other EDA tools or unavailable live access

Use native projects, DRC, exports, and scripting in KiCad, Altium, or other tools with the same checks. Do not report PASS for formats the available scripts cannot parse.

With images alone, assess visible layout and annotations and list outstanding checks; do not claim pin-by-pin connectivity, completed repours, or a correct manufacturing package. Gerbers support manufacturing-geometry review but cannot fully recover symbols, component parameters, or schematic intent.

Without an available EDA tool, continue requirements, architecture, pin tables, candidate BOM, critical electrical/footprint evidence, and manufacturing constraints. Report exact missing deliverables rather than fabricating a saved PCB file.

A disconnected bridge does not authorize resetting projects, terminating unrelated processes, or deleting projects. Background startup and storage must follow the current environment's requirements.

## Schematic attribute coordinate probe

Before bulk edits to pin attributes or NC markers, test one documented operation and inspect it after save/reopen. Component-local, API and serialized source positions may use different origins and Y directions. A negative coordinate alone is not corruption. Do not apply a sign flip or global translation without a verified transform and parent relationship. Preserve pin identities and the pre-edit netlist; restore a failed probe before trying another method. Follow the bounded repair procedure in reference 12.

## One-object persistence probe before bulk mutation

For an unverified API method/client-version combination involving component properties, symbol attributes, coordinates or import/synchronization, first back up and test one representative object. Read exact method semantics: a replacement-style setter may erase unspecified fields. Capture the full relevant pre-state, make the smallest documented edit, read back, save, reopen the document, then compare:

- Requested field/position and native rendered result.
- Stable object ID, designator, part/MPN, supplier code, footprint, value, fitted/BOM status and pin-net mapping where applicable.
- For geometrical edits, units, parent transform, orientation, layer and association with the correct object.

Proceed in small batches only if the intended change persisted and unrelated protected fields stayed unchanged. Reread after each batch. A missing field, wrong object type, document switch or unexpected diff fails the operation; restore the affected object/snapshot and diagnose before retrying. Do not blindly fill missing fields from a stale snapshot after the user has edited the design. Avoid whole-source replacement for a local attribute if a verified narrow method exists. Direct source repair still needs current format documentation, parse/round-trip checks and connectivity comparison.

Import/synchronization success may mean a confirmation dialog opened, not that changes were applied. Complete the native confirmation within authorized scope, then verify imported object identities and pin nets. Export calls may depend on the active editor: activate the exact document, verify project/document/type immediately before exporting, and inspect the returned content, not only its filename. After reconnect or project opening rediscover window/document IDs rather than reusing stale ones.

Record probe evidence once per relevant version/operation and reuse it while those conditions remain unchanged. Do not repeat the entire capability discovery for each component. A timeout requires readback before retry; do not create duplicates.
