# On-demand operation details

Read only the section relevant to the current operation. Stage-specific references remain authoritative for their detailed contracts. Commands are run from the skill root.

## Engineering constraint evidence

For external design recipes or stackup, dense escape, timing and thermal decisions,
read [engineering constraints](19-engineering-constraints.md). Resolve
critical numbers to exact-part/process sources and track calculation, native rule,
actual geometry and manufacturing readback under one baseline. Do not adopt article
defaults or reduce rules to force PASS. Classify warnings by physical consequence.


## EasyEDA backend selection

The [third-party inventory](../THIRD_PARTY_NOTICES.md) identifies bundled tools, pinned versions, runtime packages and external-only backends. Preserve vendor notices; a reference to a backend does not mean it is installed.

Read [operation backends](16-easyeda-operation-backends.md) when selecting or changing an EDA integration. Official API and native-format references are bundled, alongside the schematic methods. Community easyeda-agent is an optional typed CLI/Connector backend; easyeda-mcp-pro is an optional external MCP backend with its own license. Neither is required or installed automatically. Keep one selected writer for an operation scope and retain this skill's full design sequence and acceptance gates.

For native source inspection, generation or repair, read [native format operations](17-easyeda-native-format.md) and the bundled official format reference. Use explicit document types and the file-input schema adapter; do not equate schema validation with an importable project or a working circuit.


## EasyEDA operating foundations

For online schematic operations, use these two bundled layers: [easyeda-api](../vendor/easyeda-api/SKILL.md) for the bridge and exact operation references, and [schematic methods](15-easyeda-schematic-methods.md) for drawing blocks, placing parts, selective fanout and controlled revisions. For EasyEDA schematic work, load the methods reference before applying the bundled [upstream recipes](../vendor/easyeda-schematic-net-fanout/SKILL.md). This workflow owns staging and acceptance; the adapter identifies which upstream shortcuts require replacement or version verification. Both layers are available by relative path without separate installation or discovery.


## Schematic drafting sequence

Before creating a schematic, read [schematic drafting standards](12-schematic-drafting.md). Complete G2-A with all required components placed, named functional blocks, no unintended overlap, and zero electrical wires/buses. Read back and visually inspect the placement, save its evidence, then continue to G2-B wiring and electrical review. The zero-wire requirement applies to the placement snapshot only. Existing wired projects retain their connections; review their current state and apply the staged process to new blocks.


## Prevent late rework

Before wiring, verify schematic values against independently resolved MPN/supplier specifications (`PART-IDENTITY`, reference 02). Before routing, verify native outline recognition, placement gates and actual routing rules/tool capability (`ROUTING-READY`, reference 03). Before bulk API edits, prove one object's requested change and protected properties survive save/reopen (reference 06). Consolidate defects, repair native source, then freeze and export one reviewed candidate (`RELEASE-FREEZE`, reference 04); later edits invalidate only the relevant checks unless side effects are uncertain.


## Structured data and bounded operation recovery

Use [data reconciliation and recovery](20-data-and-recovery.md) when
combining native PCB/toolkit records, reading large exports, or operating on a
complete closed-file native project copy. Reconcile observed data independently of
design intent, query summaries/deltas before detail, and preserve raw files.
The file state machine edits only an isolated candidate and guards recovery by hashes;
it cannot roll back a running EDA client or turn an inspection JSON into a native backup.


## Native extraction and independent inspection

At G3-G5, use the [PCB inspection toolkit](18-pcb-inspection-toolkit.md)
when native exports or manufacturing files are available. The bundled adapted tools
cover PCB/footprint extraction, physical connectivity, placement/via corridors,
Gerber/drill/mask checks, mesh envelopes and optional DSN/SES routing. Invoke through
`scripts/pcb_toolkit.py`; supply actual rule/layer inputs and verify extraction
coverage before trusting geometry. Unsupported formats and missing objects fail
explicitly. Toolkit board JSON is not the normalized schema in reference 10.
Require nonempty measured coverage. Distinguish FAIL from NOT_CHECKED; unsupported
geometry cannot establish acceptance. Protected routing needs a prior geometric
baseline. Confirm pad plating, actual layer spans and mask-opening policy before
using their results; details are in reference 18.
These tools supplement existing stage gates; script success is not board acceptance.


## Measured schematic placement

For new G2-A blocks, use [layout planning and native execution](21-layout-execution.md)
when organizing multiple measured functional blocks. Measure complete visible envelopes,
compute a fixed plan, apply through the selected backend, then compare immediate
and post-reload observations. The helper packs existing local blocks; it does not
solve wiring, operate EDA or certify save/reload. Preserve two-format and stage rules.

For bounded layout writes and repairs, use [batch preflight and repair feedback](22-batch-repair.md).
Preview the complete target from fresh source, record actual observations and use
one scoped retry ledger. Change the failing plan or adapter before retrying;
repeated/no-progress failures stop that method. Reports are repair evidence,
not executable commands or proof of electrical intent. Native readback still applies.


## Circuit intent and reuse

For critical connection checks, reusable blocks, or revisions, read [circuit intent and reuse](13-circuit-intent-and-reuse.md). Record expectations from requirements and exact-part documentation, implement through the native EDA workflow, then compare independent intent with actual exported pin nets. Keep native source authoritative for the implemented design. Recheck reused blocks against the new supply, load, pin mapping, and physical constraints. No additional circuit language or PCBDL dependency is required.


## Language

Use the user's language for conversation, explanations, and generated project records unless they request otherwise. Keep API names, commands, file paths, identifiers, status values, and template placeholders unchanged. English instructions do not require English replies.


## Case lessons

Read [instructions, actions, and failure modes](07-case-lessons.md) for the origin of these constraints. Use the lessons to guide decisions, not to copy the old board's electrical values into a new design.


## Electrical review beyond DRC

At G1/G2, calculate supply/load budgets and component operating margins. At G4, update calculations from actual geometry: DC path drop/loss, load-step budget, relevant signal impedance and return paths. Use [electrical analysis](09-electrical-analysis.md) and its reproducible calculator. Do arithmetic with available tools; ask the user only for unavailable inputs, inaccessible calculators, or physical measurements, with exact fields and units. Do not ask a beginner to invent stackup values or interpret an unexplained impedance number.


## Persistent constraints

Before placement changes and after task resumption, reload the current constraint revision, native state and open items. Use [executable constraints and bounded context](24-executable-constraints.md): bind mechanical rules to actual IDs/units, require them for guarded live batches, and use output-budgeted data queries. This does not provide native PCB mutation or full 3D checking.


## Guarded native writes

For G2-A moves of existing parts on an unwired EasyEDA page, use [the guarded live writer](23-live-eda.md). It captures native state, preflights the batch, preserves writable properties, verifies actual writes and performs guarded compensation. Use its explicit save/reopen check before claiming persistence. Other native operations retain their selected backend and normal gates; this wrapper does not intercept external calls.


## Tools and templates

- `python scripts/init_project.py --output <project-directory> --name <project-name> --lang <en|zh>` creates `PROJECT.md`, `CHECKS.csv`, and `HANDOFF.md` only in a directory that does not exist. It refuses overwrite.
- `python scripts/release_manifest.py create --root <frozen-release-directory> --revision <revision> --baseline <baseline-id>` generates byte counts and SHA-256 hashes for a prepared release package without modifying the PCB.
- `python scripts/release_manifest.py verify --root <frozen-release-directory>` checks missing, added, and changed files and rejects path traversal and symbolic links. It verifies package integrity, not schematics, impedance, or hardware acceptance.
- `python scripts/check_evidence.py --root <project-directory> --baseline <baseline-id> --through G5 --design-gates` enforces required design-gate rows and checks record completeness, evidence files, and baseline identity. It does not certify the circuit.
- `python scripts/component_cost.py --input <component-quotes.json>` calculates component-only per-board consumption and MOQ/tier-aware purchase amounts from observed quotes. See [26](26-component-cost-planning.md); it does not query prices or purchase parts.
- `python scripts/electrical_calcs.py --input <calculations.json>` calculates sourced first-order power, loss, DC path, and transient budgets; see [09](09-electrical-analysis.md).
- `python scripts/audit_design.py compare <schematic.json> <pcb.json>` compares normalized records; `geometry <pcb.json> --clearance-mm <value>` screens body envelopes. See [data contracts](10-validation-tools.md); these are not native EDA parsers.
- `python scripts/check_connectivity.py <snapshot.json> <circuit-checks.json>` checks declared pin relationships against a normalized native export. `python scripts/audit_design.py diff <before.json> <after.json>` reports component/pin changes between revisions. See [13](13-circuit-intent-and-reuse.md); neither result certifies electrical or physical correctness.
- Run [behavioral and live validation](11-validation-scenarios.md) when changing this skill or its integration. Do not report dry-run scenarios as real EDA validation.
- Templates start at [assets](../assets/PROJECT.template.md). Adapt them to the task; empty tables are not completed work. Leave unperformed checks untested.

Deliver the current conclusion, actual edits, corresponding verification, real limitations, and accessible files. When measurements require user assistance, specify test points, meter mode, power state, expected results, and branches for the next step.
