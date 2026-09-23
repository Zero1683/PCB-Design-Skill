# Accepted dimensions to observed geometry

Use this check for new-design G3 and later. It ties the confirmed proposal to measured extents; existing narrow repairs do not need a new product intake.

`intake.json` already contains `proposal.assembly_envelope_mm` with `board_length`, `board_width` and total `assembled_height`. Axes mean X span, Y span and total Z extent, including both sides, PCB and installed parts. Do not silently swap X/Y to fit. By default board X/Y are exact design dimensions and total height is a maximum. For a genuine maximum size, include `proposal.dimension_policy` with all three keys and values `exact` or `maximum` before presenting/accepting the proposal. The policy participates in the proposal digest. Do not change it afterward just to pass.

```sh
python scripts/mechanical_envelope.py derive --root /project --baseline RevA
python scripts/mechanical_envelope.py check --root /project --baseline RevA
```

`derive` writes `mechanical-contract.json` from the accepted intake; no second hand-written copy of dimensions is needed. `check` compares it with the current intake and `mechanical-observation.json`. Changing either the expected size or the plan invalidates stale records.

The observation is schema 1 and contains `project_id`, `baseline_id`, `units: mm`, `coverage: complete`, `source: {path, sha256}`, `board_bounds_mm: [minX,minY,maxX,maxY]`, and positive `assembled_height_mm`. Its source must be a current input in `design-baseline.json`. Extract bounds and assembly height from actual native/assembly geometry; an agent-written estimate is not complete observed coverage.

For G5, also supply `outline: {path, sha256}` referencing the final exported manufacturing outline, listed in the same baseline. The checker reparses that file and refuses an observation whose bounds disagree. The supported exact extent path is a closed simple linear Gerber outline; open, branched, self-intersecting and curved outlines cannot pass through a guessed bounding box. Curved-outline support needs an exact-extents adapter, not relabeling the input or loosening tolerance. G3 can use sourced native observations before manufacturing export; G5 cannot omit the bound outline.

The fixed 1e-6 mm allowance is for numeric representation only. This check does not assess manufacturing tolerance, mounting-hole position, internal cutouts, connector reach, cavity collisions, antenna clearance or real three-dimensional assembly fit. Total height is still a sourced observation; this script does not derive it from a 3D model. Those requirements keep their independent mechanical checks. A correct rectangular extent cannot make a wrong outline shape acceptable.

Existing G3/G5 projects need to recover the actual accepted size and generate the new contract/observation. Do not fill unknown measurements with the expected values. `check_evidence.py --design-gates` now invokes this comparison automatically from G3 and requires the manufacturing outline from G5.

The envelope adapter requires an explicit absolute leading-zero coordinate format, millimetres, circular apertures, linear draw/move commands and a final M02 terminator. It rejects unknown commands, missing declarations and unconsumed/truncated content before calling the geometry reader. Other legal Gerber dialects need a capable independent adapter; they are not accepted by approximation.
