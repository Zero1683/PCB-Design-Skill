#!/usr/bin/env python3
"""Reproducible first-order electrical calculations. Explicit SI units; no impedance solver."""
import argparse
import json
import math
from pathlib import Path
import workflow_io as io


def number(data, key, zero=False):
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or (value < 0 if zero else value <= 0):
        raise ValueError(f'{key} must be a finite {"nonnegative" if zero else "positive"} number')
    return value


def calculate(item):
    if not isinstance(item, dict): raise ValueError('Calculation must be an object')
    kind = item['kind']
    n = lambda key, zero=False: number(item, key, zero)
    if kind == 'converter':
        vin, vout, iout, eta = n('vin_V'), n('vout_V'), n('iout_A', True), n('efficiency')
        if eta > 1: raise ValueError('efficiency must be <= 1')
        pout = vout * iout
        result = {'pout_W': pout, 'iin_A': pout / (vin * eta), 'loss_W': pout * (1 / eta - 1)}
        limit = 'Steady operating point only; efficiency must match load/Vin. Excludes unmodeled startup and quiescent current.'
    elif kind == 'ldo':
        vin, vout, iout = n('vin_V'), n('vout_V'), n('iout_A', True)
        if vin < vout: raise ValueError('LDO input is below requested output')
        iq, dropout = n('iq_A', True), n('dropout_V', True)
        result = {'loss_W': (vin-vout)*iout + vin*iq, 'headroom_V': vin-vout,
                  'dropout_margin_V': vin-vout-dropout, 'iin_A': iout+iq}
        limit = 'Check dropout at actual current/temperature; package thermal limits need board-specific analysis.'
    elif kind == 'dc_path':
        segments = item['segments']
        if not isinstance(segments, list) or not segments: raise ValueError('Provide all modeled path segments')
        resistances = []
        for segment in segments:
            if segment['kind'] == 'trace':
                # rho in ohm*m, length/width in mm, thickness in micrometres.
                resistances.append(number(segment, 'rho_ohm_m') * number(segment, 'length_mm') /
                                   (number(segment, 'width_mm') * number(segment, 'thickness_um') * 1e-6))
            elif segment['kind'] == 'lumped':
                resistances.append(number(segment, 'resistance_ohm', True))
            else: raise ValueError('Path segment kind must be trace or lumped')
        resistance, current = sum(resistances), n('current_A', True)
        drop = resistance * current
        result = {'segment_resistance_ohm': resistances, 'total_resistance_ohm': resistance,
                  'drop_V': drop, 'loss_W': current*drop, 'drop_margin_V': n('allowed_drop_V')-drop}
        limit = 'DC model only. Include forward and return paths, contacts, vias and temperature-adjusted resistance. No ampacity or AC impedance verdict.'
    elif kind == 'transient_budget':
        delta_i, delta_v, dt = n('step_A'), n('allowed_droop_V'), n('response_s')
        esr, esl, rise = n('esr_ohm', True), n('esl_H', True), n('rise_s')
        parasitic = delta_i*esr + esl*delta_i/rise
        available = delta_v-parasitic
        result = {'target_impedance_ohm': delta_v/delta_i, 'esr_esl_step_V': parasitic,
                  'capacitive_droop_budget_V': available,
                  'ideal_min_effective_capacitance_F': delta_i*dt/available if available > 0 else None,
                  'budget_feasible_in_model': available > 0}
        limit = 'Simplified step/charge budget, not actual Z(f), loop stability, antiresonance or a capacitor recommendation. Validate effective C and regulator response.'
    elif kind == 'mask_pair':
        openings = []
        for side in ('left', 'right'):
            pad = n(f'{side}_pad_width_mm')
            expansion = item[f'{side}_expansion_per_side_mm']
            if isinstance(expansion, bool) or not isinstance(expansion, (int, float)) or not math.isfinite(expansion):
                raise ValueError('Mask expansion must be a finite signed number')
            opening = pad + 2*expansion
            if opening <= 0 or not math.isfinite(opening):
                raise ValueError('Mask opening must remain finite and positive; tenting is a different model')
            openings.append(opening)
        web = n('pitch_mm') - sum(openings)/2
        result = {'left_opening_mm': openings[0], 'right_opening_mm': openings[1],
                  'nominal_web_mm': web, 'web_margin_mm': web-n('required_web_mm')}
        limit = 'Aligned projected widths, symmetric per-side expansion per pad. No registration/process compensation, paste model, polygon validation or SMD/NSMD approval.'
    elif kind == 'escape_channel':
        count = item['trace_count']
        if type(count) is not int or count < 1:
            raise ValueError('trace_count must be a positive integer')
        gap = n('pitch_mm') - (n('left_pad_width_mm')+n('right_pad_width_mm'))/2
        width, clearance = n('trace_width_mm'), n('clearance_mm')
        required = count*width + (count+1)*clearance
        result = {'gap_mm': gap, 'required_gap_mm': required,
                  'gap_margin_mm': gap-required, 'single_trace_max_width_mm': gap-2*clearance}
        limit = 'Straight aligned channel only. Account for tolerances in inputs; turns, vias, staggered pads, antipads, layer topology and full escape routability are not assessed.'
    elif kind == 'annular_ring':
        basis = item['hole_basis']
        if basis not in ('drill', 'finished'):
            raise ValueError('hole_basis must be drill or finished and match the sourced fabrication rule')
        nominal = (n('land_diameter_mm')-n('hole_diameter_mm'))/2
        minimum = nominal-n('radial_offset_mm', True)
        result = {'nominal_ring_mm': nominal, 'offset_adjusted_ring_mm': minimum,
                  'ring_margin_mm': minimum-n('required_ring_mm')}
        limit = 'Circular pad/hole screening only. Use matching hole basis and dimensional corners; radial offset is explicit. No plating conversion, slots, inner-layer or fabrication verdict.'
    elif kind in ('microstrip', 'microstrip_width'):
        import line_models
        result = line_models.calculate(item) if kind == 'microstrip' else line_models.synthesize(item)
        limit = 'Quasi-static isolated uncoated microstrip only. No differential, coplanar, dispersion, loss, discontinuity, mask, process guarantee or PDN model. Corner samples are sensitivity estimates, not certified bounds.'
    elif kind == 'i2c_pullup':
        vmax, vol, sink = n('supply_max_V'), n('vol_max_V', True), n('sink_A')
        cap, rise = n('bus_capacitance_F'), n('rise_time_max_s')
        if vmax <= vol: raise ValueError('Supply must exceed VOL')
        resistance, tolerance = n('resistance_ohm'), n('tolerance', True)
        if tolerance >= 1: raise ValueError('Tolerance must be a fraction below 1')
        minimum, maximum = (vmax-vol)/sink, rise/(.8473*cap)
        result = {'r_min_ohm': minimum, 'r_max_ohm': maximum,
                  'sink_margin_ohm': resistance*(1-tolerance)-minimum,
                  'rise_margin_ohm': maximum-resistance*(1+tolerance),
                  'feasible_interval': minimum <= maximum}
        limit = '30%-70% RC rise model; sum parallel pull-ups first. Verify actual pin sink rating, bus capacitance and mode; no active rise accelerators or bus waveform validation.'
    else: raise ValueError(f'Unknown calculation kind: {kind}')
    # Library callers must receive the same finite-result guarantee as CLI callers.
    io.encoded(result)
    return {'id': item['id'], 'kind': kind, 'inputs': item, 'results': result,
            'limitations': limit, 'status': 'CALCULATED', 'hardware_validation': 'NOT_RUN'}


def run(data):
    if not isinstance(data, dict) or type(data.get('schema')) is not int or data['schema'] != 1 or not isinstance(data.get('baseline_id'), str) or not data['baseline_id'].strip():
        raise ValueError('Provide schema=1 and baseline_id')
    items = data.get('calculations')
    if not isinstance(items, list) or not items: raise ValueError('Provide calculations')
    seen = set(); outputs = []
    for item in items:
        if not isinstance(item, dict): raise ValueError('Calculation must be an object')
        for key in ('id', 'source', 'conditions'):
            if not isinstance(item.get(key), str) or not item[key].strip(): raise ValueError(f'Missing {key}')
        if item['id'] in seen: raise ValueError('Duplicate calculation ID')
        seen.add(item['id']); outputs.append(calculate(item))
    return {'schema': 1, 'baseline_id': data['baseline_id'], 'scope': 'first-order-estimates', 'calculations': outputs}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--input', type=Path, required=True)
    args = p.parse_args()
    try: result = run(io.read(args.input))
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc: p.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__': main()
