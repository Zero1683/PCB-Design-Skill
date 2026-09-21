# G2: Schematic drafting and staged review

Read this before creating a schematic or adding a new functional block. Apply it together with [circuit and footprint checks](02-circuit-and-library.md). These drafting conventions organize the drawing; electrical decisions still require the exact parts' datasheets and [electrical analysis](09-electrical-analysis.md).

## Two-stage workflow

For a new schematic, complete **G2-A: components and placement, with zero electrical wires**, inspect it, then proceed to **G2-B: wiring and electrical review**. The AI performs the intermediate review and fixes failures before wiring. Continue automatically within the authorized scope after passing; stop there only if the user requested placement only or another unresolved requirement blocks wiring.

For an existing wired design, preserve valid work. Review its current organization and connectivity without deleting wires to recreate G2-A. For a new block on an existing sheet, apply the unwired stage to that block and explicitly record the scope; the whole sheet need not have zero wires. Missing historical placement evidence remains unavailable, never a fabricated PASS.

## Functional organization

1. **Functional blocks:** group power, input protection, controller, clocks, reset, communications, sensors, actuators, and debug interfaces as applicable. Give every block a visible, meaningful title. Omit blocks the design does not need.
2. **Signal flow:** arrange input, protection/filtering, functional processing, controller, and output in a readable sequence, usually left to right. Bidirectional interfaces may use a clearly labeled branch.
3. **Power flow:** show the source connector, protection, conversion, filtering, and loads in order. Label rail voltages and destinations; show source selection and backfeed paths where relevant.
4. **Associated parts:** place decoupling capacitors, pull resistors, terminations, crystals, inductors, TVS, and ESD protection beside their associated pins or interfaces in the drawing. Record actual PCB proximity and loop requirements separately; schematic proximity is only logical organization.
5. **Signal domains:** separate high-voltage, high-current, high-speed, analog, digital, RF, and sensitive circuits into identifiable regions. Avoid mixing unrelated paths or routing noisy signals across sensitive blocks in the drawing.
6. **Ground and isolation domains:** distinguish power and signal returns and any analog/digital domains. Show where currents return and where domains join. Named functional regions do not require split copper grounds: follow manufacturer guidance and preserve appropriate continuous returns. For genuine galvanic isolation, show the barrier and every crossing explicitly; different ground symbols alone do not establish isolation or adequate PCB clearance.
7. **External interfaces:** group interface circuitry beside its connector. Put protection first in the external signal path where the device topology requires it, and carry the connector-side placement requirement into PCB layout.
8. **Controller peripherals:** arrange supporting circuits around the corresponding pin functions to reduce crossings and make critical nets easy to follow. Keep the correct symbol-to-package pin mapping when arranging or rotating symbols; drawing aesthetics cannot justify swapping pins.

## G2-A: Place, organize, inspect

1. Build the expected component inventory from the selected architecture and pin requirements. Include support parts, protection, pulls, decoupling, clocks, reset, programming connectors, test points, and relevant mechanical parts. Identify DNP parts and multi-unit symbols explicitly. Unresolved selections must be listed and resolved before wiring the affected circuit.
2. Place all required symbol units on a consistent electrical snap grid. Assign unique instance reference designators, readable values, exact part/footprint associations, and fitted status. Multi-unit symbols may share their component reference, with distinct unit identifiers.
3. Apply the functional organization above. Leave room for local wires, net labels, and component annotations. Align blocks and repeated circuits, keep symbols and text from overlapping, and place module titles outside component and wiring areas.
4. Do not create electrical wires or buses yet. Use graphical primitives for frames and separators, clearly distinguished from electrical primitives. Defer external net labels, power ports, and inter-sheet connectivity until G2-B; do not let touching pin endpoints accidentally connect placed components. Account for any library-defined internal or hidden power connections in the pin review.
5. Read the actual document back. Compare expected parts against placed parts by identity, unit, value, and footprint. Inspect the rendered overview and detailed views for symbol/text overlap, missing module titles, pin accessibility, and the intended flow. A component count alone cannot detect one missing part replaced by a duplicate.
6. Count native electrical wire and bus primitives in the reviewed scope. Both counts must be **0**. Record the document/sheet IDs, scope, extraction method, counts, and snapshot identity. A screenshot alone cannot certify a zero count; if the tool cannot expose it, record the limitation and obtain a suitable native export or inspection before claiming this check passed.
7. Save the placement-only source snapshot, inventory comparison, count report, and overview/detail images. Fix omissions and overlap, then repeat affected checks. Unconnected pins are expected at this stage; do not add NC markers merely to suppress their warnings.

**G2-A acceptance:** every required component is present, symbols and annotations have no unintended overlap, every functional block has a name, placement follows the applicable organization rules, and the scoped electrical wire and bus counts are zero. The AI must inspect these results before creating wires.

## G2-B: Connect, annotate, verify

### Connections and readability

- Use native electrical wires snapped to verified pin endpoints. Prefer clear orthogonal routes and consistent spacing. Use graphical lines only for non-electrical frames and notes.
- Show local critical topologies directly: regulator feedback and energy paths, reset/boot networks, clock connections, protection, and decoupling. Use net labels for distant or cross-sheet connections without hiding the relationships needed to review the circuit.
- Make junctions explicit. Prefer T-junctions over ambiguous four-way intersections. An ordinary crossing must remain visibly and electrically unconnected; check the actual netlist rather than assuming the presence or absence of a rendered dot is decisive.
- Keep wire runs away from reference designators, values, pin numbers, and module titles. Do not route through unrelated symbols. Maintain readable text at normal page/PDF viewing size; enlarge the sheet or split it into named sheets when needed.
- Use consistent, exact net names and label scope. Distinguish voltage domains, differential polarity, active-low signals, and similarly named interfaces. Check global power names, local labels, hierarchical ports, bus members, and cross-sheet references against actual connectivity.
- Show power and ground in consistent orientations where practical, conventionally power upward and ground downward. Preserve readable signal flow when a different orientation is clearer.
- Include connector pin numbers, signal names, voltage/logic levels, and a viewing-direction note when needed to interpret the mating connector. Identify polarity, pin 1, test points, DNP options, and mutually exclusive links.
- Show component values and units consistently. Keep required ratings, tolerance, and variant information in visible annotations or linked properties/BOM so a reviewer can verify the selection. Do not replace a full part number with an ambiguous family name.

### Electrical review

1. Check each functional block against the exact datasheet and approved pin table. Include supply pins, exposed pads, reserved/unused pins, startup states, protection polarity, logic levels, and recovery interfaces.
2. Verify actual connected pin sets, intentional unconnected pins, and the boundaries between voltage/ground domains. Apply NC markers only to intentionally unused pins where the datasheet permits that treatment, with the reason recorded.
3. Check power budgets, feedback/divider values, current limiting, pulls, timing, ratings, and margins using reference 09. ERC cannot establish these by itself.
4. Run native schematic rules/ERC and review individual findings. Reconcile symbol properties, footprints, fitted status, and BOM. Record justified exceptions without disabling rules to hide faults.
5. Export and inspect the completed drawing as an overview and at readable detail. Check block boundaries, title placement, references, page order, and off-sheet navigation. Include project name, sheet title/number, revision, and date in the title block. Save the final source, netlist, BOM, rule report, and rendered review evidence.

**G2-B acceptance:** the completed schematic is readable, intended pin connections are verified, electrical calculations and footprint checks are recorded, and rule findings are resolved or have specific justified dispositions. Zero wires is no longer a criterion.

## Evidence and later revisions

Use the following IDs in `CHECKS.csv`. Record G2-A or G2-B in `conditions`, together with the sheet/block scope. The `baseline_id` identifies the reviewed design state; each evidence file must also identify its precise snapshot or revision.

| Check ID | Phase | Evidence |
|---|---|---|
| SCH-INVENTORY | G2-A | Expected-versus-placed identity/unit/value/footprint comparison |
| SCH-PLACEMENT | G2-A | Named blocks, flow review, overview and readable details; no unintended overlap |
| SCH-UNWIRED | G2-A | Placement-only source snapshot plus scoped native wire/bus counts of 0 |
| SCH-WIRING | G2-B | Pin-table and netlist review, intentional NC treatment, label/domain checks |
| SCH-VISUAL | G2-B | Final drawing export and visual review, including title block and sheet navigation |

Retain the G2-A snapshot as historical process evidence after wiring. Never reuse its zero count as a measurement of the final wired document. For a later design baseline, retain the original snapshot identity and document whether changes invalidate its inventory or placement findings. The evidence checker deliberately rejects stale baseline IDs; archive superseded rows separately and record any applicable re-review for the current baseline. Do not relabel old measurements as newly performed checks.

For existing designs where the unwired phase was not performed, record the limitation and applicability decision. Review current inventory, placement, wiring, and readability; do not erase a working circuit to manufacture historical evidence. Any new parts or changed modules require an affected-scope inventory and placement review before wiring them.

## Visual reference

![User-supplied example of schematic page organization](../assets/schematic-style-reference.png)

This user-supplied image illustrates aligned functional blocks, visible module names, locally readable circuits, a drawing frame, and a title block. It shows a **wired** drawing and therefore illustrates final G2-B presentation. It is not a G2-A zero-wire example, a universal parts list, or an electrically validated reference circuit. Apply the organization to the current design; choose parts and connections from its own requirements and manufacturer documentation. Image provenance and licensing scope are recorded in [third-party notices](../THIRD_PARTY_NOTICES.md).
