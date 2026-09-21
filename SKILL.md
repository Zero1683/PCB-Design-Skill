---
name: pcb-design-to-bringup
description: Design manufacturable, assembleable, and testable PCBs from hardware requirements. Covers component selection, schematics, footprint verification, placement and routing, manufacturing handoff, and hardware acceptance. Use for new designs, board reviews and rework, fabrication preparation, and first-board bring-up. Includes staged verification records and project handoff templates. Supports EasyEDA and workflows in other EDA tools. Not for firmware-only changes or enclosure modeling.
---

# PCB Design to Bring-up

EasyEDA API Skill 1.1.36, API and source-format documentation, the bridge server, and the ws runtime dependency are bundled. The bundled schematic methods library adds block drawing, batch placement and selective net fanout. No separate easyeda-api or schematic enhancement installation is required. See [setup](START_HERE.md) and follow [EDA operations](references/06-easyeda-execution.md) to load the relevant tool documentation and start the bridge. The target machine still needs Node.js, the EDA desktop client, and its Gateway extension. Do not start a service for workflow advice or file-only review.

Deliver designs that can be manufactured, assembled, measured, and maintained. Resolve known issues before the first prototype, but do not promise first-pass success or describe an unbuilt design as a mature product.

## Engineering constraint evidence

For external design recipes or stackup, dense escape, timing and thermal decisions,
read [engineering constraints](references/19-engineering-constraints.md). Resolve
critical numbers to exact-part/process sources and track calculation, native rule,
actual geometry and manufacturing readback under one baseline. Do not adopt article
defaults or reduce rules to force PASS. Classify warnings by physical consequence.

## Default outcome and tool choice

For a request to design a PCB or prepare it for fabrication, finish at **G5: a reviewed, routed, manufacturing-ready engineering prototype package**. Deliver source, Gerber/drills, BOM, assembly information, ordering parameters, and open items for the user to place the order. Do not initiate purchasing, add parts to a cart, submit orders, pay, or contact vendors unless explicitly requested. Reading manufacturer or distributor pages for datasheets, availability, or part selection is allowed; it does not authorize procurement. G6-G9 apply when assembly, hardware testing, or handoff work is requested; absent hardware does not block completing G5.

For EasyEDA, load the **bundled** API skill before choosing an interaction method. Use documented, version-compatible API calls for project creation and editing. Computer use is appropriate for installing/enabling Gateway, login, visual inspection, or a specific API gap/failure. Record that reason and return to API calls when available. Never continue clicking through design simply because installation used the UI. See [connection and operation routing](references/06-easyeda-execution.md).

Use native autorouting for suitable ordinary nets after critical placement, power, and sensitive routes are planned. Preserve completed routes and verify the result. This can reduce per-segment agent work; it does not remove engineering checks or guarantee a particular token saving. Follow [routing strategy](references/03-layout-routing.md).

## EasyEDA backend selection

Read [operation backends](references/16-easyeda-operation-backends.md) when selecting or changing an EDA integration. Official API and native-format references are bundled, alongside the schematic methods. Community easyeda-agent is an optional typed CLI/Connector backend; easyeda-mcp-pro is an optional external MCP backend with its own license. Neither is required or installed automatically. Keep one selected writer for an operation scope and retain this skill's full design sequence and acceptance gates.

For native source inspection, generation or repair, read [native format operations](references/17-easyeda-native-format.md) and the bundled official format reference. Use explicit document types and the file-input schema adapter; do not equate schema validation with an importable project or a working circuit.

## EasyEDA operating foundations

For online schematic operations, use these two bundled layers: [easyeda-api](vendor/easyeda-api/SKILL.md) for the bridge and exact operation references, and [schematic methods](references/15-easyeda-schematic-methods.md) for drawing blocks, placing parts, selective fanout and controlled revisions. For EasyEDA schematic work, load the methods reference before applying the bundled [upstream recipes](vendor/easyeda-schematic-net-fanout/SKILL.md). This workflow owns staging and acceptance; the adapter identifies which upstream shortcuts require replacement or version verification. Both layers are available by relative path without separate installation or discovery.

## Schematic drafting sequence

Before creating a schematic, read [schematic drafting standards](references/12-schematic-drafting.md). Complete G2-A with all required components placed, named functional blocks, no unintended overlap, and zero electrical wires/buses. Read back and visually inspect the placement, save its evidence, then continue to G2-B wiring and electrical review. The zero-wire requirement applies to the placement snapshot only. Existing wired projects retain their connections; review their current state and apply the staged process to new blocks.

## Drawing and spacing gates

Read [visual and geometry checks](references/14-visual-geometry-gates.md) before placing schematic or PCB components. Exactly two schematic formats are allowed: `free-layout` without a standard outer frame, or `framed-layout` partitioning inside a standard sheet frame. No third format is permitted; record and pass SCH-FORMAT before wiring. Failed format/readability/spacing gates block progression and cannot be waived as small warnings. Follow the common-remedy and item-specific warning disposition tables in reference 12. Define usable canvas/export bounds, reserve metadata or the title block as appropriate, and draw graphical block separators. Pass page-boundary, block and text checks before PCB import. Before routing, pass separate pad-to-pad, silk-to-silk and silk-to-mask checks using positive recorded clearances; a body-envelope check or zero electrical DRC errors is insufficient. Recheck final native drawings and manufacturing outputs. After two ineffective repairs to the same visual defect, diagnose the coordinate/symbol/rendering cause before further edits; do not spend the release stage blindly nudging attributes.

## Prevent late rework

Before wiring, verify schematic values against independently resolved MPN/supplier specifications (`PART-IDENTITY`, reference 02). Before routing, verify native outline recognition, placement gates and actual routing rules/tool capability (`ROUTING-READY`, reference 03). Before bulk API edits, prove one object's requested change and protected properties survive save/reopen (reference 06). Consolidate defects, repair native source, then freeze and export one reviewed candidate (`RELEASE-FREEZE`, reference 04); later edits invalidate only the relevant checks unless side effects are uncertain.

## Structured data and bounded operation recovery

Use [data reconciliation and recovery](references/20-data-and-recovery.md) when
combining native PCB/toolkit records, reading large exports, or operating on a
complete closed-file native project copy. Reconcile observed data independently of
design intent, query summaries/deltas before detail, and preserve raw files.
The file state machine edits only an isolated candidate and guards recovery by hashes;
it cannot roll back a running EDA client or turn an inspection JSON into a native backup.

## Native extraction and independent inspection

At G3-G5, use the [PCB inspection toolkit](references/18-pcb-inspection-toolkit.md)
when native exports or manufacturing files are available. The bundled adapted tools
cover PCB/footprint extraction, physical connectivity, placement/via corridors,
Gerber/drill/mask checks, mesh envelopes and optional DSN/SES routing. Invoke through
`scripts/pcb_toolkit.py`; supply actual rule/layer inputs and verify extraction
coverage before trusting geometry. Unsupported formats and missing objects fail
explicitly. Toolkit board JSON is not the normalized schema in reference 10.
These tools supplement existing stage gates; script success is not board acceptance.

## Measured schematic placement

For new G2-A blocks, use [layout planning and native execution](references/21-layout-execution.md)
when organizing multiple measured functional blocks. Measure complete visible envelopes,
compute a fixed plan, apply through the selected backend, then compare immediate
and post-reload observations. The helper packs existing local blocks; it does not
solve wiring, operate EDA or certify save/reload. Preserve two-format and stage rules.

## Circuit intent and reuse

For critical connection checks, reusable blocks, or revisions, read [circuit intent and reuse](references/13-circuit-intent-and-reuse.md). Record expectations from requirements and exact-part documentation, implement through the native EDA workflow, then compare independent intent with actual exported pin nets. Keep native source authoritative for the implemented design. Recheck reused blocks against the new supply, load, pin mapping, and physical constraints. No additional circuit language or PCBDL dependency is required.

## Language

Use the user's language for conversation, explanations, and generated project records unless they request otherwise. Keep API names, commands, file paths, identifiers, status values, and template placeholders unchanged. English instructions do not require English replies.

## Starting a task

1. Identify the mode: new design, read-only review, local revision, manufacturing preparation, assembly guidance, or hardware troubleshooting. Resume existing projects at the relevant stage without repeating valid completed work.
2. Read project rules and any `PROJECT.md`, `HANDOFF.md`, and `CHECKS.csv`. Verify the actual project, release revision, and physical board ID. Historical text, screenshots, and files sent to fabrication may describe different revisions.
3. Read [requirements and context recovery](references/01-intake-and-recovery.md). Extract confirmed parameters first. Ask only for missing information that affects architecture, interfaces, or manufacturing outcomes; do not reconfirm settled requirements.
4. For tasks permitting writes, save new work in the authorized directory and follow storage preferences. Use `scripts/init_project.py --lang zh` for Chinese records or `--lang en` for English to initialize templates without overwriting files, or copy them manually if Python is unavailable. For read-only reviews, report in the conversation by default; do not initialize or update project records, and use access methods that leave the original project unchanged.
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
| G2 Schematics and footprints | G2-A component inventory and unwired placement review; G2-B wiring, readable drawing, pin/footprint checks, ERC disposition, and consistent BOM | [02](references/02-circuit-and-library.md), [12](references/12-schematic-drafting.md) |
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

## Electrical review beyond DRC

At G1/G2, calculate supply/load budgets and component operating margins. At G4, update calculations from actual geometry: DC path drop/loss, load-step budget, relevant signal impedance and return paths. Use [electrical analysis](references/09-electrical-analysis.md) and its reproducible calculator. Do arithmetic with available tools; ask the user only for unavailable inputs, inaccessible calculators, or physical measurements, with exact fields and units. Do not ask a beginner to invent stackup values or interpret an unexplained impedance number.

## Tools and templates

- `python scripts/init_project.py --output <project-directory> --name <project-name> --lang <en|zh>` creates `PROJECT.md`, `CHECKS.csv`, and `HANDOFF.md` only in a directory that does not exist. It refuses overwrite.
- `python scripts/release_manifest.py create --root <frozen-release-directory> --revision <revision> --baseline <baseline-id>` generates byte counts and SHA-256 hashes for a prepared release package without modifying the PCB.
- `python scripts/release_manifest.py verify --root <frozen-release-directory>` checks missing, added, and changed files and rejects path traversal and symbolic links. It verifies package integrity, not schematics, impedance, or hardware acceptance.
- `python scripts/check_evidence.py --root <project-directory> --baseline <baseline-id> --through G5 --design-gates` enforces required design-gate rows and checks record completeness, evidence files, and baseline identity. It does not certify the circuit.
- `python scripts/electrical_calcs.py --input <calculations.json>` calculates sourced first-order power, loss, DC path, and transient budgets; see [09](references/09-electrical-analysis.md).
- `python scripts/audit_design.py compare <schematic.json> <pcb.json>` compares normalized records; `geometry <pcb.json> --clearance-mm <value>` screens body envelopes. See [data contracts](references/10-validation-tools.md); these are not native EDA parsers.
- `python scripts/check_connectivity.py <snapshot.json> <circuit-checks.json>` checks declared pin relationships against a normalized native export. `python scripts/audit_design.py diff <before.json> <after.json>` reports component/pin changes between revisions. See [13](references/13-circuit-intent-and-reuse.md); neither result certifies electrical or physical correctness.
- Run [behavioral and live validation](references/11-validation-scenarios.md) when changing this skill or its integration. Do not report dry-run scenarios as real EDA validation.
- Templates start at [assets](assets/PROJECT.template.md). Adapt them to the task; empty tables are not completed work. Leave unperformed checks untested.

Deliver the current conclusion, actual edits, corresponding verification, real limitations, and accessible files. When measurements require user assistance, specify test points, meter mode, power state, expected results, and branches for the next step.
