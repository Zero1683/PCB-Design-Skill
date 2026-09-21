---
name: pcb-design-to-bringup
description: Design manufacturable, assembleable, and testable PCBs from hardware requirements. Covers component selection, schematics, footprint verification, placement and routing, manufacturing handoff, and hardware acceptance. Use for new designs, board reviews and rework, fabrication preparation, and first-board bring-up. Includes staged verification records and project handoff templates. Supports EasyEDA and workflows in other EDA tools. Not for firmware-only changes or enclosure modeling.
---

# PCB Design to Bring-up

EasyEDA API Skill 1.1.28, API and source-format documentation, the bridge server, and the ws runtime dependency are bundled. No separate easyeda-api installation is required. See [setup](START_HERE.md) and follow [EDA operations](references/06-easyeda-execution.md) to load the relevant tool documentation and start the bridge. The target machine still needs Node.js, the EDA desktop client, and its Gateway extension. Do not start a service for workflow advice or file-only review.

Deliver designs that can be manufactured, assembled, measured, and maintained. Resolve known issues before the first prototype, but do not promise first-pass success or describe an unbuilt design as a mature product.

## Language

Use the user's language for conversation, explanations, and generated project records unless they request otherwise. Keep API names, commands, file paths, identifiers, status values, and template placeholders unchanged. English instructions do not require English replies.

## Starting a task

1. Identify the mode: new design, read-only review, local revision, manufacturing preparation, assembly guidance, or hardware troubleshooting. Resume existing projects at the relevant stage without repeating valid completed work.
2. Read project rules and any `PROJECT.md`, `HANDOFF.md`, and `CHECKS.csv`. Verify the actual project, release revision, and physical board ID. Historical text, screenshots, and files sent to fabrication may describe different revisions.
3. Read [requirements and context recovery](references/01-intake-and-recovery.md). Extract confirmed parameters first. Ask only for missing information that affects architecture, interfaces, or manufacturing outcomes; do not reconfirm settled requirements.
4. For tasks permitting writes, save new work in the authorized directory and follow storage preferences. Use `scripts/init_project.py` to initialize templates without overwriting files, or copy them manually if Python is unavailable. For read-only reviews, report in the conversation by default; do not initialize or update project records, and use access methods that leave the original project unchanged.
5. Load references for the relevant stage below. For live EasyEDA work, also read [EDA operations](references/06-easyeda-execution.md). Do not start unrelated services.

## Execution constraints

- Record the user's dimensions, assembly side, retained parts, read-only scope, budget, and available tools. Case values such as 24 x 70 mm, two layers, 1.6 mm, 1 oz, 0603, ESP32-C3, and COM30 are not universal defaults.
- Perform backups, reads, checks, and edits within existing authorization without adding approval gates at every stage. Prepare a concrete proposal for component, outline, interface, or functional changes outside that scope. Ordering, payment, and public release require the corresponding authorization.
- Treat “do not change it yet” as read-only. Later permission to modify one area extends scope only to that area. Record other issues without silently modifying the whole board.
- Read the datasheet for the exact manufacturer, part number, and package suffix before connecting the circuit. Bare chips, modules, and similarly named compatible parts do not share pinouts or ratings by assumption.
- Verify dimensions using evidence rather than library defaults, custom footprints, recommended-part labels, or 3D appearance. List actual changes before replacement; do not standardize blindly to remove property warnings.
- Check rotated physical pads and component outlines, assembly clearance, connector access, and silkscreen identification. Center coordinates or zero DRC errors do not establish absence of overlap.
- Mark unmeasured geometry as assumed. Evaluate power-trace widths, differential impedance, and return-path conditions against the actual stackup and current. Average copper clearance cannot validate a nonuniform route.
- Read back every change, rebuild affected copper pours, and repeat affected checks. API success does not establish a successful edit. If edits fail or results are abnormal, stop adding operations, read the state, and decide whether to retry or roll back.
- Provide accessible test paths for hidden joints, boot pins, and debug interfaces. Draw manual-assembly orientation and pin order explicitly.
- Every passed check needs its revision, conditions, method, and result. Distinguish untested items, unsupported checks, and accepted limitations; do not relabel them PASS.

## Stages and exit criteria

Apply stages relevant to the authorized scope. These are engineering criteria, not additional approval procedures.

| Stage | Required outcome | Reference |
|---|---|---|
| G0 Requirements and baseline | Functions, power, mechanics, assembly, manufacturing constraints, unknowns, and authoritative revision identified | [01](references/01-intake-and-recovery.md) |
| G1 Architecture and parts | Power states, budgets, pin assignment, procurable parts, and datasheet sources | [02](references/02-circuit-and-library.md) |
| G2 Schematics and footprints | Pin-by-pin checks, critical footprint dimensions, ERC/DRC disposition, and consistent BOM | [02](references/02-circuit-and-library.md) |
| G3 Placement | Mechanical and physical envelopes clear, critical routes feasible, manual assembly unambiguous | [03](references/03-layout-routing.md) |
| G4 Routing and ground | Appropriate power paths, critical interfaces, and returns; final copper readback and complete connectivity evidence | [03](references/03-layout-routing.md) |
| G5 Manufacturing release | Frozen snapshot, independent manufacturing-file preview, consistent BOM/placement/stencil, disclosed limitations | [04](references/04-release-assembly.md) |
| G6 Assembly and unpowered checks | Correct paste print, orientation, and checks after cooling; traceable board identity and unpowered measurements | [04](references/04-release-assembly.md) |
| G7 Current-limited power-up and programming | Measured power, reset, boot, logic compatibility, and at least one recovery programming path | [05](references/05-bringup-debug.md) |
| G8 Functional and boundary tests | Required sensor/interface/load/cold-start tests completed; failures and reduced functionality documented | [05](references/05-bringup-debug.md) |
| G9 Handoff | Files mapped to physical boards; tested scope, untested scope, and next steps recorded for continued work | [08](references/08-evidence-and-handoff.md) |

When a tool or physical board is unavailable, continue independent work and deliver reviewable results with the exact blocker. Never invent DRC, simulation, connectivity, screenshot, or oscilloscope results.

## Reporting maturity

- **Design review complete:** specified static checks passed; identify baseline and coverage.
- **Ready for engineering prototyping:** the design and manufacturing package meet the conditions for this prototype; list accepted residual risks. This is not a mass-production guarantee.
- **Basic prototype functions passed:** identify the board, firmware, power/interface combinations, and tests.
- **Specified verification complete:** evidence covers the defined requirements and tests; make that scope accessible. Do not generalize to all operating conditions, regulatory certification, or unlimited battery life.

See [evidence and handoff](references/08-evidence-and-handoff.md). When the user accepts reduced functionality, retain the requirements change and limitations. Acceptance does not make the original function pass.

## Case lessons

Read [instructions, actions, and failure modes](references/07-case-lessons.md) for the origin of these constraints. Use the lessons to guide decisions, not to copy the old board's electrical values into a new design.

## Tools and templates

- `python scripts/init_project.py --output <project-directory> --name <project-name>` creates `PROJECT.md`, `CHECKS.csv`, and `HANDOFF.md` only in a directory that does not exist. It refuses overwrite.
- `python scripts/release_manifest.py create --root <frozen-release-directory> --revision <revision> --baseline <baseline-id>` generates byte counts and SHA-256 hashes for a prepared release package without modifying the PCB.
- `python scripts/release_manifest.py verify --root <frozen-release-directory>` checks missing, added, and changed files and rejects path traversal and symbolic links. It verifies package integrity, not schematics, impedance, or hardware acceptance.
- Templates start at [assets](assets/PROJECT.template.md). Adapt them to the task; empty tables are not completed work. Leave unperformed checks untested.

Deliver the current conclusion, actual edits, corresponding verification, real limitations, and accessible files. When measurements require user assistance, specify test points, meter mode, power state, expected results, and branches for the next step.
