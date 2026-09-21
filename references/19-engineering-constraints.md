# Engineering constraints and source review

Use this reference when adopting an external design recipe, reviewing dense escapes,
or defining stackup, timing, thermal and manufacturing constraints. Apply relevant
checks within G1-G5; ordinary boards do not automatically need BGA, FPGA or SI simulation.

## From a claim to an implemented constraint

Treat an article, generated example or reference board as a lead. Before using a
design-critical number, resolve it to the exact part/package/revision or the selected
fabrication process. A cited document must contain the claimed table or requirement;
a familiar document number and an expert-role prompt are not verification.

Use the constraint table in PROJECT.md, with one row per critical rule or grouped
equivalent rules. Record units and whether a dimension is per-side, total, nominal,
minimum or maximum. Separate operating limits from absolute maximum ratings.

1. G1/G2: identify exact endpoints, supply domains, operating corners and source.
   Reconcile conflicting sources before implementing the affected connection.
2. G3: establish the applicable stackup/process and calculate physical feasibility.
   Bind constraints to real net/object IDs and native rule settings; a net-name list
   in a prompt is insufficient. Verify rule precedence and scoped overrides by readback.
3. G4: compare actual routed geometry, repoured copper and references against the
   rule. Use a manual or external check for an unsupported EDA constraint and retain
   its output. Never invent a native rule or menu entry.
4. G5: inspect exported geometry and fabrication notes against the same baseline.
   Later CAM/stackup/process changes reopen affected checks and exports.

Mark missing design-critical input BLOCKED for that item, with a specific next step;
continue independent work. A proposal is not a confirmed fabrication capability.
Do calculations with available tools; ask the user only for inaccessible inputs or
measurements. No mandatory human calculation or full simulation for every design.

## Power, startup, clocks and package selection

- Establish a reproducible startup, reset and recovery path appropriate to the exact
  device. JTAG and SWD are different protocols; a connector's pin count does not make
  it compatible. Verify the programmer pinout, VTref, voltage and reset behavior.
- For multi-rail devices, check every supply/bank voltage, ramp and sequencing limits,
  configuration straps, configuration-memory capacity and programming pin mapping.
  Use the device power-estimation model for the implemented resources/activity;
  do not invent a universal maximum current from a configuration manual.
- Check continuous regulator output, dropout, transient response and thermal limits
  together. For illustration, a 600 mA regulator is not a valid 1.2 A rail source.
  A hypothetical 5 V to 1 V LDO at 1.2 A dissipates about 4.8 W before quiescent loss;
  that arithmetic is a rejection clue, not a claim that a chosen part can operate there.
- Verify decoupling against each applicable supply pin/group and the recommended
  placement/return topology. Missing required decoupling is an electrical defect,
  not a cosmetic ERC warning.
- Resolve package geometry and ball maps from the exact package drawing and pinout
  data, not the configuration guide alone. Pitch does not determine pad shape, ball
  population, or SMD/NSMD construction. Library and custom footprints need the same
  pin-to-physical-terminal review.
- Distinguish a passive crystal from an active oscillator. A clock-capable pin alone
  does not establish an on-chip crystal amplifier. Check oscillator supply/output
  standard or crystal load network and startup requirements as applicable.

## Stackup, timing and dense routing

- Layer roles depend on routes and their returns. A four-layer signal/GND/power/signal
  example is not universally suitable: bottom-layer signals referencing a split
  power layer need specific return-path review. Never substitute overall board
  thickness for signal-to-reference dielectric height.
- Use the fabricator's actual layer construction, dielectric data/frequency, finished
  copper and applicable tolerances. Calculate cross-sections with a suitable solver.
  Record single-ended versus differential targets separately, plus tolerance,
  reference layers, spacing and transition exceptions. No fixed 0.25 mm/50 ohm rule.
- Evaluate edge rate and propagation delay, not clock frequency alone. Derive skew
  budgets from interface timing, topology and endpoint requirements; do not apply
  1 mm matching to all clocks or assume every single-ended clock needs length matching.
  Termination and AC coupling depend on driver/receiver specifications.
- For a straight channel between aligned pads, let pitch be p, projected pad widths
  d1/d2, trace width w and required edge clearance c. Available gap is
  `g = p - (d1 + d2)/2`. For n parallel traces, require
  `n*w + (n-1)*c + 2*c <= g`. Equal-pad single-trace bound is `w <= p-d-2*c`.
  All dimensions must reflect the applicable manufacturing allowance. Diagonal or
  staggered escapes, turns, vias, antipads and plane continuity need separate geometry
  checks. This bound cannot establish whole-BGA routability or select the layer count.
- If escape is infeasible, evaluate placement, legal geometry, layer count and via
  technology, then package choice. Do not lower clearance solely to silence DRC or
  because a signal is described as low speed. Recheck affected electrical/process
  limits and record the basis for any genuine rule correction.

## Thermal paths, relief spokes and manufacturable apertures

- Thermal power uses W, thermal resistance K/W and temperature rise K or degrees C.
  Via current in A cannot be summed into heat-removal capacity. Use package/layout
  thermal guidance and a model matching ambient, copper, airflow and interfaces.
  `Tj ≈ Ta + P*thetaJA` is only a screening estimate under matching boundary conditions;
  thetaJC and characterization parameters are not interchangeable with thetaJA.
- Follow package land-pattern guidance before adding thermal vias. BGA balls are not
  an exposed thermal pad. Check the net of each via, escape/plane effects and whether
  filling/capping or stencil changes are needed to prevent solder wicking. Never add
  a universal array beneath every processor.
- Thermal relief spokes ease soldering and also affect current/thermal paths. Select
  count, width and gap from current, assembly and package guidance; four spokes is not
  an acceptance criterion. Inspect the actual remaining spokes and narrow necks after
  final repour. Removing islands or refilling zones does not fix an undersized hole ring.
- For symmetric per-side mask expansion e, opening width is `pad_width + 2*e`.
  Example: 0.45 mm pad and +0.02 mm per side gives 0.49 mm, not 0.47 mm.
  Two adjacent openings leave `web = pitch - (opening1 + opening2)/2`.
  A larger opening can consume the dam; expansion is not always an improvement.
  Solder-mask-defined pads may need negative expansion and explicit fabrication notes.
  Check the selected process and CAM policy; mask and paste apertures are separate.
- For concentric round lands/holes, nominal ring is `(land_diameter-hole_diameter)/2`.
  A simple eccentricity budget subtracts radial offset from that ring. State whether
  hole dimensions refer to tool/drill or finished plated size, and include tolerances
  according to the fabricator's rule. Slot/noncircular/internal-layer checks need an
  appropriate geometry model. Do not substitute a neighboring pad-overlap explanation.

The sourced-input calculator supports `mask_pair`, `escape_channel` and `annular_ring`:

```sh
python scripts/electrical_calcs.py --input assets/fabrication-calcs.example.json
```

Replace demonstration values and sources before project use. Its geometric margins
are first-order screening, not native DRC, solder yield or fabrication approval.

## Manufacturing findings and bounded repair

Do not disposition findings by red/yellow color. Classify each by affected net/object,
physical consequence and evidence. Shorts, opens, missing required decoupling,
invalid pin/voltage mapping, inadequate return paths and violated applicable process
limits block affected release checks regardless of displayed severity. Exempt a
specific nonfunctional/reporting warning only with a recorded reason and scope;
never globally suppress the class. Existing visual-format gates still apply.

Cluster failures by root cause. Correct the governing footprint/rule/stackup/transform
once, run affected checks and inspect the result. After two ineffective repairs to
the same defect, stop repeating the edit, inspect raw geometry and model assumptions,
and change the diagnosis. Fix copper necks in copper geometry, not by hiding warnings.

Manufacturing output must use agreed layer identities, units, origin and precision.
A closed outline may contain the required nonrectangular contour and cutouts.
Check PTH/NPTH and slots in actual drill data; an optional graphical drill map does
not replace it. Do not require PostScript, one naming convention, or a universal
3:3 coordinate format without fabrication evidence. Proper mil/mm conversion alone
does not imply coordinate loss; compare dimensions and alignment in a separate viewer.

## Sources and applicability

Reviewed 2026-09-21. Use current exact-part/process documents for each project.

- [Diodes AP2112 datasheet](https://www.diodes.com/datasheet/download/AP2112.pdf):
  regulator rating and variant selection, not a universal power-tree recommendation.
- [AMD UG475 package and pinout specification](https://docs.amd.com/v/u/en-US/ug475_7Series_Pkg_Pinout):
  package/ball-map source; configuration and electrical documents serve other purposes.
- [TI high-speed layout guidelines, SCAA082A](https://www.ti.com/lit/an/scaa082a/scaa082a.pdf):
  edge rate, transmission lines and return-path reasoning.
- [AMD thermal solution guidance, XAPP1377](https://docs.amd.com/r/en-US/xapp1377-heatsinks-thermal/Device-Lid-Type-and-Associated-Documentation-Identification):
  package-specific thermal documents and models.
- [KiCad PCB Editor documentation](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html):
  per-side mask expansion and drill-file/map distinction. Version-specific UI is not
  an instruction for EasyEDA; use the selected native backend's documented API.
- [JLCPCB solder-mask-defined pads](https://jlcpcb.com/help/article/how-to-order-boards-with-solder-mask-defined-pads):
  SMD/NSMD distinction and communication of intended mask geometry.

The supplied CSDN article (article/details/165558808) motivated this review, but its
example component choices, fixed fabrication numbers, alleged plugins/UI commands,
model claims and success percentages are not adopted as engineering evidence.
