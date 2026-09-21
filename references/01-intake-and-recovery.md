# G0: Requirements, scope, and context recovery

## Extract confirmed requirements before asking questions

Read the conversation, attachments, and project files. Record parameters as `confirmed / proposed / unknown / superseded`. Do not fill important unknowns with values from a previous case.

| Category | Establish | Design impact |
|---|---|---|
| Function | Inputs, outputs, computation, communication, response time, operating modes | MCU, interfaces, storage, sensors |
| Power | Minimum/nominal/maximum voltage for every input, continuous/peak current, connection combinations | Topology, protection, connector ratings |
| Battery | Chemistry, series count, protection board, pin order, charging method, capacity source | Charging and undervoltage protection; a “14500” form factor is insufficient |
| Mechanics | Outline, corner radii, holes, connector orientation, enclosure clearance, antenna and battery positions | Include the assembly envelope, not just board width and length |
| Manufacturing | Layers, stackup, copper weight, finish, fabricator capabilities and tolerances | Trace widths, clearances, holes, impedance, cost |
| Assembly | Hand soldering/stencil/factory assembly, single/double sided, smallest manageable package | Packages, spacing, test points, assembly order |
| Tools | Multimeter, current-limited supply, oscilloscope, magnification, hot air, heating area | What can be verified locally and what requires external measurement |
| Maintenance | Programming interface, recovery mode, test points, replaceable parts, firmware update | Avoid dependence on a sole unrecoverable operating path |
| Delivery | Prototype quantity, source project, manufacturing package, documentation, license | Do not invent project background or automatically purchase/publish |

Ask only about missing information that changes the current design. Battery series count, whether USB supplies power, and enclosure width may be hard dependencies; solder-mask color usually does not block schematic work. Recommend an evidence-based option, explain its tradeoff, and continue independent selection and documentation checks.

State units and the object being measured: board outline, module overhang, USB shell projection, bottom-side through-hole leads, and complete assembly envelope. Resolve conflicting dimensions from the outline or physical measurement; do not silently replace manufacturing history with a newly spoken number.

## Existing projects

A newer file is not automatically authoritative. Establish authority by purpose:

1. Current explicit user instructions define the permitted edit scope.
2. The submitted manufacturing package and order preview identify the fabricated bare-board revision.
3. The active editable project is the target for design changes and may differ from the fabricated board.
4. Cross-check schematic netlist, PCB data, and BOM; record conflicts explicitly.
5. Physical board ID, rework history, and firmware revision determine which board a test conclusion covers.
6. Historical reports are investigation leads, not inherited PASS results.

If only exchange files or snapshots are available, label them accurately and record missing libraries or project hierarchy. A few screenshots or an isolated `.epcb` file must not be described as a complete editable project.

First produce a project summary. For read-only tasks, report it in the conversation without creating or updating adjacent records. Save it only when writes are allowed:

```text
Mode: read-only review / local revision / new design / manufacturing / assembly / debugging
Authoritative design files and revision: ...
Fabricated boards and manufacturing package: ...
Explicitly protected content: ...
Authorized scope for this task: ...
Known failures and original evidence: ...
Missing information and the step it affects: ...
```

“Optimize everything” does not justify arbitrary chip, pin-order, or mechanical-interface changes. Distinguish authorized optimization from architecture changes that alter use.

## Requirements baseline and changes

For every power, pin, or mechanical change, record reason, old value, new value, affected files, and checks to repeat. Moving a sensor interrupt to a wake-capable pin requires updating schematics, PCB, interface tables, firmware, and tests; changing a label alone is insufficient.

If charging moves off-board, remove the relevant components and check schematics, PCB, purchasing lists, interfaces, power states, instructions, and firmware pins for obsolete functionality. Gaps in reference designators are acceptable; do not renumber a fabricated design for cosmetic consistency.

## Define power states before routing

List every realistic combination, such as battery present/absent, USB connected/disconnected, switch on/off, and debugger connected/disconnected. For each state, specify:

- which input supplies each rail;
- whether the battery charges;
- whether the switch interrupts load current or controls EN;
- possible back-powering through signals when main power is off;
- any paralleled supplies and how contention is avoided;
- whether the MCU should run, remain in reset, or be unpowered;
- measurements required.

A Type-C connector does not establish power input, charging, USB Host, PD, or high-speed USB capability.

## Planning deliverables

Provide a functional block diagram, preliminary power and pin tables, part-selection direction, mechanical sketch, stage order, and unknowns. Define measurable power, response, accuracy, and temperature-rise requirements before testing; do not redefine acceptance to match the result afterward.

A request to design directly authorizes producing these intermediate artifacts within scope without waiting for approval of every table.
