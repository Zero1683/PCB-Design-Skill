#!/usr/bin/env python3
"""Reproducible first-order electrical calculations. Explicit SI units; no impedance solver."""
import argparse
import json
import math
from pathlib import Path


def number(data, key, zero=False):
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or (value < 0 if zero else value <= 0):
        raise ValueError(f'{key} must be a finite {"nonnegative" if zero else "positive"} number')
    return value


def calculate(item):
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
    else: raise ValueError(f'Unknown calculation kind: {kind}')
    return {'id': item['id'], 'kind': kind, 'inputs': item, 'results': result,
            'limitations': limit, 'status': 'CALCULATED', 'hardware_validation': 'NOT_RUN'}


def run(data):
    if data.get('schema') != 1 or not isinstance(data.get('baseline_id'), str) or not data['baseline_id'].strip():
        raise ValueError('Provide schema=1 and baseline_id')
    items = data.get('calculations')
    if not isinstance(items, list) or not items: raise ValueError('Provide calculations')
    seen = set(); outputs = []
    for item in items:
        for key in ('id', 'source', 'conditions'):
            if not isinstance(item.get(key), str) or not item[key].strip(): raise ValueError(f'Missing {key}')
        if item['id'] in seen: raise ValueError('Duplicate calculation ID')
        seen.add(item['id']); outputs.append(calculate(item))
    return {'schema': 1, 'baseline_id': data['baseline_id'], 'scope': 'first-order-estimates', 'calculations': outputs}


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--input', type=Path, required=True)
    args = p.parse_args()
    try: result = run(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc: p.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__': main()
