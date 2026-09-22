# Repeatable improvement and external-method admission

## Review each meaningful change

Start with a concrete product/physical invariant, identify how the current code can violate it, create a reproducer, then repair it. Follow every fix with a valid case that must still pass. Review both false negatives and false positives. Do not count additional prose as an implemented check.

For each batch record baseline, defect, reproducer, change, results, limitations and next unresolved issue. Re-check source identity, missing-data handling, units, geometry transformations, ordering, retries and output evidence. A changed parser or checker invalidates affected prior reports. Use the existing scoped retry ledger; do not add another competing rollback state machine.

A useful adversarial case changes one relevant condition: a footprint suffix, rotated physical pad, absent export object, duplicate key, stale source, unsupported macro, missing mask layer, skipped process, changed user dimension or incorrect calculator unit. A failed check is not solved by changing its rule to match the board.

## Default test entrypoint

```sh
python scripts/run_regression.py --workdir /absolute/disposable/work
```

Python 3.10+ and Node.js 18+ are required. The runner sets temporary directories, loads the complete Python suite, supplies legacy test working directories, runs Node suites and reports test/skip counts. Skips make release validation fail by default. `--allow-skips` is diagnostic only; the report must retain the uncovered platform case. `--python-only` is a scoped run, not complete release verification.

Run targeted tests after small changes, then the full suite for the candidate. For performance work, compare exact outputs against the prior/brute-force algorithm over seeded random and boundary cases before measuring speed. The body-envelope X sweep prunes impossible pairs only and preserves ordering/metrics; worst-case dense overlap can still be quadratic. It does not replace pad, mask, 3D or mating-clearance checks.

## External review, 2026-09-22

| Project and inspected commit | Evidence inspected | Decision |
|---|---|---|
| [specs-to-pcb](https://github.com/bluzername/specs-to-pcb/tree/5bf0c9837b0d07f851023c540060702ff4a01edc) | MIT license, skill, prerequisites/pipeline, generator and routing script review | Borrow structured input and separate export-review phases. Do not require novices to supply netlists; do not adopt fixed example geometry or automatic tool downloads. No code bundled. |
| [circuit-synth](https://github.com/circuit-synth/circuit-synth/tree/3aaff18c056de7cbe8f5b0a3e1e6e7e7895f544e) | MIT license, simple validator, KiCad/ERC/QA source | Adopt explicit issue locations/subjects and separate runtime validity from electrical validity. No automatic source patching or KiCad runtime added. |
| [atopile](https://github.com/atopile/atopile/tree/619eda7f777558a3e500dbad9cc2941712881495) | MIT license, interface ERC diagnostics, DRC invocation, default-constraint trait | Adapt source-to-interface diagnostic structure into existing pin-net failures. Do not import its compiler/toolchain or assume ERC implies schematic/PCB parity. |
| [JITX Skills](https://github.com/JITx-Inc/jitx-skills/tree/bd4cb45905e27b8e472cd01276fdcc744ee39f5b) | Published substrate/interconnect docs and license | Excluded from bundling/derivative reuse: inspected LICENSE reserves rights and grants no general reuse permission. Public visibility is not an open-source license. |

These are reviewed candidates, not claims of market leadership, complete repository audits or measured superiority. Existing four bundled toolsets remain listed in THIRD_PARTY_NOTICES. General engineering rules continue to use manufacturer/technical sources. Before incorporating any future code, verify license compatibility, pin a commit, retain notices, test the adapter and document new dependency/platform costs.

## Stop and preserve evidence

Prioritize stable, accurate progress over token throughput. When repeated attempts do not improve a reproducible defect, change the method before retrying. When tools or hardware are unavailable, continue independent checks and record the gap. Before execution capacity ends, save a coherent candidate and handoff; do not mark the goal complete or publish a stable release with unmet required validation.
