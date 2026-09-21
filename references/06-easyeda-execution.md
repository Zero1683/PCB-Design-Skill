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
