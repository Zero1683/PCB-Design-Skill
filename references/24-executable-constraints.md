# Executable constraints and bounded context

Use this reference before guarded native moves, mechanical geometry reviews, or resuming a long design task.

## Persist requirements outside the conversation

Keep one reviewed constraint file per document. Each has a revision, project/document IDs, explicit coordinate system and source references. Record connector mating positions, mounting holes, antenna/assembly keepouts and enclosure height from the actual requirements. Do not infer that an empty rule list means mechanical design is verified. Use [requirement coverage](25-requirement-coverage.md) to expose unmapped requirements and stale evidence. Unknown dimensions remain open items.

`design_constraints.mjs` evaluates rectangular bounds, locked anchor/rotation/side, allowed regions, keepout clearance and PCB component height. It rejects unknown fields/rules, stale object IDs, wrong units and incomplete declared PCB inventory. Rectangle checks are conservative; polygons, curved outlines, layer-specific copper rules, cables and full 3D collisions need separate checks. Keep electrical and mechanical acceptance independent.

Start with [the schematic constraint example](../assets/schematic-constraints.example.json), replacing IDs, bounds and sourced rules from the actual page. For schematic native captures use `domain: schematic`, `units: raw-0.01inch`, `axis: y-up`. The live writer checks all native parts against page bounds and rules. Sheet/title exclusion still determines usable bounds. Schematic positions do not encode physical PCB positions.

For PCB review use the example files below. The geometry must come from actual transformed board coordinates with complete object coverage. Include mounting holes or other mechanically fixed objects in that inventory with stable IDs. A caller-supplied `coverage: complete` declaration still needs export evidence; this tool cannot establish native truth by itself. Do not use a local footprint bounding box as its world-space box.

```sh
node scripts/check_constraints.mjs --snapshot assets/pcb-geometry.example.json --constraints assets/pcb-constraints.example.json --output /project/checks/mechanical-A.json
```

The report records input hashes. Check the fresh proposed geometry before a PCB modification and actual exported geometry afterward. This entrypoint does not execute PCB edits or provide PCB rollback.

## Enforce constraints at the live writer

New live batches require `--constraints /project/constraints.json`; see [the live writer](23-live-eda.md). Source, complete target and each intermediate move are checked before writes. Explicit directed repair may retain enumerated source defects until they are fixed; it never waives final compliance. See reference 23 for its scope. The constraint payload participates in operation identity. The journal records the file path/hash; changing or deleting that file blocks further mutations until reconciled. Do not delete a rule or enlarge bounds solely to pass a check.

```sh
node scripts/eda_live.mjs resume --journal /project/checks/operation.json
```

Resume is read-only. It captures actual state, checks the saved rules and reports the known step and previous operation state. Changed rules, unknown geometry or lost Gateway session require reconciliation. It never resumes an old write queue automatically. `status` remains available when the rules file changed. These commands recover one supported live batch; separately reload PROJECT.md, current requirements, latest native export, gate evidence and open items for whole-project handoff.

## Limit context output

`design_data.py summary/query/diff` default to a 16,384-byte output budget, including UTF-8 JSON and its newline. `--max-bytes` accepts 1,024 through 1,048,576 bytes. This is a byte limit, not a token count or total model context guarantee.

```sh
python scripts/design_data.py query /project/design-data.json --section footprints --limit 25 --max-bytes 8192
python scripts/design_data.py diff /project/before.json /project/after.json --max-bytes 8192
```

Use the returned `next_offset`, not the requested page size, to continue. Oversized individual records are replaced by an explicit digest/offset handle, never treated as fully reviewed. Export the complete board/normalized data to disk and inspect that record locally. Full original inputs remain preserved. If metadata itself cannot fit, the command fails explicitly. Summary/diff are navigation aids; relevant detailed geometry, source pages and visual checks still need review.

## Routing capability and recovery

Before authorizing automatic routing, classify nets and record which constraints the installed backend actually supports. For dense designs, verify the critical escape and channel assumptions before populating ordinary routes. Use actual footprint geometry, fabrication via processes, reference planes and stackup; count-based channel estimates alone do not prove routability. Select a different backend or revise the layout/stackup when required constraints cannot be expressed or verified. Do not retry an unchanged failed layout.

Native PCB routing lifecycle and rollback still require separate real-engineering validation. Layer count alone is not a pass/fail criterion. No DDR/HDI production capability or token-saving percentage is implied by these helpers.
