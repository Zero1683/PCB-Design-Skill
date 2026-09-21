# G3-G4: Placement, routing, ground copper, and signal integrity

## Set manufacturing rules first

Read the selected fabricator's capabilities and tolerances for the intended process. Set trace width/clearance, drill, annular ring, copper-to-edge, solder-mask dam, silkscreen, and stackup rules from project requirements and fabrication capability. Do not relax them merely to clear errors. Nominal board thickness differs from dielectric thickness between signal and reference layers; finished outer copper may differ from base copper.

If controlled impedance is required, obtain the fabricator's stackup and calculate preliminary cross-sections before freezing layer count, thickness, and critical placement. Avoid discovering after routing that the required width cannot escape the connector.

## Placement order

1. Fix the outline, mounting holes, connector mating faces, button access, antenna, and keepouts. Document allowed overhang; do not reject every component extending past the outline.
2. Place connectors, MCU/modules, and mechanically constrained parts. Check cable insertion/removal, screw-tool access, adjacent plugs, and enclosure clearance.
3. Place inductors, input/output capacitors, and feedback parts around power ICs using manufacturer layouts. Preserve critical loops; long routing cannot compensate for distant components.
4. Place sensors, decoupling, bias/pull resistors, and interface protection. Record sensor axes and mounting rather than optimizing only the plan view.
5. Reserve channels for power, differential pairs, and required signals before filling remaining space. Single-sided assembly does not prohibit all bottom-layer signals, but prioritize a continuous reference ground.
6. Check silkscreen, polarity, reference-designator association, and probe access before extensive routing.

## Check actual geometry

Establish internal units, origin, rotation convention, and mirroring before transforming library coordinates into board coordinates. Verify with a known-size component. Bottom-side transforms require more than changing one sign.

Obtain copper pads, body/assembly outline, courtyard, silkscreen, and height for each component. Record sources and missing fields. Bounding boxes provide a conservative first pass; rotated parts and polygons may require exact-contour review.

Report suspected overlapping reference-designator pairs, clearance, location, and screenshots. Reporting only “49 components placed” is insufficient. Unavailable or unparsed footprints remain unchecked rather than having zero occupied area.

Additional assembly checks:

- Four pads from two adjacent two-terminal parts must not look like alternative pairings. Increase spacing, rotate parts, or provide a clear assembly drawing.
- Keep reference designators associated with the correct part and visible around connectors. Indicate top view and board orientation.
- Connector pin 1, latch, and polarity marks must agree with electrical pin order. Wire colors are only supporting cues.
- Expose critical EP/LGA nets through same-net resistors, capacitors, vias, or test pads where hidden terminals cannot be probed.
- For hot-plate assembly, consider bottom-side through-hole leads, already soldered plastic parts, and contact with the heating surface.
- If 3D models are missing, review dimensional envelopes and report that complete 3D assembly validation remains unfinished.

## Routing priorities and loops

Generally route switching-power loops, critical clocks/differential pairs/sensitive analog signals, then power trunks and ordinary control signals. Adapt this order to the project.

Follow the specific IC's requirements for high-di/dt loop minimization, input-capacitor returns, PGND/signal-ground relationships, thermal pads, and feedback sensing. Do not sense feedback at arbitrary noisy points or points with high-current voltage drop. Keep switch nodes compact rather than treating them as large ordinary power pours.

Evaluate widths against current, copper thickness, temperature rise, and allowed voltage drop. Check the narrowest necks, via count, and connectors; a wide trunk does not compensate for long narrow fanouts. Evaluate short narrow escapes using their actual length and load rather than requiring one width everywhere on the net.

Review the complete power-pin/capacitor/ground decoupling path, not only component separation. Account for high-frequency return current; do not split analog/digital grounds in a way that breaks critical returns.

Treat autorouted traces as candidates requiring power-path, layer-transition, reference-ground, impedance, and assembly checks. Do not claim automatic routing when the available tool does not provide it.

## Ground pours and vias

- Assign pours to the intended ground net and preserve manufacturer antenna and other keepouts.
- Connect top and bottom ground where appropriate. Check islands, narrow necks, ineffective thermal-relief connections, and return-path detours.
- Provide appropriate nearby return paths for signal layer changes; do not scatter ground vias arbitrarily.
- Via-in-pad decisions depend on filling, capping, plugging, and assembly requirements. Do not claim polygon pads are free of solder-wicking risk without the relevant checks.
- After routing, rule, or keepout changes, rebuild pours, read back actual copper edges and nets, and run full connectivity checks.

## USB and other controlled-impedance interfaces

Record protocol and speed. Derive impedance, tolerance, length, and mismatch requirements from the relevant standard and manufacturer guidance. A 90 Ω USB target applies to particular interfaces, not every differential pair.

For each calculated segment, record:

| Parameter | Required detail |
|---|---|
| Layer/model | Microstrip/stripline/coplanar; single-ended/differential; actual signal and reference layers |
| Stackup | Dielectric thickness, applicable frequency for Dk, copper thickness, solder-mask and other model assumptions |
| W | Actual copper width, units, and whether both traces have equal width |
| S | Edge-to-edge spacing, not center pitch |
| D | Left/right same-layer copper-edge clearance; symmetric or asymmetric |
| Reference ground | Continuity, width, slots, other signals, and antipads |
| Extent | Start/end locations, length, and variation covered by the cross-section |
| Transitions | Pads, series resistors, protection devices, vias, layer changes, and stubs |

Do not replace nonuniform impedance analysis with averages of left/right clearance or length-weighted averages. Symmetric calculators apply only when the actual geometry sufficiently meets their assumptions. If field solving is unavailable, align the main routed section with an applicable model and explicitly identify transition limitations.

Geometry iteration:

1. Save the pre-edit snapshot and actual existing cross-section.
2. Calculate candidate geometry with the correct fabricator stackup; label estimates and targets.
3. Adjust width, edge spacing, copper clearance, and necessary return paths.
4. Maintain clearances with appropriate pour rules/local constraints so repouring preserves them.
5. After repouring, measure actual copper edges at multiple points, including corners and transitions.
6. Save calculator inputs, results, covered length, and structures outside the model.
7. Report cross-section calculation, fabricator manufacturability/impedance-service confirmation, physical communication tests, and TDR/eye-diagram/compliance tests separately. They are not interchangeable.

A green calculator result does not establish that fabrication includes impedance testing. Resolve capability warnings separately. If the differential geometry is known to be substantially mismatched and lacks justification, do not claim the target is met because the user accepts “close enough.” An authorized experimental prototype may proceed with explicit risks.

## Final static checks

After repouring, run applicable whole-design DRC/ERC and unrouted-connection checks. Save rules, exemptions, and full results. Compare netlist, PCB, and BOM component by component and pin by pin. Geometric scripts supplement the EDA connectivity graph; segment-endpoint matching alone misses trace overlap with pads and pours.

Connectivity conclusions require actual EDA connectivity data or trustworthy analysis. Missing API returns, nulls, and timeouts differ from a successful empty error list.

Save and reread or reopen the checked design. A subsequent component or trace move invalidates affected checks; do not reuse the earlier final-inspection conclusion unchanged.
