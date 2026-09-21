# Circuit intent, reuse, and revision checks

Use this workflow for repeated circuit blocks, critical pin-net relationships, or design revisions that need reproducible comparison. Keep the native EDA project authoritative for the implemented design. Requirements and manufacturer documentation define what the circuit should do; actual EDA exports establish what was drawn. A mismatch requires review of both, never an automatic rewrite of either to make a check pass.

The approach borrows the useful idea of expressing circuit structure as data/code from [PCBDL](https://github.com/google/pcbdl). This skill implements its own small checks using Python's standard library and the existing normalized export format. No PCBDL runtime, source code, exporters, or circuit library is bundled or required.

## Structured intent and native readback

1. From the requirements, exact-part datasheets, and reviewed pin table, record intended components, interfaces, and critical connections before wiring. For a simple circuit, the existing pin table may be sufficient; avoid a second full circuit description with no verification benefit.
2. For critical connections, write explicit expectations independently of the exported wiring. Good examples include an enable pin's pull-up connection, distinct supply rails, an exact feedback-node membership, and a datasheet-required unused pin. State the source and rationale for each rule.
3. Perform G2-A component placement and review as specified in [reference 12](12-schematic-drafting.md). Recording intended connections in a JSON file does not authorize placing wires early. G2-A intentionally has unconnected pins; check final connection expectations after G2-B wiring.
4. Read back actual native pin nets after the edit. Retain the native export, extractor/version, project/document identity, and normalized snapshot. Use [reference 10](10-validation-tools.md) for the snapshot contract. Do not feed the planned data into the checker as if it were an actual EDA export.
5. Run declared connection checks and native ERC. Review failures against the source requirements and the actual drawing. After an intentional change, update the reviewed expectation with its reason and rerun; retain previous results.

For read-only tasks, use existing exports or non-mutating reads and return results without editing the project or initializing records. If native extraction is unavailable, identify missing evidence; textual intent alone cannot establish implemented connectivity.

## Executable connection expectations

`scripts/check_connectivity.py` accepts a complete normalized schematic/PCB snapshot and a JSON contract:

```json
{
  "schema": 1,
  "baseline_id": "revA",
  "source": "PROJECT.md section 5; selected part datasheet revision and pin table",
  "rules": [
    {
      "id": "enable-pull",
      "kind": "same_net",
      "pins": [["U1", "8"], ["R1", "2"]],
      "basis": "Illustrative pin assignment only: these two pins must share the enable node"
    }
  ]
}
```

The example reference designators and pins are fictional. Substitute the current design's actual package pins and cite its real design basis. Do not infer GPIO numbers from package pins. `source` and each `basis` are required provenance text; the checker does not independently verify the cited documents.

| Rule | Required relationship | Important boundary |
|---|---|---|
| `same_net` | At least two distinct pins share one non-null net | Allows other pins on the same net |
| `different_nets` | At least two distinct pins each have a different non-null net | Checks direct net separation, not DC conduction through resistors, switches or protection devices |
| `exact_net` | Listed pins comprise one entire non-null net | Detects added branches, including electrically present DNP footprints; list every intended member |
| `no_connect` | Every listed pin has explicit null connectivity | Null is allowed only for documented intentional NC; missing export data must never become null |

Pins use `[reference, package-pin-number]` pairs. Matching is exact and case-sensitive. Net names may change without changing a pin relationship. The baseline must match; empty rule sets, missing endpoints, duplicate rules/pins/JSON keys, partial exports, and BOM-only input are rejected. DNP parts remain in the logical topology; fitted status does not remove their copper pads.

```sh
python scripts/check_connectivity.py schematic.json circuit-checks.json
python scripts/check_connectivity.py pcb.json circuit-checks.json
```

Exit 0 means the declared relationships match the supplied data, 1 means at least one relationship fails, and 2 means invalid input. JSON output includes the observed pin nets and, for exact membership, unexpected members. Save the result alongside the input contract and source export as `SCH-WIRING` or affected G4 evidence. It covers only declared relationships; it cannot establish ratings, timing, impedance, geometry, actual routed copper continuity, or measured hardware performance.

## Reusable circuit blocks

Reuse a reviewed block only when its assumptions match the new design. Keep a small module record with the following fields; add it to the project's existing design notes rather than building a parallel catalog by default.

| Field | Record before reuse |
|---|---|
| Identity | Block name, revision, exact parts, datasheet sources, native source document |
| Parameters | Supply range, logic domain, load/rate, resistance/capacitance choices and calculations |
| Interface | Named ports, direction, voltage, startup state, return reference, address/polarity |
| Dependencies | Required pulls, decoupling, sequencing, firmware configuration, external protection |
| Physical requirements | Verified footprints, placement/return constraints, isolation or antenna keepouts |
| Verification | Which revision/conditions were checked, actual test scope, unresolved items |

When instantiating a block:

- Bind every local reference and local net explicitly to a unique instance. Share power/global nets only intentionally. Do not silently merge two modules with the same local net names.
- Recheck exact pin mapping, voltage compatibility, aggregate load, parallel pull resistance, bus capacitance/timing, addresses, startup/boot behavior, and thermal/physical constraints as applicable. A successful earlier board does not validate a changed part or load.
- Use parameterized generation through supported EDA APIs when it reduces repeated work. Preserve module-to-native object IDs, read back each result, and inspect the rendered schematic. Keep a backup and reconcile partial success before retrying so a retry does not duplicate components.
- Reuse placement and annotation conventions, then repeat the affected G2-A/G2-B checks. Generated graphics still need readable module titles, real electrical connections, correct junctions, and native rule checks.

## Review revisions

```sh
python scripts/audit_design.py diff before.json after.json
```

Use actual complete exports of the same project and document kind with distinct baseline IDs. The report lists added/removed references and changed part number, value, footprint, fitted/BOM status, or pin-net mapping. Reference renumbering appears as removal/addition; document the identity mapping before interpreting it as a component substitution. A net rename appears as a pin-map change and needs review even when a relationship check still passes.

Exit 0 means no differences in the compared fields, 1 means differences were found, and 2 means invalid input. Differences can be intentional. This report does not compare placement, routing, copper pours, geometry, or design rules; inspect native diffs for those. Continue using `audit_design.py compare` for schematic/PCB/BOM consistency within one baseline.

Link each accepted change to the request, affected module, calculation, check result, and native snapshot. Review unchanged critical connections as well as the targeted edit. Keep release source, Gerber, BOM, and assembly evidence tied to the same final baseline.
