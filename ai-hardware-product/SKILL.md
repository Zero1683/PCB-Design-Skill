---
name: ai-hardware-product
description: Build or revise a complete AI-enabled physical product, coordinating the user journey, hardware, firmware, computer or cloud software, integration tests, cost, and reproducible build instructions. Use when the requested outcome is a working device or multi-route tutorial; use a PCB-specific skill for board-only work.
---

# AI hardware product

Turn the user's intended interaction into a demonstrable device and a buildable handoff. Keep the original features and constraints visible throughout the work. A schematic, assembled board, running firmware, desktop demo, and end-to-end tested product are different outcomes; report each at its actual maturity.

## Start from the current project

Read the user's requirements, existing files, and project rules before proposing new parts or architecture. Extract what is already settled: target user interaction, input/output, wireless and wired interfaces, power, size, supported computer systems, assembly route, budget, and available hardware. Ask only about an unresolved choice that changes the architecture or acceptance result. For an existing project, resume its actual stage rather than restarting intake.

Write or update a single [product record](assets/PRODUCT_RECORD.md) in the authorized project workspace when the task permits files. Preserve prior decisions and measurements; do not replace unknown values with plausible defaults. Give each supported hardware/firmware/software combination a version identity.

## Drive one complete path first

Choose one reference configuration that can demonstrate the whole user journey, then expand to optional functions and beginner/advanced or no-solder/solder variants. Treat each route as a separate claim of reproducibility. A computer-only mock-up may validate software but does not validate a device microphone or wireless transfer.

| Stage | Concrete result before moving on |
|---|---|
| Product contract | One user scenario, observable success criteria, supported platforms, reference configuration, variant boundaries, and open decisions |
| System slice | Interface and data path fixed end-to-end; part, power, memory/bandwidth, and computer-side feasibility checked from actual sources |
| Implementation | Hardware and assembly files, firmware, receiver, AI processing, and display built for that slice; versions linked |
| Integrated verification | A real device produces the intended computer-visible result; measurements and failures tied to the exact configuration |
| Teaching and handoff | Reproducible build/run/recovery instructions for each claimed route, costs and usage, source files, test evidence, and remaining limits |

Do useful independent work when a device, account, or tool is unavailable. Mark physical, compatibility, and endurance tests `not_run` until they are performed on the actual configuration. Do not make an unbuilt design sound like a tested product.

## Delegate board-specific work to the PCB skill

When the task reaches schematic, PCB, manufacturing files, assembly, or board bring-up, find and load the available `pcb-design-to-bringup` Skill and follow its stage-specific guidance. Discover its actual location through the current skills catalog or project; do not hard-code a machine path. If it is unavailable, continue system, firmware, software, and record work, and identify the missing board workflow before claiming board completion. Keep this Skill responsible for whole-product interfaces and end-to-end acceptance rather than duplicating PCB gates.

## Evidence and decisions

Use exact manufacturer part numbers, module/board revisions, firmware commits, protocol versions, desktop environment, and model names in implementation and test records. Separate requirements, calculations, static checks, simulated results, and physical measurements. A passed subassembly or app test cannot stand in for the full user scenario. When the product records voice through a device microphone, read [voice-device integration](references/voice-device-integration.md) before settling transport, firmware states, or acceptance.

Present a short next action and its reason at each handoff. Continue within the user's authorized scope; purchasing, payment, contacting vendors, and publishing require their own authorization. Explain unresolved decisions with concrete options and consequences, without adding routine permission pauses.

## Cost and deliverable meaning

Show both **parts consumed in one build** and **cash needed to obtain them**, including minimum order quantities, fabrication, assembly, shipping/tax where known, tools, rework, and ongoing AI/service fees. Keep unknown quotes unknown and refresh time-sensitive prices before purchase. Record hands-on time separately from machine or delivery waiting time. Use provider usage records for tokens, audio minutes, and charges; do not infer token counts from duration or label a per-minute charge as tokens.

At delivery, name the actual package: design/source files, firmware image and recovery method, receiver/app, BOM and sourcing, build guide, and test record as applicable. State whether a physical unit, assembly, hosting, subscriptions, and future support are included. Use the product record so a user can tell what they receive for each quoted amount.
