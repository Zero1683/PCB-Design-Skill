# Electrical review beyond DRC

DRC checks configured geometric/connectivity rules. It does not establish regulator capability, logic compatibility, thermal margin, PDN impedance, or signal integrity. Select analysis appropriate to the circuit and record assumptions, sources, operating corners, units, methods, margins, and unresolved items before fabrication.

## Separate the questions

| Question | Analyze | Evidence and boundary |
|---|---|---|
| Can the source supply the board? | Rail-by-rail steady/startup/burst budgets at minimum/nominal/maximum input; cascaded conversion losses | Actual component limits and efficiency curves; do not sum currents at different voltages |
| Is voltage adequate at the load? | Forward and return resistance, contacts, switches, vias, narrow escapes; I × R drop | Geometry and temperature assumptions; include supply tolerance, dropout, load minimum voltage |
| Will parts overheat? | LDO/switcher/trace/resistor/diode losses, ambient, derating, thermal paths | Manufacturer models and layout conditions; package theta-JA alone does not describe every PCB |
| Will load steps disturb the rail? | Allowed droop, current step/rise time, effective capacitance, ESR/ESL, regulator response and stability | First-order estimates inform selection; actual Z(f), ringing and loop behavior require appropriate models/tests |
| Does USB or another interface need controlled impedance? | Actual stackup, width, edge spacing, reference plane, coplanar clearances and transitions | Applicable calculator/field solver; a DC resistance calculation cannot answer this |
| Will signals meet pin specifications? | VOH/VOL versus VIH/VIL, absolute maximum ratings, power-off injection, pull-up currents, RC timing | Exact IC/module data, corners, level shifting where needed |

## Calculations the agent should do

Use code or a suitable verified calculator for available arithmetic. Do not ask a beginner to perform calculations the agent can reproduce.

- Conversion: `Pout = Vout × Iout`, `Iin ≈ Pout / (Vin × efficiency)`, `Ploss ≈ Pout × (1/efficiency − 1)`. Apply at relevant operating points and check quiescent/startup terms separately. Never use an advertised peak switch current as the board's output rating.
- LDO: `Ploss ≈ (Vin − Vout) × Iout + Vin × Iq`; compare input headroom against worst-case dropout. Check thermal conditions and required input/output capacitors.
- Uniform trace DC resistance: `R = rho × length / (width × thickness)` using consistent SI units and copper resistivity at the evaluated temperature. Sum **both forward and return paths** plus contact/via/component resistances; derive `Vdrop = I × R` and `Ploss = I² × R`. This does not calculate allowable temperature rise or AC impedance. For planes or parallel paths, use a suitable model rather than pretending all geometry is a series trace.
- Load-step target: allocate allowable **dynamic** droop after DC tolerance/drop budgets, then use `Ztarget ≈ ΔV / ΔI`. State the relevant frequency range and load-step assumptions. This is a design target, not the actual PDN impedance.
- Simplified capacitor budget: reserve `ΔI × ESR` and `ESL × ΔI / rise_time` from allowed droop; for a constant current deficit until regulator response, estimate `Ceff ≥ ΔI × response_time / remaining_droop`. If no positive budget remains, increasing capacitance alone cannot satisfy that model. Effective capacitance includes DC bias, tolerance, aging and temperature. Do not invent response time or assume the full deficit persists in every regulator.
- Check inductor saturation/RMS/ripple, switching current, feedback dividers, LED/resistor dissipation, I²C rise time and sink current, boot/reset levels and timing, ADC input range and settling, as applicable, from the selected parts' models and equations.

Run `python scripts/electrical_calcs.py --input <project-calculations.json>` for reproducible converter, LDO, series DC path and simplified transient arithmetic. Start from [the example](../assets/electrical.example.json), replace every demonstration value and source, and save input plus output under the project baseline. Output is `CALCULATED`, never automatic electrical PASS. Negative margins and infeasible budgets require design changes or explicit disposition. The helper does not solve current capacity, thermal equilibrium, regulator loop stability, PDN frequency response, or transmission-line impedance.

## Missing inputs and manual calculator handoff

First extract accessible geometry and exact datasheet values. If the fabricator's stackup or an instrument measurement is unavailable, request only those missing facts. Do not substitute a prior project's values.

When a required calculator is inaccessible to the agent, provide a ready-to-enter table:

| Field | Value with units | Source | Status |
|---|---|---|---|
| Calculator/model and version | Exact model, e.g. outer-layer coplanar differential | Fabricator page/model | confirmed or unresolved |
| Stackup | Signal/reference layers, dielectric height, Dk/frequency, finished copper, mask assumptions | Actual fabrication stackup | confirmed or unresolved |
| W / S / left D / right D | Measured dimensions and variation | Current PCB geometry | measured or assumed |
| Target and tolerance | Protocol/design criterion | Applicable requirements | confirmed or unresolved |
| Requested result | Calculated impedance and capability warnings, screenshot/export | User-operated calculator | pending |

Explain which button/action computes the result and what to return. Do not tell the user to “calculate impedance” without inputs. Asymmetric or changing geometry needs an applicable model or segmentation, not an invented weighted average. If a required model cannot be evaluated, mark that item BLOCKED or an explicitly accepted limitation; do other independent work. Do not claim an impedance-controlled fabrication result before the fabricator confirms the stackup/process/service.

For oscilloscope or physical measurements, supply accessible test points, instrument setup, supply/load conditions, acceptance criteria, and next branches. A design-only request ends with a first-board test plan and clearly labeled unmeasured items.

## Calculation records and review

Use separate checklist rows for power budget, DC drop, component/thermal margins, dynamic-PDN analysis, logic/boot, and signal impedance. Keep calculation evidence separate from G8 physical measurements. Record baseline, actual input sources, formula/model, result, limit, margin, reviewer conclusion, and limitations. Every layout/stackup/part change invalidates the affected calculation inputs until reviewed.

Validate exported normalized schematic/PCB/BOM records with [the comparison helper](10-validation-tools.md), then review actual EDA connectivity and manufacturing output. A correct equation with guessed geometry is not a verified design.

## Method references

Checked 2026-09-21. Apply methods to the selected parts; example processor limits are not universal values.

- [TI, PDN implementation and analysis, SPRAC76H, sections 4–5](https://www.ti.com/lit/an/sprac76h/sprac76h.pdf): static voltage drop and dynamic impedance budgeting.
- [Analog Devices, AN104](https://www.analog.com/media/en/technical-documentation/application-notes/an104f.pdf): load-step behavior and capacitor parasitics.
- Exact regulator, capacitor, inductor and load datasheets define the project's limits and required models.

## Physical screening calculations

The same helper also accepts `mask_pair`, `escape_channel` and `annular_ring` inputs
from [the fabrication example](../assets/fabrication-calcs.example.json). Read
[engineering constraints](19-engineering-constraints.md) for formulas, tolerances,
per-side dimensions and geometry limits. Results remain CALCULATED; positive margins
do not establish fabrication acceptance, complete fanout or thermal performance.
