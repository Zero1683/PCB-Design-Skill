# Source and local adaptations

Source: https://github.com/daishuge/pcb-skill
Commit: 6e939b64907e3c63236c7522c511af5d7d1afaad
Retrieved: 2026-09-21
License: MIT; original LICENSE retained beside this file.

Included: scripts/placement, scripts/routing, scripts/verify, scripts/notify and
their documentation. Not included: upstream SKILL, setup guides, browser approval
automation, purchase workflow, case-specific project or external MCP dependency.
Our reference 18 governs integration; the upstream project is not an EasyEDA
official component. This copy is locally adapted, not pristine upstream.

Local changes:

1. netlist_assert.py rejects unknown/empty/malformed assertion contracts and
   unresolved net/pad targets for all three assertion types, including unknown
   declared plane nets. Missing objects cannot satisfy a negative check.
2. gerber.py rejects clear/negative polarity and unimplemented transforms, while
   retaining dark/positive and identity settings. Unsupported aperture holes and
   compound/clear/rotated macros also fail explicitly. No full polarity implementation
   is claimed; unsupported files require a different capable checker.
3. route_supervise.py binds output readiness to run start, checks crash/gone/time
   conditions even with growing/stale output, exposes readiness-only coverage and
   returns nonzero for a pending --once query. --started-at supports late attach.
4. New process_status.py uses OpenProcess(SYNCHRONIZE), WaitForSingleObject and
   CloseHandle on Windows; both watcher utilities share it. POSIX signal-0 remains
   POSIX-only. Access errors propagate rather than masquerading as process exit.
5. import_easyeda.py rejects missing footprints, duplicate designators, multiple
   PCB documents and empty PCB imports, and reports source/imported part counts.
6. Affected README/docstring descriptions are updated to reflect these changes.

First-party wrapper and regression tests live in the parent skill's scripts/.
The wrapper requires project-specific rule/layer inputs on import; upstream
example defaults remain available to its synthetic fixtures. NumPy is optional
for raster/clearance and is not redistributed in this package.

Validation performed by this integration is recorded in the parent VALIDATION.md.
Upstream case measurements are the author's reported results, not our reproduction
on those original files or a physical board. Native-client acceptance is separate.

Additional local adaptation: native PCB import retains each component's native_id
for the first-party reconciliation adapter. Existing board fields remain available.
This additive field does not establish full primitive-ID or native restore coverage.

2026-09-22 local acceptance fixes:
- outline_check.py reconstructs one simple ring from actual endpoints, rejects unsupported
  topology, enforces full-edge copper/drill margins and records empty/omitted scope.
- boardmodel.py retains physical element nets and rejects ambiguous repeated lands;
  pad_reconcile.py compares every physical land and rejects contradictory pin membership.
These changes have synthetic/public-CLI regression evidence; they do not extend
native-client or physical-board qualification.

2026-09-22 physical inspection corrections:
- boardmodel/import_easyeda preserve supported plating and layer spans; unsupported
  native encodings fail explicitly instead of becoming through-vias.
- route_accept compares protected copper geometry with a baseline and records
  PASS/FAIL/NOT_CHECKED with coverage. Equivalent straight segmentation is retained.
- netlist_assert checks all physical lands per logical pin and actual plane reach.
- mask_check computes supported circle/polygon opening unions, explicitly scopes
  partial openings and untagged pads, and rejects unsupported raw Gerber semantics.
- Public wrapper validates inspection arguments before vendor dispatch.
