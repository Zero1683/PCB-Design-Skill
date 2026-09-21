# {{PROJECT_NAME}}: PCB Project Requirements and Design Baseline

Created: {{CREATED_UTC}}

Blank fields are unresolved, not implicitly passed. Complete the applicable rows and remove inapplicable rows according to the project scope. Give units and sources for every numeric value.

## 1. Scope and Authorization

- Current task mode:
- Changes authorized for this task:
- Changes explicitly prohibited:
- Authorization to order, pay, or publish (record its source, if applicable):
- Current stage: G0
- Project working directory, tools, and versions:
- Current authoritative design baseline ID:
- Manufacturing package, order, and hash already submitted (write “not ordered” if none):
- Physical board ID and assembly revision (write “not built” if none):

## 2. Requirements and Constraints

| ID | Requirement or parameter with units | Status: confirmed/proposed/unknown/superseded | User or document source | Design impact |
|---|---|---|---|---|
| REQ-01 | Functions, response, and communication | unknown | | |
| REQ-02 | Input supply range and peak load | unknown | | |
| REQ-03 | Board outline, hole locations, and assembly envelope | unknown | | |
| REQ-04 | Layer count, stackup, board thickness, and copper thickness | unknown | | |
| REQ-05 | Assembly side, minimum package size, and available tools | unknown | | |
| REQ-06 | Programming, recovery, and test points | unknown | | |
| REQ-07 | Budget, quantity, manufacturing process, and deliverables | unknown | | |

## 3. Power States and Budget

| Input/USB/battery/switch/debugger combination | Current source and path | Powered rails | Charging and backfeed behavior | Expected MCU state | Physical measurements required |
|---|---|---|---|---|---|

| Load or rail | Input range | Steady-state/peak/startup current | Efficiency or voltage-drop assumptions | Component and thermal margins | Source |
|---|---|---|---|---|---|

## 4. Critical Components and Footprint References

| Reference designator | Manufacturer/full part number/supplier part number | Datasheet revision and section | Electrical selection rationale | Recommended land pattern vs. library dimensions | Open items |
|---|---|---|---|---|---|

## 5. Pin Mapping and Accessible Measurement Paths

| Function | Reference designator and package pin | Chip GPIO/net name | Direction and startup level | Connector pin order/polarity | Accessible alternative test point | Firmware definition |
|---|---|---|---|---|---|---|

## 6. Manufacturing and Assembly Parameters

- Fabricator, process specification revision, and date accessed:
- Board outline and component overhang:
- Actual stackup, copper thickness, and dielectric parameters:
- Minimum trace width/spacing, hole size/annular ring, copper-to-edge clearance, solder-mask rules, and silkscreen rules:
- Special holes/slots, antenna keepouts, and mechanical keepouts:
- Controlled-impedance model, dimensions, applicable sections, and transitions not covered:
- Surface finish, stencil side/thickness, and special apertures:
- Assembly sequence, polarity drawing, through-hole parts, and heating-tool limitations:

## 7. Acceptance Criteria

Define these before testing; record details in CHECKS.csv. Checks requiring an unavailable physical board or instrument remain untested.

| Function or operating condition | Measurement method/instrument/test point | Load and supply | Acceptable range/repetitions/duration | Raw result file |
|---|---|---|---|---|

## 8. Changes, Issues, and Reduced Functionality

| Date | Previous baseline → new baseline | Change and reason | Affected files/checks | Source of user decision, if required |
|---|---|---|---|---|

| Issue | Facts and evidence | Hypothesis | Next test to distinguish possible causes | Accepted limitations and their sources |
|---|---|---|---|---|

## 9. File Locations

- Source project and required component libraries:
- Schematic, PCB, netlist, and BOM:
- Actual manufacturing package, stencil, placement data, and assembly drawing:
- DRC/ERC results and rules:
- Firmware, programming scripts, and recovery procedure:
- Checklist: CHECKS.csv
- Handoff: HANDOFF.md

## 10. Delivery Scope and Calculations

- Requested stopping stage (default for design: G5):
- Ordering responsibility (default: user):
- Calculation inputs, sources, output and margins:
- Native API probe and any operation-specific UI fallback:
- Routing strategy and preserved critical nets:
