# Visual and geometry gates

Use reference 12 for schematic composition and reference 03 for PCB spacing. Run these checks before advancing stages, not as optional cleanup at manufacturing release. Record six separate check IDs in the provided templates. For each, retain the actual baseline, numerical limits where applicable, native readback, method, unresolved object pairs and visual evidence. A completeness checker only audits records; it cannot certify the drawing.

## Conservative object screening

Run `python scripts/screen_visual_geometry.py snapshot.json`. Standard library only. Exit 0 means no suspects in the supplied bounds with declared complete coverage; exit 1 means suspects or incomplete coverage; exit 2 means malformed input. Output always leaves final engineering acceptance unassessed. Confirm every suspect using exact shapes and native rendered evidence; do not automatically move objects or declare an AABB overlap to be a proven copper collision.

Snapshot schema:

```json
{
  "schema": 1,
  "kind": "pcb",
  "baseline_id": "revA",
  "source": "native-export.json; extractor version and transform proof",
  "unit": "mm",
  "coverage": "complete",
  "missing": [],
  "limits": {"pad-pad": 0.15, "silk-silk": 0.2, "mask-silk": 0.2},
  "objects": [
    {"id": "R1.pad1", "kind": "pad", "ref": "R1", "layers": ["top"], "bbox": [0, 0, 1, 1]},
    {"id": "R2.pad1", "kind": "pad", "ref": "R2", "layers": ["top"], "bbox": [1.1, 0, 2.1, 1]},
    {"id": "R1.ref", "kind": "silk", "ref": "R1", "layers": ["top"], "bbox": [0, 2, 1, 3]},
    {"id": "R1.mask1", "kind": "mask", "ref": "R1", "layers": ["top"], "bbox": [-0.05, -0.05, 1.05, 1.05]}
  ]
}
```

These example limits are test inputs, not a fabrication specification. IDs identify unique physical objects, including separate pads sharing a pad number/net. Include all copper layers occupied by through-hole pads; omit layers only for schematic objects. A mask object is an opening. Silk objects include text and graphics; aggregate connected strokes belonging to one intentional graphic. No same-net exemption exists. Bounds are axis-aligned enclosing boxes **after** verified rotation/mirroring, including stroke widths and visible text extents. They must come from the actual saved design, never invented rectangles selected to pass. Preserve raw exports, extraction code, object counts by category, unsupported types and transform evidence. Missing data must appear in `missing` and set `coverage` to `partial`; empty categories are rejected for PCB screening.

For schematic screening, use `kind: schematic`, `unit: sheet`, `usable: [xmin,ymin,xmax,ymax]`, `reserved: [[title-block or reserved metadata bounds]]` (use `[]` when none exist), and `objects` with unique IDs, kinds and `bbox` in the same verified sheet coordinates. For framed layout, `usable` is the inner frame with margins; for free layout it is the declared custom canvas/export rectangle with margins. Both modes are valid and must be recorded with the evidence. Include visible symbols, child attributes, labels, pin text, NC markers, wires and notes; exclude the sheet border/grid/title-block decorations themselves. Split electrical wires into occupied segments rather than treating a large L-shaped wire as a filled rectangle. The helper checks bounds/title-block intrusion only. It cannot infer visual text collisions or functional block membership: `SCH-TEXT` and `SCH-BLOCKS` require native rendering inspection. Do not claim a schematic text-overlap PASS from this helper.

## Gate evidence

| Check | Timing | Required result |
|---|---|---|
| SCH-PAGE-BOUNDS | G2-A, G2-B, G5 | No circuit content outside the chosen free-layout canvas or inner frame, or intruding into reserved metadata |
| SCH-BLOCKS | G2-A, G2-B, G5 | Named regions with visible graphical separators and whitespace |
| SCH-TEXT | G2-A, G2-B, G5 | Every block inspected at readable detail; no overlapping or clipped text |
| PCB-PAD-GAP | G3 and final G4/G5 | Exact pad contours satisfy recorded positive gap, including same-net pads |
| PCB-SILK-GAP | G3 and final G4/G5 | Text/graphic edges satisfy recorded positive gap |
| PCB-SILK-MASK | G3 and final G4/G5 | Final silk stays clear of actual mask openings |

Save a full-page/whole-board view and readable detail views. For PCB delivery inspect top and bottom silk with mask in the actual manufacturing outputs. For schematic delivery inspect the native saved/reopened document and vector export where supported. Treat unsupported export, missing geometry or unreadable screenshots as gaps, not evidence of no collisions. A user choosing to stop repair changes delivery scope; unresolved checks remain visible.

## Required design profile

For new designs and full design release, run `python scripts/check_evidence.py --root <project-directory> --baseline <id> --through G5 --design-gates`. Required G2 rows: PART-IDENTITY, SCH-FORMAT, SCH-PAGE-BOUNDS, SCH-BLOCKS, SCH-TEXT. Required G3 rows: ROUTING-READY, PCB-PAD-GAP, PCB-SILK-GAP, PCB-SILK-MASK. Required G5 row: RELEASE-FREEZE. Each must be PASS on the current baseline with evidence. SCH-FORMAT actual must be exactly free-layout or framed-layout. At intermediate --through G2 only G2 rows are enforced. Keep earlier stage IDs for final rechecks and update the evidence baseline. Do not claim this metadata check automatically verifies native geometry.
