# Agent-operated calculations and fabrication cost choices

## Select a model before calculating

Start from the circuit question: DC load voltage, source capacity, load-step droop, transmission-line impedance, thermal behavior or component rating. The word "impedance" alone does not select a model. A manufacturer trace-impedance calculator cannot evaluate a regulator's PDN frequency response.

Gather inputs from the exact-part datasheets, current native geometry and selected fabrication process. Keep nominal/min/max values, units and sources in the project. A board thickness is not the signal-to-reference dielectric height. Finished copper differs from starting foil. Nearby ground, coating and reference-plane gaps change the supported transmission-line model.

Use, in order:

1. A local verified model covering the actual inputs and geometry.
2. An available documented manufacturer calculator API or applicable field solver.
3. Browser control of the manufacturer's current calculator. Read the page before selecting controls; never guess a private endpoint or reuse stale selectors blindly.

If a page requires login or contains inaccessible inputs, continue other work and identify the missing fact. Do not ask a beginner to perform arithmetic the agent can do. Physical measurements still need the person holding the board.

## Local models

Use `electrical_calcs.py` for the existing power, LDO, DC-path, transient and fabrication estimates. New kinds:

- `microstrip`: `width_mm`, `height_mm`, `copper_mm` (finished thickness), `er`. Explicitly set `geometry: isolated_microstrip`, `soldermask: false`, `nearby_coplanar_copper: false`. Hammerstad–Jensen quasi-static model with thickness correction; the correction uses normalized W/H. Source: [Qucs technical reference, equations 11.4–11.6, 11.15–11.18, 11.22–11.23](https://qucs.sourceforge.net/tech/node75.html). Formula reproduction is project-authored; [scikit-rf 1.8.0](https://github.com/scikit-rf/scikit-rf/blob/v1.8.0/skrf/media/mline.py) supplies an independent implementation for numerical cross-checks.
- Supported local domain: `1 <= er <= 20`, `0.1 <= W/H <= 20`, `0 <= t/H <= 0.1`, `t/W <= 0.2`. These conservative wrapper limits are not a claim of complete physical accuracy. Most soldermasked PCB traces require another applicable model. Do not set mask/coplanar flags false merely to obtain a result.
- Optional `ranges` supplies `[min,max]` for all four dimensions/material inputs. Output reports 16 sampled corners, not a certified bound or guaranteed fabrication tolerance. An unsupported corner rejects the calculation.
- `microstrip_width`: adds positive `target_ohm` and explicit `width_bounds_mm`; bounded bisection proposes a nominal width only. Round to the fabricator's supported precision and re-evaluate actual width and tolerances. No automatic rule relaxation or target expansion.
- `i2c_pullup`: supply maximum, VOL maximum, pin sink-current specification, total bus capacitance, maximum 30–70% rise time, selected effective resistance and tolerance. Uses `Rmin=(Vmax-VOLmax)/IOL`, `Rmax=tr/(0.8473*Cb)`; see [TI SLVA689](https://www.ti.com/lit/an/slva689/slva689.pdf). Aggregate parallel pull-ups first. Negative resistance margins require repair; a calculated interval does not prove measured waveform quality.

Every item still requires `id`, `source`, `conditions`. Results remain `CALCULATED`; model agreement is not board acceptance. A strict JSON parser rejects duplicate keys, nonfinite inputs and nonfinite arithmetic output. Unknown model/geometry, incomplete inputs and unbracketed targets fail explicitly. No additional runtime package is required for these local estimates.

## Browser fallback record

Open the correct regional manufacturer's current calculator, select the actual stackup/layers and geometry, enter all fields, trigger calculation and read back the displayed inputs and result. Preserve warnings and a screenshot or structured page capture in the project. Do not publish screenshots containing account information.

`calculator_observation.py` verifies declared request/observation consistency:

- Request: `schema:1`, `baseline_id`, exact HTTPS `calculator_url`, `model`, nonempty `inputs` mapping field names to `{value,unit}`, and `outputs` mapping requested positive numeric result names to their units.
- Observation: same schema/baseline/URL/model, `request_digest`, complete `displayed_inputs`, `state: computed`, timezone-aware `observed_at`, `results` mapping names to `{value,unit}`, explicit `warnings` array and `evidence: {path,sha256}` for a nonempty project-local capture.
- Use `python scripts/calculator_observation.py --root /project --request /project/calc-request.json --observation /project/calc-observation.json`.

`OBSERVATION_MATCHED` verifies the recorded fields and capture hash, not the authenticity of a webpage or model suitability. Inspect the capture and warnings. No saved result should be relabeled PASS just because this helper exits zero. Model, inputs, stackup or layout changes require a fresh computation.

## Cost without removing necessary controls

Compare feasible alternatives against identical confirmed functions and margins. Use ordinary processes when sufficient; prefer standard stackups, supported drill sizes and repairable footprints before premium options. Keep electronics-only purchase estimates separate from fabrication/assembly costs.

Do not assume controlled-impedance service always costs extra or is always required. Obtain the actual regional process and quote. [JLCPCB's calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator) notes process-specific inputs and limits. The [domestic impedance design guide](https://www.jlc.com/portal/server_guide_38565.html) is another source to consult for the selected domestic service; regional offers must not be substituted silently.

An impedance calculation chooses geometry under a model. Fabrication control determines process/tolerance verification. Canceling the latter does not preserve a guaranteed impedance tolerance. Where ordinary fabrication has enough justified margin, show that lower-cost choice; where it does not, retain the necessary service or propose a different architecture without silently downgrading function.
