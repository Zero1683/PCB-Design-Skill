# G5-G6: Manufacturing release and assembly

## Freeze a traceable revision

Before fabrication, save the native project and required libraries, schematics, PCB, netlist, BOM, and check results with a revision/baseline ID. Changed record order with unchanged semantics is not necessarily a design change, but different bytes cannot have an assumed identical hash. Record semantic comparison separately from byte hashes.

Select deliverables for the intended use:

| File | Verify |
|---|---|
| Native project/libraries | Reopens in the intended tool; exchange snapshots are not complete native projects |
| Gerber/ODB++ and drill files | Match the frozen PCB, with outline, copper, mask, silkscreen, and drilling |
| BOM | Fitted reference designators, quantities, full part numbers, specifications, packages, DNP status, substitution limits |
| Placement file | Required for factory placement; origin, units, side, and rotation convention agree |
| Stencil | Assembly side, aperture geometry/orientation, thickness, special EP apertures |
| Assembly drawing | Pin 1, A/K, latch, polarity, adjacent pad pairings, DNP, staged soldering |
| Fabrication notes | Stackup, board/copper thickness, tolerances, finish, special holes/slots/impedance |
| Inspection/test instructions | Reviewed scope, accepted limitations, first-board test points, recovery programming |

Do not send conflicting revisions for the fabricator to choose between. Label historical files explicitly and keep one identifiable current set in the release package.

## Independently review manufacturing files

Reopen exports in a manufacturing viewer and check at least:

- closed outline, dimensions, corner radii, and slots; no duplicate outline or silkscreen used as outline;
- copper-layer count, top/bottom orientation, copper-to-edge clearance, reference ground, and keepouts;
- drill units, PTH/NPTH, tooling/mounting holes, and pad alignment;
- mask openings, fine-pitch mask dams, and via-tenting requirements;
- stencil apertures, assembly side, and large-pad segmentation;
- legible silkscreen clear of pads, with explicit polarity;
- copper, pads, protection, series resistors, and power structures matching the final PCB.

Archive existence or file count is insufficient. Without a manufacturing viewer, mark preview incomplete and continue other preparation; do not claim all DFM checks passed.

Use project requirements for order parameters rather than copying old screenshots. Choose finish for assembly and storage conditions; OSP, HASL, and ENIG have no universally best choice. Recheck affected impedance and assembly if the fabricator changes stackup or process.

After authorized upload, save the uploaded package hash, order ID/preview, and parameters. Before upload, call it a package awaiting ordering. Without order evidence, do not describe subsequently found historical Gerbers as the submitted files.

Use `scripts/release_manifest.py` on a separate frozen release directory. It cannot validate electrical correctness or semantic consistency across files. Review first, then hash. Later changes require a new revision; do not recompute hashes to conceal unreviewed edits.

## Incoming inspection and assembly preparation

Normally complete one testable board before assembling the batch, unless the user already specified a process or batch plan. Check bare-board revision, critical dimensions, damage/contamination, and connector holes. Compare physical part labels with the BOM and record substitutions.

Group small parts by reference designator and provide a top-view assembly drawing showing labels, real pad pairings, and orientation. Avoid ambiguous references such as “the upper-left one.” Color and connector notches are supporting cues; determine pin order from the circuit and measurements.

For paste printing, secure and align board/stencil at all fine pads with flat support. Inspect for offset, omissions, excess paste, and continuous bridges. Correct clear defects before reflow; surface tension is not a guarantee of self-correction.

Check IC pin 1, LED A/K, polarized parts, and connectors during placement. Center gently. Do not press a module while solder is molten, which can squeeze solder underneath, bridge pads, or cause floating.

## Reflow and hand-tool limitations

Base the profile on the exact solder-paste alloy/process documentation and component thermal limits. Record how temperature is measured. Melting point is not a whole-board hot-plate setpoint; hot-air settings, plate temperature, and actual joint temperature differ. Without measurements, do not claim strict compliance with a reflow profile.

For sectional heating on a small plate, assess support, thermal uniformity, copper heat sinking, modules spanning hot/cold boundaries, reheating of completed regions, and plastic temperatures. Nonoverlapping component placement does not imply thermally independent passes. If hidden critical joints cannot reflow uniformly, propose a suitable heat source, fixture, or staged assembly process; do not guarantee two-half reflow reliability.

Schedule through-hole/tall plastic connectors appropriately, often after reflow, to preserve plate contact. Verify each part's reflow rating rather than treating all connectors alike.

Before rework, disconnect all supplies and let the board cool. Use suitable flux, controlled airflow, protection for adjacent parts, and moderate cleanup. Raised solder does not establish correct volume; leveling solder is not scraping copper away. Use accessible same-net points to localize faults before removing hidden-joint parts where possible, reducing repeated rework.

After soldering, inspect visible joints under magnification for misalignment, tombstoning, bridges, pad damage, and connector orientation. Invisibility of underside joints does not establish absence of shorts; use electrical tests, a comparison board, or suitable inspection as needed.

## Assembly records

Assign each board an ID and record manufacturing revision, assembly revision, substitutions, reworked areas, date, and photos. After full cooling, disconnection, and confirmation that relevant rails have discharged, proceed to [power-up and debugging](05-bringup-debug.md). Without a physical board, G6 remains untested; assembly instructions do not establish completed assembly.
