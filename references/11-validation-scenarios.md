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
| Board enumerates but fails at packet boundaries | Separates physical power/boot/link evidence from software behavior, requests discriminating measurements; no immediate component removal based only on symptom |

Give an independent evaluator only the request, skill and necessary artifacts before revealing acceptance notes. Document incorrect or missing behavior and fix instructions narrowly. Do not claim a token reduction without a same-task comparison and recorded usage.

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
