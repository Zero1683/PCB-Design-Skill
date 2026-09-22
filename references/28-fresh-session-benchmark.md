# Fresh-session whole-board benchmark

Use when the user asks to test the complete skill in a new task. This benchmark remains NOT_RUN until actual evidence is collected. Unit tests and the earlier test1 schematic movement demonstration cannot fill its results.

## Scope and starting point

Start from the user's requested hardware idea. Use a new authorized engineering project and the installed skill's normal intake. Record skill manifest revision/hash, OS, EDA/Gateway/API versions, project/document IDs and the target directory. Verify the loaded skill path and its manifest before editing. Do not silently use an older duplicate installation. An existing EDA connection does not establish which project is selected.

Let the user provide the product goal; derive specifications through normal requirement review. Do not impose an ESP32 model, board dimensions, fixed layer count, generic component package minimum, NAS dependency or fixed budget from previous examples. Quote components before detailed drafting. Stop at reviewed G5 deliverables; the user handles ordering.

## Evidence record

Create BENCHMARK.md with a row for each stage, initially NOT_RUN. Record actual elapsed time, attempted and failed writes, repeated repairs, selected backend and API fallback reasons. Do not infer counts from estimates or call elapsed time a token benchmark.

| Stage | Evidence required |
|---|---|
| G0/G1 | Sourced functional requirements, preliminary BOM, actual quote captures, MOQ-aware component totals, declared unresolved options |
| G2-A | One of the two allowed formats, actual components and document IDs, no-wire snapshot, readable partitioned full-page and detail exports |
| G2-B | Final wired native source, pin/footprint/part identity checks, independent net expectations, electrical calculations and ERC disposition |
| G3 | Actual board outline/layers, transformed bodies/pads/silk/mask, positive clearances, connector access and routing feasibility |
| G4 | Selected routing strategy, critical routes and return paths, poured copper, final native DRC and complete connectivity evidence |
| G5 | Saved/reopened source, raw manufacturing export and independent preview, coherent BOM/placement, current design bindings, requirement coverage and remaining limits |

Evaluate each stage PASS, FAIL, BLOCKED or NOT_RUN against actual evidence. If any step fails, retain the first failure and remedy, not only the final screenshot. After two ineffective attempts on the same issue, inspect the adapter/geometry/rule cause and change the method. Never weaken a physical rule to improve pass statistics.

## Recovery testing

Use a disposable copy and only operations supported by the selected writer. The guarded runtime currently supports moves of existing components in an unwired schematic. It does not implement native PCB routing rollback. Do not inject a PCB routing fault and assume this schematic recovery path can restore it. For a supported controlled test, capture before, apply one bounded change, read back, save/reopen, restore, and compare source identity/properties/geometry. Record mocks separately from native observations.

## Finish

Run the registry/binding check from reference 27 against the frozen candidate. Deliver files plus BENCHMARK.md and the actual operation log. Report unsupported checks explicitly and keep G6-G9 unperformed until real hardware work occurs. No claim of full-board capability improvement, token savings or first-pass hardware success can be made solely from this software update.

Suggested short user prompt (Chinese):

> 使用 $pcb-design-to-bringup，帮我做一个 ESP32 最小系统开发板，完成原理图、PCB 和可打样文件。这次是完整流程实测，请保留操作日志、阶段检查和最终交付文件。

The user can replace the board idea with their own; the skill supplies the workflow without a long engineering prompt.
