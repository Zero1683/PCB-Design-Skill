# Beginner decisions and a two-step brief

Read before committing a new design's outline, connectors, power arrangement or assembly plan. Use the user's language. Ask about the product they will use; research engineering parameters yourself.

## Step 1: understand the object

Extract existing answers first. Group missing everyday decisions into a short exchange, normally no more than three questions at once. Cover these six topics, with follow-up only where relevant:

| Record | Beginner-facing example | Agent responsibility |
|---|---|---|
| purpose | What should it do, and how will you use it? | Translate behavior into measurable functions; preserve every requested function. |
| carrier | Bare board, handheld object, or an existing case? A photo/model is useful. | Check cavity, mounting, battery, connector access and antenna clearance. |
| board_size | Is there a maximum length/width, or should I propose a size? | Distinguish PCB outline from enclosure exterior and total assembled envelope. |
| power | USB, battery, external adapter, or a combination? | Determine chemistry, charging, input ratings and simultaneous-source states from evidence. |
| controls_connectors | Where should buttons, lights and plugs be accessible? | Derive connector orientation, mating space, user reach and recovery access. |
| assembly | Will you solder it yourself or order assembly? | Select manageable parts and explain the effect on price and repairability. |

Do not present the engineering intake table as a questionnaire about Dk, current slew rate, impedance tolerances or via construction. Derive those from exact components, actual use and the fabricator. Ask only when a missing physical fact cannot be obtained otherwise.

"I don't know" is a useful answer. Propose a dimensioned sketch and explain what fits. Silence, an unanswered question and the agent's recommendation are not user confirmation. A user's explicit "you decide" is delegation for the stated topic, not permission to drop functionality. Ask only about remaining undelegated choices. Parts research and alternative costing may continue while a choice is pending.

Translate outcome language too: "a keyboard I can plug into my computer and use" includes host compatibility and firmware behavior. Record those dependencies in the functional plan. The default PCB G5 package covers fabrication preparation; it does not by itself satisfy a request for a working finished device. Explain the remaining firmware/assembly/test work and include it in the requested scope without silently changing the outcome or claiming it is already tested.

## Step 2: show the proposed device

Before detailed drawing, show one compact plan: functions, dimensioned board sketch, total height, carrier/mounting, accessible connectors/buttons, power/charging behavior, assembly method and component-only cost. Show unknown prices as unknown. Explain only meaningful tradeoffs. Ask for acceptance or changes once; do not ask permission for each subsequent wire or check. Explicit delegation already covering those decisions permits proceeding after showing the chosen plan.

Include a short reason for the proposed size, not merely "50 x 30 mm". Record strict maxima separately from preferred sizes and free-design space. If it will not fit, propose changes before placing components outside the confirmed space. Do not silently enlarge a board, rotate its external interface or remove a function to achieve routing or cost targets.

## Executable record

`init_project.py` creates `intake.json` with unknown topics and baseline `UNSET`. Set `baseline_id` to the chosen revision; use the provisional-to-native identity procedure below for `project_id`. Each of the six named topics has `state`, a plain-language `value`, and `source: {path, sha256}`. States: `unknown`, `proposed`, `confirmed`, `delegated`, `not_applicable`. Core topics cannot be omitted: "bare board, no enclosure" is a carrier decision, not N/A.

Use source files containing the actual user statements/attachments; never use agent-authored approval text. Hashes prove file integrity, not who wrote it. Preserve enough conversation context to inspect the meaning and scope of the decision.

The `proposal` contains `topics_digest`, a `document` file reference to the displayed plan, `choices` text for all six topics, `assembly_envelope_mm` with positive `board_length`, `board_width`, `assembled_height`, and timezone-aware `created_at`. Bind the separate `decision` using `proposal_digest`, `status` (`accepted`, `delegated`, `rejected`), actual source reference, and `recorded_at`. The recorded event occurs after the plan is assembled; a delegated source can be an earlier explicit user instruction. A direct plan acceptance can resolve earlier unknown choices only if the presented plan explains those choices. A delegated decision cannot resolve an unanswered topic.

Generate digests with `workflow_io.digest()` and file references with `file_hash()`. Do not edit digests merely to silence stale-decision errors; review the changed topic and obtain any newly required decision. Normal accepted choices can be carried into a new design revision with the original source, but changed product decisions need a new proposal/decision binding.

Before an EDA project exists, `init_project.py` uses the local project name as the provisional `project_id`; choose the actual working baseline instead of `UNSET`. Preliminary brief/price work needs no native project. Once native creation returns the real ID, record the provisional-to-native mapping and the creation/readback evidence in PROJECT.md, then set intake `project_id` to that ID and rerun the checker. Preserve user source files and the unchanged proposal/decision; this identity reconciliation alone does not require asking the same product questions again. Refresh downstream bindings using the actual ID. A different product or changed scope cannot inherit that consent through this migration.

```sh
python scripts/intake_review.py --root /project --baseline RevA --through brief
python scripts/intake_review.py --root /project --baseline RevA
```

The brief check supports early research. The design check must return `PLAN_RECORDED` before dependent new-design native writes. G2–G5 `check_evidence.py --design-gates` also requires it. The guarded live CLI enforces it before new-design apply requests; [scoped existing-page maintenance](23-live-eda.md) uses its separate exact-batch record and cannot establish new-design acceptance. Raw official API calls remain the agent's responsibility. This is not a security boundary around all EDA access.

Legacy projects remain readable. Missing records produce an explicit migration item, not invented consent. Recover actual prior decisions; ask only for still-missing information. Do not require a complete product-intake interview for a read-only review or an unrelated, narrowly authorized repair; keep that work outside the new-design acceptance claim.

## Communication during design

Tell the user what changed and what they need to decide. Keep internal check IDs, hash reports and detailed failure logs in project records. Group defects into one repair pass. At handoff, provide source/manufacturing files, assembly orientation, connection instructions and measured versus unmeasured scope. Do not describe synthetic checks or successful API calls as a proven physical board.
