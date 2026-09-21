# User instructions, observed work, and reusable rules

This case concerns the design and debugging of an elongated board using ESP32-C3, LSM6DS3TR-C, and TPS63021. These decisions can be applied without the original conversation, machine paths, or previous agent context.

## Convert requests into workflow requirements

| User request or feedback | Work or issue observed | Reusable rule |
|---|---|---|
| Why reject the default pads? I want to verify them myself. | Custom and library L1 geometry differed; the default was rejected prematurely | Provide manufacturer lands, both pad geometries, and reasoning that can be recalculated; do not defend a prior conclusion without evidence |
| Use recommended parts; can this be done in bulk? | The component manager replaces selections with a target device | Group by identical part number; do not apply one replacement to heterogeneous parts |
| No bottom components; use stencil and hot plate | Top-side assembly still had through-hole leads | Record side and tools, consider later through-hole soldering and underside contact; this does not require single-layer copper |
| 24 x 70 outline, radius 1; leave routing room | Narrow board, antenna overhang, constrained routing | Lock mechanics and antenna first, reserve critical channels, and do not arbitrarily widen the board |
| The components all overlap | Early automated placement lacked adequate checks | Validate real footprint outlines, rotation, spacing, and actual screenshots before calling placement complete |
| Routing is done; do not change it yet | Read-only review required | Record issue locations and evidence; do not repour/save or optimize without appropriate authorization |
| Fix U4 power; handle USB directly | Authorization first covered local areas, then expanded | Back up each iteration, bound changes, check interfaces and nearby nets, avoid unrelated edits |
| Check everything and confirm it runs | DRC/netlist checks were possible before a board existed | Separate static, transient-power, communication, assembly, and firmware tests; label actual coverage |
| 1.6 mm, 1 oz | Nominal manufacturing conditions fixed | Obtain actual stackup before impedance calculation; nominal board thickness is not dielectric height |
| Average D1; later, make D1 uniform | Asymmetric ground clearances were later standardized locally | Do not validate the whole path with an average; repour and sample actual edges at multiple locations |
| Separate stencil, OSP, self-assembly | Fabrication, stencil production, and assembly were separate | Use one baseline for all files and document aperture orientation/process; fabrication alone is not assembly |
| Paste bridges will disappear on heating | Fine-pitch hidden-joint bridging risk | Inspect paste before reflow; surface tension does not guarantee excess solder will separate |
| Inaccurate hot-air temperature; small plate | Rework and sectional heating were constrained | Plan around actual measurement/heating conditions; avoid universal temperatures and fixed durations |
| Pads are hidden under the part | Critical U1/U2 terminals inaccessible | Identify exposed same-net points and design test access; do not repeatedly request hidden-pad probing |
| The switch pads stay shorted; the button is fine | EN remained short with button removed and cleared after module removal | Compare bare board, removed parts, and same-net measurements to isolate design versus assembly |
| Correcting resistor orientation changed behavior | R17/R18 pad pairs were confused and previously called R16 | Verify designator, pin, net, and photo; discard uncertain labels and improve assembly drawings |
| CH340 claims 3.3 V support but measures 3.8 V | Supply selection might not change logic levels | Measure TX, check IO specifications and power responsibility; seller confirmation is insufficient |
| Use native USB for everything from now on | Programming and web access moved from FT232 | Identify ports by device identity, migrate all clients, and release port ownership; do not hard-code COM30 |
| Stop interrupt testing; polling is acceptable | I²C worked; interrupt output was unresolved; polling used | Honor accepted reduced scope, avoid pointless rework, and do not claim interrupt/deep-sleep validation |
| Package software, algorithms, and instructions | Reproducible complete delivery needed | Distinguish source, project, manufacturing, BOM, firmware, test points, limits, and licenses; exclude caches and credentials |

## Boundaries of the examples

1. **L1 footprint:** custom pads were 1.0 x 2.9 mm at 1.9 mm center pitch; default pads were 1.3 x 3.0 mm at 2.1 mm pitch. This establishes a geometric difference, not which is wrong. Check the new project's manufacturer datasheet.
2. **USB cross-section:** the case used a nominal 1.6 mm board. A later uniform straight section used W = 0.80 mm, S = 0.35 mm, and D = 0.30 mm on both sides; the calculator showed about 92.4 Ω. There was no whole-route TDR evidence, and transitions were outside the uniform model. These dimensions are not a universal 90 Ω recipe. The 1.6 mm value is board thickness, not the modeled segment length.
3. **Resistance versus shorts:** two boot nets each pulled up through 10 kΩ to one rail can read about 20 kΩ between them. In the case, resistance near the shorted-probe baseline supported a hard-short diagnosis. A hot board, powered measurements, and in-circuit capacitors alter readings.
4. **Conflicting records:** the interrupt changed from GPIO6 to GPIO1. At the 3.0 V input setting, an initial output reading was 3.20 V; later two-point measurements were 3.329 V. Retain the correction source instead of repeating obsolete values.
5. **Manufacturing identity:** the stored 24 x 70 mm outline conflicted with a later stated 24 x 76 mm size; manufacturing Gerbers and editing snapshots also had different dates. Match the object and files rather than simply choosing the latest.
6. **Firmware can cause interface faults:** a USB echo failure at fixed packet boundaries was later corrected through ZLP handling. Enumeration or programming does not validate arbitrary application transfers, and application failure does not necessarily implicate PCB hardware.

## How evidence developed

During design, netlist, DRC, and geometry checks supported engineering prototyping.

During assembly, comparisons and rework resolved EN and boot-pin shorts. These faults also exposed assembly-usability weaknesses in the layout and should not all be attributed to the user.

Basic functional evidence covered identity reads, IMU self-test and continuous sampling, buttons/LEDs, multiple input voltages, verified bidirectional USB data, and some wireless round trips. It did not establish full impedance compliance, long-term runtime, or interrupt wake-up.

Before extending results to another board, battery, firmware, or enclosure condition, assess and retest affected items. Preserve actual limitations so subsequent decisions remain valid.
