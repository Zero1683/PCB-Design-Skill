# Skill validation scenarios

Run these when changing tool selection, design scope, electrical review, or integration behavior. Record skill commit, platform, client/extension version, raw inputs, observable actions, outputs, and unresolved items. Dry-run evaluations do not establish live EDA compatibility or reduce a hardware test requirement.

## Independent task scenarios

| Task given to evaluator | Observable acceptance |
|---|---|
| New Mac user has installed EasyEDA/Gateway and wants a small sensor PCB, files only | Loads bundled API instructions, checks bridge/API separately, prefers supported API operations, stops at G5; no supplier cart/order; no compulsory blanket restart |
| Review an existing board without changes | Uses supplied evidence read-only, separates visible geometry from connectivity, reports missing checks; no repour/save/record initialization |
| Route a partially routed MCU board; power and USB are already reviewed | Assesses a native autoroute for ordinary nets, preserves critical routes, handles empty net selection, verifies actual results; no clear-all shortcut |
| Supply has a narrow neck and a burst load; user only owns a multimeter | Calculates sourced DC drop/loss and available transient budget, requests missing inputs, distinguishes estimates from actual dynamic impedance; no invented scope measurements |
| Create a schematic from a parts list and functional requirements | Places all parts with named blocks and no overlap, reads back zero wire/bus counts, inspects and saves G2-A evidence before wiring; then completes G2-B checks without an unnecessary approval pause |
| Improve a wired schematic with no historical placement-only snapshot | Preserves connections, reports missing historical evidence, reviews current inventory/placement and electrical state; stages new blocks within an explicit scope |
| Reuse a sensor module on another voltage rail and modify its enable connection | Rechecks exact parts, logic/startup levels and module assumptions; keeps local nets unique; applies independent pin rules to actual native exports after wiring and reports before/after changes without replacing EDA checks |
| EasyEDA schematic using the bundled enhancement recipes | Loads the adapter and API by relative path without a second installation; draws one of the two allowed formats, saves G2-A before fanout, shows critical local connections directly, and verifies native pin nets rather than counts |
| Fanout batch times out after creating some objects; a nearby label belongs to another block | Reads actual state and recorded IDs, preserves unrelated/shared objects, resumes only missing operations; no full-batch retry or proximity-only deletion |
| Dense rotated MCU pins collide with labels at a 10-unit offset | Probes transform and full label bounds, changes local spacing/branch layout, and checks rendering; does not claim fixed offsets guarantee clearance or silently skip pins |
| Board enumerates but fails at packet boundaries | Separates physical power/boot/link evidence from software behavior, requests discriminating measurements; no immediate component removal based only on symptom |

Give an independent evaluator only the request, skill and necessary artifacts before revealing acceptance notes. Document incorrect or missing behavior and fix instructions narrowly. Do not claim a token reduction without a same-task comparison and recorded usage.

## Backend and format integration scenarios

| Task | Observable acceptance |
|---|---|
| Choose tools on a machine with official Gateway and a community connector | Identifies protocols and versions, keeps one writer for the scope, retains our main workflow and does not replace the default connection based on port alone |
| Use typed compose for a new schematic | Preserves our unwired placement review; if the selected action cannot separate stages, hands off explicitly to the supported API path |
| Community layout check passes but a long part value overlaps a frame | Treats the tool's coverage as partial, checks all visible text and repairs before claiming our drawing gates pass |
| Generate a PCB LINE using a schematic payload or wrong document | Rejects incorrect domain/schema; does not silently fall back or describe schema-valid data as a finished project |
| Native ungrouped PCB LINE uses groupId 0 but schema expects string | Preserves the native value, records the schema discrepancy and requests native-version evidence; no string coercion to manufacture PASS |
| Add MCP inspection to an MIT distribution | Keeps the reviewed noncommercial implementation external, verifies selected version and setup scope, and does not enable supplier purchasing |

## Live EasyEDA smoke test

Use a disposable test project; do not repurpose an active valuable design. Project creation is a mutation, so run this only within authorized test scope. Save unrelated open work before changing documents. Current bundled API creation and autorouting are beta; respect installed-version restrictions and record any UI fallback.

1. On Windows and separately on macOS, record Node/EDA/Gateway versions and installation location. Start or reuse the bridge, verify the selected window, then run the read-only probe.
2. Create a uniquely identified disposable project using a supported API; reread its UUID/name, open it safely, and create required documents using exact documented methods. If creation API is restricted, record UI creation as a fallback and resume API operations.
3. Place a minimal circuit with a known pin mapping using supported calls. Move one component, read back position/rotation, inspect named blocks and rendered placement, compare expected units, and save the G2-A snapshot with zero native wire/bus counts. Then connect it, inspect junctions and labels, compare actual pin nets, and save G2-B evidence separately.
4. Set simple routing rules. Explicitly route one net, native-autoroute an explicit different ordinary-net list with existing routes preserved, then confirm the first route stayed unchanged and inspect failed nets/results.
5. Rebuild pours where applicable, run real DRC/unrouted checks, export manufacturing files, independently preview them, save and reopen the project. Confirm nets, positions and export identity.
6. Exercise a wrong-window ID and a disconnected Gateway. They must fail clearly without editing another window or duplicating work after reconnect. Simulated HTTP failures in unit tests cover transport handling only.
7. Save logs and screenshots. Mark each platform and operation separately PASS/FAIL/BLOCKED/NOT_RUN. End-to-end acceptance requires the observable actions above, not merely a healthy bridge.

## Current validation boundary

Python tests cover record validation, first-order arithmetic, normalized comparison, envelope screening and initialization. A local fake bridge tests the read-only probe's transport/payload behavior. These tests are not live EasyEDA or macOS testing. Retain the actual live status in the release notes; do not carry forward a PASS from unrelated earlier PCB work.

## Inspection-toolkit integration scenarios

- Import a supported native export with one missing footprint: fails without
  producing a partial successful model. Two PCB documents cannot select the last silently.
- Use a misspelled net in connect/open/isolation assertions: fails; empty or
  malformed contracts are rejected. Known good and genuinely disconnected fixtures
  must still produce the expected different outcomes.
- Feed clear-polarity Gerber or unsupported aperture macros: refuses calculation;
  no manufactured artwork is altered to satisfy the parser.
- Leave a previous SES output in the destination: not completion for this run.
  Growing output must not mask a crash; a pending --once query is nonzero.
- Watch a live process on Windows: it remains alive, then is reported gone after
  independently ending it. No signal is sent by the probe.
- Missing NumPy/model geometry or a plane-net assumption: report coverage and
  remaining checks instead of inheriting full-board PASS from an exit code.

Automated fixture results belong in VALIDATION.md. A new board's native client,
real export compatibility, full rendering and physical hardware need their own evidence.

## Engineering-recipe regression scenarios

| Input or task | Observable acceptance |
|---|---|
| Article proposes a 600 mA regulator for a 1.2 A core rail | Rejects the rating mismatch; calculates loss separately, resolves exact variant and power estimate before circuit reuse |
| 0.45 mm pad; 0.02 mm expansion per side | Computes 0.49 mm opening; checks the resulting adjacent dam, process and SMD/NSMD intent before changing expansion |
| BGA pitch 0.8 mm, projected pads 0.45 mm, clearance 0.18 mm | Reports negative single-track width budget; proposes supported process/layer/package changes instead of claiming a routable 0.15 mm trace |
| A 10 MHz signal has fast edges; requested rule is blanket 1 mm matching | Resolves edge rate, timing endpoints and return topology; no frequency-only classification or automatic meanders |
| Article says 144 vias times 0.3 A removes 43 A of heat | Rejects dimensional mismatch; uses loss in W and applicable package/board thermal model; no arbitrary via array |
| Yellow DFM finding removes a supply neck; red finding is an identified report artifact | Classifies actual electrical/physical impact, repairs the supply neck and records the specific artifact evidence; no color-based blanket waiver |
| Tutorial names a plugin/menu absent from the installed client | Verifies availability/version; uses documented backend operations or records a specific gap, without inventing commands |

These are evaluation inputs and expected behavior, not claims of live EDA or hardware
validation. Automated arithmetic coverage is recorded separately in VALIDATION.md.

## Data and recovery scenarios

- Join observed PCB models with conflicting element and numbered pad nets: reject
  the join without substituting the intended connection. Missing nets remain unknown.
- Read a large board for one decision: use summary then exact/paged queries, preserve
  raw geometry and show coverage and digest. Do not promise a fixed token reduction.
- Fail an isolated edit after the user changes the original source: refuse recovery;
  preserve both user changes and failed candidate.
- Interrupt recovery between candidate renames: resume the recorded operation and
  preserve the failed copy, without claiming live EDA or electrical acceptance.
- Feed an online/cloud-only inspection export as a restorable project: reject that
  workflow; use supported native checkpoint/readback and verify restore separately.
