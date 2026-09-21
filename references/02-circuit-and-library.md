# G1-G2: Architecture, parts, schematics, and footprints

## Sources and component selection

For critical parts, record manufacturer, full part number, package suffix, supplier code, datasheet revision/date/page or section, and source URL. Prefer manufacturer datasheets, errata, and reference layouts. Seller descriptions support procurement but do not replace electrical specifications.

Compare proposed substitutes for operating voltage, logic levels, capacitance/resistance, tolerance, voltage rating, temperature, maximum/continuous/peak current, losses, pinout, physical dimensions, and availability. Check current stock and pricing with a timestamp; a published starting price is not a quote for the required small quantity.

For similarly named diodes, protection arrays, regulators, and compatible parts, use the actual manufacturer's specifications rather than another brand's datasheet.

## Power design

1. Budget steady-state, startup, and burst loads such as radios or motors. Calculate each cascaded regulator's input and output rather than summing load currents directly at the battery.
2. Select LDO, buck, boost, buck-boost, or another topology from the supply range. Estimate `Iin ≈ Vout × Iout / (Vin × efficiency)`, state the efficiency assumption, and account for current at minimum input voltage.
3. Check ratings and derating: inductor saturation and RMS current, MOSFET/IC switch-current limits, connectors, battery capability, effective input/output capacitance, voltage drop, and thermal loss.
4. Distinguish IC switch-current limits from sustainable board output current, which also depends on input voltage, efficiency, temperature rise, copper, and other components.
5. Check VIN/VOUT/FB/EN/PGND/AGND/EP/PG/synchronization pins individually. Fixed and adjustable versions are not interchangeable. Auxiliary supply pins may have internal connections; follow manufacturer instructions rather than adding intuitive connections.
6. Identify how reverse polarity, overcurrent, charging, overdischarge, and back-powering are handled. IC UVLO is not automatically battery protection. Document the usage boundary for omitted functions instead of claiming they exist.
7. For ADC dividers, check maximum input, tolerances, ADC limits, source impedance, and RC settling. Record calibration. Voltage alone does not establish an accurate state-of-charge percentage.

Produce the power tree, state table, budget, and reproducible calculations. List measurements separately.

## MCU, boot, and recovery

- Check bare-chip and module requirements separately for clocks, flash, RF, and decoupling; do not duplicate circuits already inside a module.
- Record boot-strap states at power-up, reset, and programming. Check whether LEDs, buttons, sensors, or dividers alter sampled levels.
- Use the specific device's reset-RC and sequencing requirements. Make reset wiring, pull-ups, capacitors, and debug connections measurable.
- Choose GPIOs supporting the intended wake mode. Ordinary interrupt capability does not establish deep-sleep wake capability.
- Provide at least one recovery programming path appropriate to the device. Native USB and USB-UART adapters are separate devices; adapter enumeration does not prove the target booted.
- Maintain a pin table with reference designator, package pin, GPIO, net, direction, startup level, external connection, and firmware definition. Keep package pin numbers separate from GPIO numbers.

## Sensors and buses

Check VDD/VDDIO, power sequencing, mode and address selection, bus pull-ups, unused-pin treatment, decoupling, measurement range, and sampling rate. An I²C address is not an identity-register value; ACK alone does not validate all sensor axes.

For interrupts, record INT1/INT2, open-drain/push-pull mode, polarity, latched/pulsed behavior, clearing conditions, receiving GPIO, test point, and software registers. Treat unused auxiliary pins as the manufacturer specifies rather than universally floating or grounding them.

## Interfaces and indicators

- USB: establish speed and role. Check D+/D−, CC, SBU, VBUS, shield, protection arrays, and series resistors against the actual interface requirements. Do not reuse a USB 2 device's CC arrangement for PD or Host by assumption.
- UART: define target logic levels, crossed TX/RX, common ground, flow control, and power responsibility. A 3V3 supply output does not establish 3.3 V TXD levels; a jumper may switch power only.
- Connectors: document pin order, mating direction, latch orientation, and cable wiring. Matching housings do not establish matching wiring.
- LEDs: verify A/K or manufacturer polarity; pin 1 is not universally the same polarity across libraries. Choose resistance from supply voltage, forward drop, and target current.
- Buttons: verify the internal contacts. Do not infer same-side continuity from a two- or four-pin housing. Specify pulls and debounce.

## Four-way footprint mapping

Verify **symbol pin → PCB pad number → physical terminal → datasheet view**.

For every critical footprint, record:

| Field | Check |
|---|---|
| Datasheet view | Top/bottom view, pin-1 reference, rotation direction |
| Geometry | Body, terminals, recommended lands, clearances, hole diameters, pitch, overhang |
| Process layers | Copper, solder-mask openings, stencil apertures, silkscreen, assembly outline; each has a different role |
| Thermal/ground | EP and duplicate ground-pad numbers/nets, aperture segmentation, and solder-wicking effects of vias |
| Model | Orientation and height support assembly review but do not replace the land pattern |
| Tolerances | Manufacturer minimum/nominal/maximum dimensions versus manufacturing capability |

Use consistent units: `1 mil = 0.0254 mm`. Distinguish edge clearance from center pitch. Calculate unequal left/right pad widths separately. Surrounding silkscreen is not the component body outline.

### Library versus custom footprints

Compare both alternatives against manufacturer lands and the assembly process before choosing. Identify exact matches, process allowances, and unsupported dimensions.

Larger pads may improve joint visibility but also change solder volume, bridging risk, parasitics, and assembly clearance. “Slightly larger is always fine” is not a general rule. Replace a library footprint with a custom one only when dimensional and process evidence supports it.

Group bulk substitutions by exact part number. Do not select heterogeneous devices and replace all with one target. Check nets, pins, BOM, footprints, and electrical properties before and after replacement. Verify actual tool behavior when preserving reference designators or unique IDs.

## Schematic/PCB consistency

Use real connections and netlists, not visually crossing lines. Check incorrect or truncated net labels, identically named power domains, hidden power pins, NC pins, and duplicate pads.

- Compare instance reference designators, part numbers, values, fitted/BOM status, and pin nets.
- Define explicit treatment for NC, mechanical pins, multiple physical pads sharing a number, and DNP components. Pin-count differences alone do not establish an error.
- Re-export the netlist and BOM after removing a functional block; check obsolete nets and dangling endpoints.
- Inspect individual ERC/DRC warnings, not only counts. Property-standardization messages differ from electrical disconnections.
- Do not remove real errors by disabling rules, expanding exemptions, or assigning false NC markers.

G2 passes when critical electrical connections and pins have manufacturer support, critical footprints have dimensional evidence, netlists and BOM agree, and rule violations are resolved or have specific applicable exemptions. Unreadable footprints and unperformed checks remain unverified.
