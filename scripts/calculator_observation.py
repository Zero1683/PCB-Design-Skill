"""Bind a browser calculator observation to exact requested inputs and captured evidence."""
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
import workflow_io as io
from evidence_binding import reference


def validate_inputs(values):
    if not isinstance(values, dict) or not values: raise ValueError('Nonempty named calculator inputs required')
    for name, field in values.items():
        io.text(name, 'input name')
        if not isinstance(field, dict) or set(field) != {'value', 'unit'}: raise ValueError('Each input needs value and unit')
        io.text(field['unit'], 'unit or explicit dimensionless/text')
        if isinstance(field['value'], str): io.text(field['value'], 'input value')
        else: io.finite(field['value'], 'input value')


def evaluate(root, request, observation):
    root = io.no_link(root).resolve(strict=True)
    for doc in (request, observation):
        if not isinstance(doc, dict) or type(doc.get('schema')) is not int or doc['schema'] != 1: raise ValueError('schema=1 required')
        io.text(doc.get('baseline_id'), 'baseline')
    if request['baseline_id'] != observation['baseline_id']: raise ValueError('Calculator baseline mismatch')
    io.text(request.get('model'), 'calculator model')
    url = request.get('calculator_url')
    if not isinstance(url, str) or urlsplit(url).scheme != 'https' or not urlsplit(url).hostname:
        raise ValueError('Exact HTTPS calculator URL required')
    validate_inputs(request.get('inputs')); validate_inputs(observation.get('displayed_inputs'))
    if observation.get('request_digest') != io.digest(request): raise ValueError('Calculator request changed')
    if observation.get('calculator_url') != url or observation.get('model') != request['model']:
        raise ValueError('Wrong calculator or model')
    if request['inputs'] != observation['displayed_inputs']: raise ValueError('Displayed inputs differ from requested inputs/units')
    if observation.get('state') != 'computed': raise ValueError('Result was not observed after computation')
    time = datetime.fromisoformat(io.text(observation.get('observed_at'), 'observation time').replace('Z', '+00:00'))
    if time.tzinfo is None: raise ValueError('Observation time needs timezone')
    reference(root, observation.get('evidence'))
    results = observation.get('results'); validate_inputs(results)
    expected = request.get('outputs')
    if not isinstance(expected, dict) or not expected or set(expected) != set(results):
        raise ValueError('Observed result names must match requested outputs')
    for name, unit in expected.items():
        io.text(unit, 'expected output unit')
        if results[name]['unit'] != unit or io.finite(results[name]['value'], 'numeric result') <= 0:
            raise ValueError('Output unit mismatch or nonpositive calculator result')
    if not isinstance(observation.get('warnings'), list) or any(not isinstance(x,str) or not x.strip() for x in observation['warnings']):
        raise ValueError('Record all calculator warnings explicitly, including empty list')
    return {'state': 'OBSERVATION_MATCHED', 'baseline_id': request['baseline_id'],
            'request_digest': io.digest(request), 'results': results, 'warnings': observation['warnings'],
            'engineering_acceptance': 'REQUIRES_MODEL_AND_WARNING_REVIEW',
            'scope': 'declared browser observation integrity; does not authenticate page contents or prove impedance control'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True);p.add_argument('--request', type=Path, required=True);p.add_argument('--observation', type=Path, required=True)
    a=p.parse_args()
    try:
        print(io.encoded(evaluate(a.root,io.read(io.no_link(a.request)),io.read(io.no_link(a.observation)))).decode()); return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:p.exit(2, 'ERROR: '+str(exc)+'\n')


if __name__=='__main__':raise SystemExit(main())
