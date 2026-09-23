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

For a resumed project, run `python scripts/project_progress.py --root /project --baseline RevA --lang zh`
after checking the actual baseline. It reads the existing intake and check
records without changing them. The result names the first unfinished stage,
summarizes at most three record errors and separates a user decision from an
agent repair. Confirm any suggested question against the actual conversation:
the data file cannot prove that the user said or accepted something. A fresh
template has baseline `UNSET`; choose and record the design revision first.
The `fabrication_evidence_complete` flag uses the full existing G5 gate when
applicable. It does not mean that electrical correctness or a physical board
has been established. Do not expose the JSON as the whole user update; turn
its `next_step` into a concise progress message with a concrete result.

The user should be able to start with "I want a small keyboard for coding" without
knowing a processor, bus or CAD file format. Translate that idea into a useful
device proposal. Do not require the user to write an engineering specification or
learn the internal gate system to get help.

At a meaningful milestone or blocker, explain briefly: what is now complete,
what will happen next, and what the user needs to do, if anything. Examples:
"The USB and buttons are connected in the schematic. I am checking their pin
assignments before arranging the board. Nothing is needed from you right now."
"The case is too narrow for this connector. I can move it to the short edge;
please confirm that a cable can plug in there." Do not repeat status templates
when nothing has changed, invent progress percentages, or expose raw tracebacks
as the only explanation of a failure.

When a check fails, investigate and repair within the accepted scope. Explain a
blocker by its effect on the device and offer a concrete next step. Ask the user
only for inaccessible information or a choice that changes the product. Do not
ask a beginner to calculate an impedance or interpret DRC output. Keep the full
diagnostic and any unresolved limitation in the project record.

## A usable handoff

Lead with what the user can do now. Use the existing handoff record to provide:

- Exact links to the source project and the package intended for fabrication,
  identifying its revision. Explain which file goes where.
- The component list, quantities, current quote/unknown items, assembly method,
  and necessary external items such as cables or a programmer. Separate parts
  from fabrication, assembly and shipping costs; never imply a parts estimate
  is the complete cost.
- A short next-step sequence matched to the user's situation: order the board,
  assemble it, inspect it, perform limited-power first startup, load the correct
  firmware where available, and test the requested functions. Link detailed
  instructions instead of showing every stage at once. The user places orders
  unless purchasing was explicitly authorized.
- What is verified, what awaits the physical board, and any unfinished firmware
  or enclosure work. When hardware is absent, finish the authorized engineering
  package and give a restart point for later bring-up.

If the request is for a working object, maintain a short completion list for
hardware, firmware, enclosure and assembly as applicable. Work on authorized
items within available tools; explicitly hand off unavailable work. Do not silently
expand a PCB-only task into those areas. A recipient should know what to do next
without reading the whole engineering log.

For a later change such as "add a screen", recover the existing project and
review the affected power, interfaces, space and cost before proposing the change.
Preserve earlier answers and working functions. At project completion, record
the actual revision, choices, verified conditions, remaining issues and file
locations in the existing handoff. Record cost or time only when known; never
label an unbuilt circuit as a proven recipe.

Tell the user what changed and what they need to decide. Keep internal check IDs, hash reports and detailed failure logs in project records. Group defects into one repair pass. At handoff, provide source/manufacturing files, assembly orientation, connection instructions and measured versus unmeasured scope. Do not describe synthetic checks or successful API calls as a proven physical board.
