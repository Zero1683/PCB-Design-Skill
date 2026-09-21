# EasyEDA native-format operations

Use the bundled [official format skill](../vendor/easyeda-pro-format-skill/SKILL.md)
for native source interpretation, generation and narrowly scoped repairs. The
API skill's [format index](../vendor/easyeda-api/format/index.md) covers its own
source representation; verify the actual container, document kind and format
version before choosing a reference. A primitive-format text file is not a
complete .epro/.eprj project or an imported document.

## Apply the format layer within the main workflow

1. Prefer documented live APIs for supported editing. For offline or source-level
   work, preserve original files, identify the exact format/client and work on a
   copy. Read the official type index, document, primitive and relevant schema.
2. Record document type explicitly. LINE, COMPONENT, META and CANVAS have different
   meanings across documents. Never rely on the validator's bare-type fallback.
3. Preserve existing IDs, references, tickets/history and unknown fields according
   to the real format. New IDs are for genuinely new objects only. Parent/child,
   pin/symbol/footprint links and associated primitives must remain consistent.
4. Check coordinate units, local/world transforms and serialized Y-axis markers
   against a native sample. Do not import a universal sign flip from a recipe.
5. Validate each generated primitive and its metadata with the wrapper below.
   Check document assembly, separators, required document primitives, references
   and history separately. Keep output and reports in the task workspace, outside
   the vendor directory; do not follow upstream's in-skill output directory.
6. Import/open the candidate with the actual target client in a disposable or
   authorized working copy. Compare parts, pin nets and geometry with independent
   intent; inspect native rendering, save/reopen, then run affected ERC/DRC and
   stage checks. No client means native acceptance remains NOT_RUN/BLOCKED.

Never silently change user-specified dimensions, electrical properties or part
identity to satisfy a schema. Resolve contradictions against versioned native
exports and exact-part documentation. Automatic coordinates for associated
graphics do not authorize inventing missing electrical requirements.

## File-input primitive validator

The wrapper uses the bundled official schemas and validator with explicit
document/type matching. Dependencies are included; no npm install is required.

```sh
node scripts/validate_eda_primitive.cjs /path/to/primitive.json
```

Input example (one CANVAS primitive, not a complete schematic):

```json
{
  "docType": "SCH_PAGE",
  "primitiveType": "CANVAS",
  "outer": {"type": "CANVAS", "id": "CANVAS", "ticket": 1},
  "data": {"originX": 0, "originY": 0}
}
```

`docType`, `primitiveType` and `data` are required; `outer` is optional for a
payload-only check. The wrapper rejects an unknown document/type pair instead of
falling back to a different schema. If outer metadata is supplied, its type must
match, and both metadata and payload must pass. DOCHEAD's payload docType must
match the requested domain. Exit 0 means only this declared primitive/schema
check passed; exit 1 means failure. The JSON result explicitly reports coverage.

Do not pass complete projects or history streams to this single-primitive helper.
It does not check global uniqueness, referential completeness, wiring, visible
geometry, package completeness or manufacturing/electrical correctness. Record
the upstream snapshot and chosen schema with the validation result.

## Known upstream caveats at the bundled snapshot

- `validate.js` can warn and fall back for an unregistered document/type pair.
  Our wrapper requires an exact registered pair (or DOCHEAD) before validation.
- The PCB LINE schema requires groupId to be a string, while its description
  explicitly says native ungrouped records use numeric 0. Report this as a schema
  versus native-format discrepancy. Do not convert real numeric 0 to string "0"
  merely to obtain valid:true; preserve the native data and obtain native evidence.
- The entrypoint gives inconsistent final-record separator examples. Establish
  framing from the versioned file specification and a save/reopen sample; the
  primitive validator cannot resolve container framing or history semantics.
- A supplied schema may allow values that are electrically or geometrically
  meaningless. valid:true does not satisfy our engineering gates.

The original LICENSE, source commit and documented integration changes are in
[UPSTREAM.md](../vendor/easyeda-pro-format-skill/UPSTREAM.md). Runtime dependency
licenses remain beside their packages. Update source, schemas and validator as a
reviewed unit; never mix examples from a newer main with an older parser silently.
