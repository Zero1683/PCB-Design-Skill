# Exact-part decisions and device-to-host acceptance

Read the relevant sections for exact-part decisions and for outcomes beyond a bare
PCB, such as a button, sensor or microphone producing a computer-visible result.
Use audio/transcription, wireless and battery/charging sections only when the
product has those features. An externally powered sensor needs its own input,
data-path and supply checks, not microphone or battery tests.
Use the project requirements and [existing requirement mapping](25-requirement-coverage.md)
as the authority for functions and thresholds. This reference adds a compact
engineering record and test sequence; it does not replace the G1/G2 part checks,
G7/G8 bring-up, or current-design evidence. Copy the
[Chinese project template](../assets/zh/PRODUCT_ACCEPTANCE.template.md) when useful.

## Lock the exact part before changing a circuit

For each function-critical IC, module and microphone, record one selected
**orderable manufacturer part number**. Identify a battery pack by its exact
model and supplier specification, including cell chemistry and protection, even
when it has no IC-style MPN. Preserve every part-number suffix. Separate the base
family, functional variant, physical package and shipping/reel suffix using the
manufacturer's ordering table; do not infer what a suffix means from its spelling.
Link the selected supplier entry, manufacturer datasheet revision and the exact
sections that govern the implemented pins, modes, limits and application circuit.
An unresolved part identity is `BLOCKED` for the affected circuit decision.

Compare five things against that one identity:

1. The fitted BOM line and supplier-resolved product, including approved alternate
   and DNP state.
2. The symbol pin names/numbers, native netlist, footprint pad numbers and package
   drawing orientation. Check the actual native objects, not a screenshot alone.
3. The selected variant's feature/options table, operating limits, truth tables,
   and any differing recommended external components.
4. The real battery, load, input source and firmware-controlled mode at each
   relevant operating corner. Recalculate resistor choices and tolerances using
   that variant's equations; include units and min/typ/max conditions.
5. The proposed edit's effect on charging, boot, test access, BOM and assembly.
   Recheck those affected functions after any part or value change.

When two reviewers disagree, write each claim beside the source section and
native net/measurement that would decide it. A repeated opinion is not evidence.
Do not implement a high-impact fix while the identity or circuit state is unknown.
Record a functional downgrade as a changed requirement, not a passed original test.

**Historical counterexample, not a default design:** one recorded review named
`BQ24072TRGTR` but applied advice for the similarly named `BQ24072` family.
TI lists `BQ24072TRGTR` under the T variant and describes its TS input as a
voltage-based divider from VIN to ground. The non-T datasheet describes a TS
current source. Therefore “remove/short the TS resistors” cannot be transferred
between these variants by name alone. The T datasheet also specifies the
applicable ISET programming range. Re-evaluate the actual net, resistor values,
battery thermistor and input conditions from the selected datasheet before making
a project-specific conclusion. The old discussion does not prove any current
board is correct or incorrect. Sources: [TI BQ2407xT Rev. C, device options,
pin functions and battery-pack temperature monitoring](https://www.ti.com/lit/ds/symlink/bq24072t.pdf),
[TI BQ2407x Rev. N, battery-pack temperature monitoring](https://www.ti.com/lit/ds/symlink/bq24072.pdf).

## Define one complete data path

Before selecting an interface or drawing its nets, choose a supported computer OS
and the specific transfer method. Record `device input/event → capture → transfer
→ host raw data → requested result`, with sample/event identity and units as
appropriate. For a USB sensor, check known sensor values through the saved host
data and result, plus startup, continuous acquisition and disconnect/recovery on
the actual USB supply.

For an audio product, “Bluetooth connects” does not tell whether audio
is a host microphone, a file sent over a custom data link, or something else.
Record the intended path in plain terms:

```text
button action → microphone capture → device buffer/storage → transfer →
host recording file → transcription → checked transcript → summary
```

For each arrow, name the implementing hardware/firmware/host component, the
data format, the acceptance criterion and the recovery owner. If a ready-made
development board is used first, bind the observed result to its exact board,
firmware and host versions. It is prototype evidence, not proof for a later PCB.

For recording products, define at least: button press/release and cancel behavior;
recording indicator;
sample rate, channels, bit depth/codec and maximum duration; where bytes are
kept before transfer; the transport and message boundaries; transfer completion
acknowledgment; host file naming and duplicate policy; transcription language;
summary format; and the behavior when the computer or AI service is unavailable.
Give each recording a stable ID so a retry cannot silently create two notes.

Estimate raw storage before committing the memory and transport plan:

`bytes = sample_rate_hz × channels × bits_per_sample / 8 × seconds`.

For illustration, 16 kHz, mono, 16-bit PCM for 60 s is 1,920,000 bytes before
headers and transport overhead. This is not a required format. Compare the
chosen device's actual usable memory/storage and **measured** end-to-end transfer
rate with the maximum recording and acceptable wait time. Advertising, pairing
or HID success is not evidence of audio transfer.

## Accept the function in layers (audio example)

For sensor or event products, use the same applicable layers with their actual
data and expected result; microphone capture and transcription are not required.

| Layer | What to run | Pass evidence |
|---|---|---|
| Contract review | Exact microphone interface and pins, clock/buffer budget, transport, host OS and file format | Sourced pin/resource table and a feasible worst-case size/time calculation |
| Software integration | Feed a known audio fixture through the host receiver/transcription/summary path | Input identity, saved audio, transcript and summary with versioned logs; mark hardware capture `NOT_RUN` |
| Device capture | Press the physical control; save the device-origin raw audio on the host; play it independently | Board/firmware ID, event times, expected vs received sample count, no unexplained truncation, silence or clipping |
| Full result | Transcribe and summarize that exact saved recording | Linked recording ID, preserved transcript, factual summary review against the recording |
| Recovery | Interrupt transfer, close receiver, retry and restart; test low-battery behavior only for a battery product | Explicit failed/pending state; no silent loss or duplicate final record; user indication matches actual state |

Choose repetitions, maximum wait, wireless distance where used, acceptable dropped samples and
audio quality before testing. A single successful file does not validate the
maximum duration or repeated use. Use fixed speech fixtures that include
numbers, negation and Chinese/English terms; review the transcript separately
from the summary so a fluent summary cannot conceal a missing or inverted fact.
Preserve actual failed cases with their inputs and versions. Never mark an
unavailable physical test `PASS` because its simulated path passed.

## Charge and runtime are operating states (battery products only)

Use the [power-state inventory](01-intake-and-recovery.md) and
[bring-up method](05-bringup-debug.md). For the chosen battery and charger,
record cell chemistry, capacity and usable range, charge-current limit,
connector polarity, pack protection/thermistor, source current limit and exact
charger operating mode. Derive allowed values from their datasheets. The
following cases matter when applicable:

| Case | Observe together |
|---|---|
| Battery only: idle, recording, transfer, sleep, wake | Battery-side voltage/current, load rail, resets, usable function |
| USB plus battery: idle and highest load | Input, BAT and system-rail voltage/current; charging or supplement state; temperature trend |
| USB present with absent/full/low battery | Startup and charger status versus actual BAT current, host behavior and restart |
| Input limit or weak source | Whether system remains stable and charging current changes as the selected charger specifies |
| Temperature-sense or charger fault state, if implemented | Actual sense signal/mode and recovery; an LED alone cannot establish charging |

Capture board revision, battery identity and condition, firmware hash, source,
instrument and test points for each run. Measure input and battery current
separately when evaluating simultaneous system load and charging. Charge-status
pins and LED states are observations, not substitutes for battery-current data.
Do not apply another battery or charger model's thresholds as generic limits.

For a first runtime estimate, measure currents at the **same battery-side
boundary** under the intended usage script and calculate
`I_avg_mA = Σ(I_state_mA × time_fraction_state)`;
`T_est_h = usable_capacity_mAh / I_avg_mA`. Fractions sum to 1. Include
advertising, connected idle, capture, transfer, retry and sleep as used. If
measurements are on different voltage rails, convert to power and account for
the actual conversion efficiency before combining them. State the assumed
usable capacity, temperature and cutoff. Then run the complete device on its
actual battery from a defined charged state to its intended low-battery stop,
using the same script; record observed time separately from the estimate.

## Record and hand off

Use existing `PROJECT.md`, `requirements.json`, `requirement-checks.json`,
`CHECKS.csv` and `HANDOFF.md`. Add project-specific check IDs for the selected
audio path and power states; link them to sourced requirements and current
observations. For other inputs, use the actual data path and power states instead
of the audio example. Omit irrelevant working-sheet examples or mark `N_A` with
the scope reason; do not count them as passed or waive registered required checks.
The template is a compact working sheet, not a second release
gate or a way to bypass the registry. Each result states `NOT_RUN`, `BLOCKED`,
`PASS` or `FAIL`, the tested conditions, actual number/file, acceptance range,
board/firmware/host identity and evidence path. A changed board, firmware,
battery, host receiver or AI model invalidates only the affected conclusions;
review the dependency before carrying any result forward.
