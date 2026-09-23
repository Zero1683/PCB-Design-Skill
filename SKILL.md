---
name: pcb-design-to-bringup
description: Design manufacturable, assembleable, and testable PCBs from hardware requirements. Covers component selection, schematics, footprint verification, placement and routing, manufacturing handoff, and hardware acceptance. Use for new designs, board reviews and rework, fabrication preparation, and first-board bring-up. Includes staged verification records and project handoff templates. Supports EasyEDA and workflows in other EDA tools. Not for firmware-only changes or enclosure modeling.
metadata:
  version: "2.0.0"
---

# PCB Design to Bring-up

EasyEDA API Skill 1.1.36, API and source-format documentation, the bridge server, and the ws runtime dependency are bundled. The bundled schematic methods library adds block drawing, batch placement and selective net fanout. No separate easyeda-api or schematic enhancement installation is required. See [setup](START_HERE.md) and follow [EDA operations](references/06-easyeda-execution.md) to load the relevant tool documentation and start the bridge. The target machine still needs Node.js, the EDA desktop client, and its Gateway extension. Do not start a service for workflow advice or file-only review.

Deliver designs that can be manufactured, assembled, measured, and maintained. Resolve known issues before the first prototype, but do not promise first-pass success or describe an unbuilt design as a mature product.

Serve people who have an idea but no hardware background. Help them understand
what they will build and take the next practical step. Prefer applicable
manufacturer reference circuits and documented working designs before inventing
new circuitry; verify suitability, changes and reuse permissions. Follow the
[beginner journey](references/30-beginner-experience.md) for communication and
[reuse review](references/13-circuit-intent-and-reuse.md) for engineering evidence.
When a reusable board is useful, follow [open hardware sourcing](references/37-open-hardware-sourcing.md): search for editable source at the time of the project, check the license of the board files themselves, obtain a revisioned working copy, and verify every affected design gate. The linked examples are leads, not bundled or prequalified board designs.
Keep check mechanics in project records; explain progress and necessary decisions
in everyday language. Working-product requests include the path beyond PCB files;
report firmware, assembly and physical tests according to their actual status.
For an existing project, use `scripts/project_progress.py --root ... --baseline ... --lang zh`
to derive the next beginner-facing step from current records. Fix record errors as
agent work; never present a missing evidence file as a user design choice. This
is navigation, not a new release gate. For an external editable base, inventory
the pinned source with `scripts/source_inventory.py` before modifying its copy;
this verifies files, not license permission, native import, or the board itself.

## Read and execute only what this stage needs

Use the user's language. Do not load every reference, full API index or raw export into the conversation. Start with the current stage's rows below; retrieve exact API classes and object records when needed. Run deterministic checks locally, keep full reports on disk, and return bounded summaries. Follow [local execution and cache rules](references/33-local-execution.md). No checks are waived to save quota.

| Current work | Read when needed |
|---|---|
| New idea and component estimate | [Beginner brief](references/30-beginner-experience.md), [cost](references/26-component-cost-planning.md) |
| Finding or adapting an existing board | [Open hardware sourcing](references/37-open-hardware-sourcing.md), [reuse checks](references/13-circuit-intent-and-reuse.md) |
| Power, impedance and electrical calculations | [Analysis](references/09-electrical-analysis.md), [model limits and fallback](references/31-calculation-automation.md) |
| EDA connection or backend choice | [Execution](references/06-easyeda-execution.md), [backends](references/16-easyeda-operation-backends.md); load bundled API skill before live calls |
| Schematic blocks and connections | [Drafting](references/12-schematic-drafting.md), [methods](references/15-easyeda-schematic-methods.md), [intent](references/13-circuit-intent-and-reuse.md) |
| Measured placement and bounded repairs | [Planning](references/21-layout-execution.md), [batch repair](references/22-batch-repair.md); [live writer](references/23-live-eda.md) only for existing parts on unwired schematic pages |
| Mechanical constraints | [Constraint contracts](references/24-executable-constraints.md), [accepted dimensions vs final outline](references/34-mechanical-envelope.md) |
| Operating states, generated variants, derivative boards or factory assembly | [Sourced project reviews](references/36-project-reviews.md); bind applicable reviews to existing requirements and run `project_reviews.py` |
| Native/manufacturing data inspection | [Extraction/toolkit](references/18-pcb-inspection-toolkit.md), [normalized data](references/10-validation-tools.md), [format](references/17-easyeda-native-format.md) |
| Large exports, context recovery or file rollback | [Data and recovery](references/20-data-and-recovery.md); file snapshots cannot roll back a live EDA session |
| Additional command syntax and operation caveats | Relevant section of [operation details](references/35-operation-details.md); do not read all sections by default |
| Changing this skill | [Regression and source admission](references/32-adversarial-improvement.md) |

Local entrypoints: `local_checks.py --root ... --plan ...` runs supported offline batches; `mechanical_envelope.py derive --root ... --baseline ...` generates the dimension contract. Capture fresh native state before writes and release. Cached reports do not establish current EDA state, fresh pricing or whole-board acceptance.

## Default outcome and tool choice

For a request to design a PCB or prepare it for fabrication, finish at **G5: a reviewed, routed, manufacturing-ready engineering prototype package**. Deliver source, Gerber/drills, BOM, assembly information, ordering parameters, and open items for the user to place the order. Do not initiate purchasing, add parts to a cart, submit orders, pay, or contact vendors unless explicitly requested. Reading manufacturer or distributor pages for datasheets, availability, or part selection is allowed; it does not authorize procurement. G6-G9 apply when assembly, hardware testing, or handoff work is requested; absent hardware does not block completing G5.

For EasyEDA, load the **bundled** API skill before choosing an interaction method. Use documented, version-compatible API calls for project creation and editing. Computer use is appropriate for installing/enabling Gateway, login, visual inspection, or a specific API gap/failure. Record that reason and return to API calls when available. Never continue clicking through design simply because installation used the UI. See [connection and operation routing](references/06-easyeda-execution.md).

Use native autorouting for suitable ordinary nets after critical placement, power, and sensitive routes are planned. Preserve completed routes and verify the result. This can reduce per-segment agent work; it does not remove engineering checks or guarantee a particular token saving. Follow [routing strategy](references/03-layout-routing.md).


## Idea-to-cost planning

For a new idea, use the [two-step beginner brief](references/30-beginner-experience.md): recover or ask about purpose, carrier, board size, power, accessible controls/connectors and assembly, then show one dimensioned plan and component estimate for acceptance or changes. Explicit prior delegation covers its stated choices; silence does not. Do not repeat this interview for a narrowly authorized repair or read-only review.

Derive a preliminary BOM and query current 立创商城 prices before detailed schematic work. Follow [component cost planning](references/26-component-cost-planning.md): show component-only consumption and actual purchase totals using build quantity, MOQ, order increments and applicable tiers. If quantity is unknown, state a one-board estimate. Cost reduction preserves confirmed functions and performance unless the user explicitly accepts a downgrade. Refresh the BOM and quotes at G5. After plan acceptance or delegation, continue authorized design without per-operation approval pauses. Price research does not authorize purchasing.

Use [calculation automation](references/31-calculation-automation.md) to distinguish DC voltage drop, PDN response and transmission-line impedance. Calculate locally within a verified model's domain; otherwise use applicable manufacturer tools or browser control. Preserve actual inputs, units, stackup and warnings. Never remove required impedance/process controls solely to reduce cost; compare actual process capability and current quotations.

Use [regression and external-method admission](references/32-adversarial-improvement.md) when changing this skill. Reproduce a failure and a valid neighboring case, fix the cause, and rerun affected checks. Required unsupported or untested coverage remains open; successful scripts cannot guarantee a flawless physical board.


## Drawing and spacing gates

Read [visual and geometry checks](references/14-visual-geometry-gates.md) before placing schematic or PCB components. Exactly two schematic formats are allowed: `free-layout` without a standard outer frame, or `framed-layout` partitioning inside a standard sheet frame. No third format is permitted; record and pass SCH-FORMAT before wiring. Failed format/readability/spacing gates block progression and cannot be waived as small warnings. Follow the common-remedy and item-specific warning disposition tables in reference 12. Define usable canvas/export bounds, reserve metadata or the title block as appropriate, and draw graphical block separators. Pass page-boundary, block and text checks before PCB import. Before routing, pass separate pad-to-pad, silk-to-silk and silk-to-mask checks using positive recorded clearances; a body-envelope check or zero electrical DRC errors is insufficient. Recheck final native drawings and manufacturing outputs. After two ineffective repairs to the same visual defect, diagnose the coordinate/symbol/rendering cause before further edits; do not spend the release stage blindly nudging attributes.


## Starting a task

1. Identify the mode: new design, read-only review, local revision, manufacturing preparation, assembly guidance, or hardware troubleshooting. Resume existing projects at the relevant stage without repeating valid completed work.
2. Read project rules and any `PROJECT.md`, `HANDOFF.md`, and `CHECKS.csv`. Verify the actual project, release revision, and physical board ID. Historical text, screenshots, and files sent to fabrication may describe different revisions.
   For an existing writable project with these records, run `project_progress.py` once for a bounded next-step summary. Treat its user action as a prompt suggestion checked against actual conversation; never infer approval from the generated text.
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
| G1 Architecture and parts | Functional baseline, power/pin plan, procurable preliminary BOM, component-only cost estimate with MOQ and actual tiers, and datasheet sources | [02](references/02-circuit-and-library.md), [26](references/26-component-cost-planning.md) |
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


## Requirement coverage

At stage acceptance, use [current-design evidence](references/27-current-design-evidence.md) and `check_evidence.py --design-gates`. Enforce every registered check through that stage, bind observations to current saved source hashes, and review carry-forward rather than refreshing stale hashes. G2 completion includes both placement and wiring; retain G2-A as its own historical observation. For a new-session whole-board test, follow [benchmark evidence](references/28-fresh-session-benchmark.md).

At intake and before G5, use [requirement coverage](references/25-requirement-coverage.md) to map each sourced requirement to checks and current hashed evidence. Unmapped requirements and stale evidence block release-record acceptance. Inspect the capability matrix before claiming support for a native operation.
