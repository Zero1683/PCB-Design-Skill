# G7-G8: Power-up, diagnostic firmware, functional tests, and troubleshooting

## Measurement request format

Request one discriminating measurement, or a group made under the same conditions. Specify:

```text
Board ID/revision: ...
Connections: supplies/USB/debuggers to disconnect; switch and button states
Instrument: DC voltage/resistance/diode/oscilloscope; range if needed
Black probe: identified ground test point or connector pin
Red probe: reference designator-pin (net), with recognizable orientation or diagram
Expected range: derived from circuit and device specifications for the actual load
Result format: value and unit; range or time trend if varying
Branches: results requiring power-off, and results leading to the next check
```

For inaccessible pads, identify exposed same-net resistors, capacitors, connectors, or vias from the project. Do not repeatedly ask for probes on hidden IC underside pads. Escalate to isolation/removal for significant evidence such as persistent near-zero resistance between two points; avoid purposeless rework.

## Unpowered checks

1. Disconnect battery, USB, and potentially powering adapters. Confirm the measured rail has substantially discharged using voltage mode before resistance/diode testing.
2. Record shorted-probe resistance. After full cooling, measure rails to ground, reset/boot pins, differential pairs, and suspect adjacent nets. A continuity beeper threshold is not a definition of a short.
3. Capacitor charging, protection diodes, and internal IC paths cause changing resistance and polarity-dependent readings. In-circuit resistance does not directly predict operating current.
4. Two nets pulled up to the same rail may read approximately the sum of their pull-up resistances. This does not establish a solder bridge. Compare low readings with the circuit, bare/neighboring boards, and lead resistance.
5. Verify battery-connector polarity with actual voltage and pin order, not wire color or a plastic notch alone. Never use resistance mode across a live battery.

## Current-limited power-up

Use the designed power input. Start short-circuit screening at a confirmed valid nominal voltage. Choose initial current limit from startup requirements and the circuit under test, and document expectations; 0.05 A or 0.5 A is not a universal value.

Stop sustained powering for persistent CC operation, voltage collapse, or rapid abnormal heating and investigate. After initial screening, allow the evaluated startup/peak current for functional tests. Resets caused by too-low current limits do not alone establish a circuit defect.

Record actual supply voltage/current, CV/CC state, regulator output, voltage near the load, and reset state together. A displayed 0 A may be below meter resolution or indicate failure to start; it is insufficient by itself.

Check input → rails → EN/RESET → boot pins → clock/ROM logs where applicable. “Warm” is only a description. Rated-temperature and power validation require suitable measurement and operating conditions; finger comfort is not an acceptance test.

## Recovery programming and device identification

- Distinguish native USB from an external USB-UART adapter. Record VID/PID, serial number, port, and cables. Do not assume another computer's or an old session's port number.
- Confirm a data-capable cable, actual board power, logic levels, and common ground. Handle multiple supplies according to the power-state table.
- Check adapter mode and idle TX voltage; inspect RX bias and specifications where needed. VCC measurement alone is insufficient, and input pins are not universally immune to back-powering. Correct logic-level compatibility before applying a level above the target's allowed range.
- Where appropriate, loop back the adapter with the target disconnected, then connect target TX/RX. Remove the loopback jumper before final wiring. Use RTS/DTR only with a defined reset circuit.
- Follow the specific chip's ROM BOOT/RESET sequence. Read identity and flash information and save handshake results.
- Back up configuration/templates that must survive flashing. Specify application-only versus full-chip programming. Do not routinely erase calibration or user data for troubleshooting.
- Confirm programming-tool exit status and hash/verification results, then check runtime logs. Adapter LEDs, one enumeration, or application LEDs do not replace this evidence.
- Descriptor failures/Code 43 cannot be attributed directly to blank firmware, missing drivers, or USB impedance. Isolate power, reset, boot, physical connection, and software state in layers.

## Minimal diagnostic firmware

Record target chip, SDK version, pin table, and firmware hash. Enable modules incrementally rather than activating all peripherals at once and obscuring fault sources.

1. Boot: revision, reset cause, key configuration, memory or fault counts where applicable.
2. GPIO: controllable LED on/off, button press/release, active level, debounce, and no conflicting drive against the circuit.
3. Bus: ACK/identity register, configuration write/readback, raw data, and error counts.
4. Sensors: stationary/orientation changes, multi-axis response, and manufacturer self-test. Record range, ODR, settling time, and criteria. Self-test is not full accuracy calibration.
5. Interrupts: independently verify output mode, routing registers, receiving GPIO, pulse width/level, and clearing. Internal pulls help identify floating behavior but do not prove continuity of the entire path.
6. Communication: sustained bidirectional data, length/checksum, packet boundaries, and reconnection. For packet-size-dependent failures, investigate protocol, driver, and buffer implementation rather than automatically reworking the PCB.
7. Power: maximum/nominal/minimum valid input, corresponding loads and radio bursts, voltage near the load. Report ripple/transients only with oscilloscope evidence and documented probe arrangement.
8. Wireless: scanning, connection, and data exchange are separate levels. Receiver confirmation and error rates provide stronger evidence than an advertised name alone.
9. Battery/shutdown: actual battery, standalone operation after removing external data/debug cables, off-state current, restart, low-battery policy, and required runtime. Seconds of logging do not establish hours of battery life.

Define repetitions, duration, load, voltage, and tolerances before testing from project requirements. EMC, eye diagrams, and other specialist tests are not mandatory for every project, but cannot be claimed passed when unperformed.

## Fault isolation

| Symptom | First discriminating checks | Avoid concluding |
|---|---|---|
| Low rail resistance/heating | Discharge/cooling, lead baseline, comparison board, sectional isolation | In-circuit 1 kΩ proves IC leakage; warmth proves failure |
| RESET stays low | Whether it remains low with button removed; RC, resistor network, same-net joints | The button must be defective, or reflashing will fix it |
| Boot nets read low between them | Correct pad pairing, both pull-up paths, bare versus assembled board | Any reading other than OL is a short |
| Repeated USB connection | RESET held/released behavior, supply, ROM mode, known cable | Immediately replace ESD protection |
| No UART output | Adapter enumeration/loopback, common ground, crossed wiring, boot state | RX LED off proves a failed chip |
| Working I²C, no interrupt | Registers, mode, GPIO, exposed test points, pulls | Sensor entirely failed, or interrupt already passed |
| Failure at specific USB packet lengths | Protocol boundaries, ZLP/buffers/timeouts, software | Impedance must be wrong |

Save the fault state before removal. Testing the removed device and PCB separately narrows causes. If both cease to be shorted, assembly is implicated, but not every component function is proven healthy. After rework, repeat affected functions and adjacent-net checks; one repaired board does not validate all boards.

If the user accepts disabling interrupts and polling instead, update functional scope, firmware, and power documentation while preserving the unresolved cause. Only the polling path may pass; original interrupt and sleep functions remain unverified.
