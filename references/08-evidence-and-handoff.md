# Evidence, revisions, and handoff

## Check states

Use these case-sensitive states in `CHECKS.csv`. Add or remove rows to match the task:

- `NOT_RUN`: not yet executed.
- `PASS`: evidence meets predetermined criteria under recorded conditions and scope.
- `FAIL`: executed but criteria not met; record actual values and disposition.
- `BLOCKED`: cannot execute because a specific tool, file, or physical board is unavailable; distinct from tested failure.
- `N_A`: genuinely inapplicable to this design, with a reason. Missing tools do not make a check inapplicable.
- `ACCEPTED_LIMITATION`: the user explicitly accepted unimplemented or insufficiently verified scope; record the acceptance source and impact. This is not PASS.
- `STALE`: a relevant design, process, firmware, or board change requires rechecking.

A stage passes verification only when all applicable required checks are PASS and genuinely inapplicable checks have justified N_A status. Explained FAIL/BLOCKED/NOT_RUN/STALE items still remain failed or incomplete. Accepted limitations may permit a prototype under specified conditions, but must be separate and cannot count as passing the original verification. Do not automatically downgrade FAIL to a limitation. Scope reduction requires an explicit decision and change record.

## Evidence for a passed check

At minimum record check ID, stage, design baseline, board/firmware where applicable, method, conditions, expected criteria, actual result, evidence path, time, and limitations. Example:

```text
USB-TRANSFER / G8 / board-B revC / fw sha256:...
Power: J2 3.7 V; FT232 VCC disconnected; native USB; cable A; Windows host...
Method: bidirectional byte comparison of fixed-seed pseudorandom data, including 63/64/65-byte boundaries
Criteria: zero mismatches over the project's predetermined byte count/repetitions; record reconnects and errors
Actual: ...; raw data: evidence/...json
Limitations: does not establish TDR, eye-diagram, or USB compliance certification
```

Words such as “final” or “passed” in a filename are not evidence. User measurements are valid evidence when labeled as user-reported with test points and conditions; do not present them as direct agent instrument measurements. Clarify missing units or ambiguous points instead of guessing between mΩ and MΩ.

## Evidence invalidation after changes

| Change | Reassess at least |
|---|---|
| Part/footprint/library standardization | Electrical specifications, pins, dimensions, nets, placement, BOM, assembly, DRC |
| Component movement/routing/pours | Connectivity, DRC, spacing, return paths, affected impedance and manufacturing exports |
| Board/copper thickness, stackup, finish | Affected impedance, current capacity, holes, assembly process |
| GPIO/interrupt/boot configuration | Schematics, PCB, interface table, firmware, recovery programming, related tests |
| Battery/enclosure/connector | Polarity, peak power, clearance, antenna, assembly/thermal/runtime behavior |
| Different board/rework | That board's unpowered/power checks, affected modules and nearby nets |
| Firmware/SDK update | Affected peripherals, power load, sleep, communication, persistence |

Do not blindly rerun the entire project. Explain which evidence remains applicable and why; repeat checks actually affected by the change.

## Handoff records

Keep actionable information in `HANDOFF.md`:

1. Current authorization and items the user explicitly does not want changed or tested further.
2. Authoritative project, manufacturing package, order mapping, baseline ID/hashes, physical board IDs, and rework history.
3. Current wiring/power, actual ports/device identities, and software holding interfaces open.
4. Specific passed checks, untested items, known failures, and accepted limitations with evidence for each.
5. Critical pin table, power states, physical orientation, and accessible alternatives to hidden-pad probing.
6. Last operation/result, exact next action, and branches for different results.
7. Rollback files, recovery programming procedure, and configurations/templates to preserve.
8. Tool blockers: service availability, desktop connection, document identity, and exact error rather than only “cannot connect.”

Do not retain credentials, private Wi-Fi passwords, or unrelated personal background. Respect naming, attribution, and content requirements in public documentation. Do not invent a project purpose or embed project-specific contacts in a general skill.

## Final report

Lead with the conclusion, then changes, verification, limitations, and deliverables. Example:

> revC schematics and PCB passed the listed static checks. The manufacturing package has been independently previewed and frozen for engineering prototypes under the agreed conditions. The local USB cross-section was calculated; full-channel/TDR testing is outstanding. The prototype has not been powered. Assemble one board next and check power and boot against the test plan.

Avoid:

> DRC is zero, everything will work, pay now, guaranteed.

Relate board maturity to agreed requirements and measured coverage. Without production-consistency, environmental-life, EMC, or regulatory tests, do not claim mass-production certification. Whether those tests are required depends on the application and delivery scope; do not add them as mandatory work to every DIY project.

## Manufacturer source examples

These sources correspond to the case. Use the actual parts and revisions for each new project:

- [Espressif hardware design guidelines](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/index.html): distinguish chips/modules, boot requirements, and layout.
- [TI TPS63021](https://www.ti.com/product/TPS63021): datasheet, layout, and power design.
- [ST LSM6DS3TR-C datasheet](https://www.st.com/resource/en/datasheet/lsm6ds3tr-c.pdf): pins, modes, registers, and self-test.

Prefer manufacturer documents and record revision/section/access date. Online “latest” content may change and is not an immutable design baseline.

## Record checker

Run `scripts/check_evidence.py` for the intended stopping stage, normally G5 for design. See [validation tools](10-validation-tools.md). The checker reports missing evidence and unresolved rows without writing statuses or claiming electrical correctness. Model and physical tests remain separate.
