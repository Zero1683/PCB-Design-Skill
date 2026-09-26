# Voice device integration

Read this only for products that record, transmit, or process sound. These are decision and acceptance prompts, not a fixed chip or service stack.

## Fix the audio path before parts selection

Write the route from **device microphone → sampled audio → local buffer/storage → physical transport → computer receiver → transcription → structured result → user-visible page**. Name which step owns each file and error. A BLE/HID keyboard event or successful pairing does not prove that recorded audio reaches the computer. If the device merely triggers the computer microphone, label that as a distinct variant.

Specify the microphone interface and actual part/module, sample format, sample rate, channels, maximum clip duration, expected bytes, buffer headroom, and transport protocol. For uncompressed PCM, `bytes = seconds × samples/second × bits/sample ÷ 8 × channels`; add headers, acknowledgements, retries, and protocol overhead separately. Compare that amount with measured or documented storage and effective transport throughput. A format or bitrate here is a design choice, never an untested default.

For wireless transfer, define clip ID, sequence/length, end-of-clip indication, integrity check, acknowledgement, bounded retry, and recovery after disconnection. Record device, OS, and receiver versions. Measure audio duration and bytes received, transfer time, and lost/retried frames on the actual target setup. If USB is used as a development path, keep its acceptance separate from the promised wireless route.

## Give the user a truthful state

Define button and indicator behavior for ready, recording, finishing, transferring, AI processing, completed, and failed. The final success signal means the result has been saved and can be opened, not merely that bytes left the device. Associate button events, audio, AI requests, and displayed output by a stable `recording_id` so retries do not create silent duplicates. Define cancellation, maximum duration, full-buffer behavior, and a recovery path when the receiver or network is unavailable.

Retain original audio, raw transcription, edited transcription if any, and the final summary as distinguishable artifacts. Check the requested output shape, such as one sentence plus three key points, and include a way to inspect or correct transcript errors. An AI-formatted page is not proof that names, numbers, dates, or negations were captured correctly.

## Power and end-to-end verification

On the actual selected board, reconcile microphone/LED/buttons/radio/USB with pin, peripheral, and boot-resource limits. For a rechargeable device, document the actual cell, protection, charger, system power path, charge settings, connector polarity, and supported charging/operating modes using the exact part datasheets. Estimate runtime from all product states, then distinguish estimate from current and endurance measurements on the assembled unit.

The minimum complete demonstration is: press and release the device button, capture known spoken content with its microphone, deliver a valid clip to the target computer, transcribe it, save the requested structured result, open that result, and link it back to the clip ID. Repeat expected recovery cases such as receiver absent, wireless interruption, AI failure, and low battery. Record the actual pass/fail/not-run status; a component simulation or source inspection cannot pass this demonstration.

For beginner, advanced, no-solder, and soldered guides, name the exact starting parts, revisions, wiring or assembly, software versions, target computer, and recovery method. Test each route with a person who did not build it before claiming it is reproducible. One successful route does not validate the others.
