#!/usr/bin/env python3
"""Run the bundled PCB inspection toolkit. Python 3.10+. No EDA connection."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1] / 'vendor/pcb-skill-toolkit/scripts'
TOOLS = {
    'import': 'placement/import_easyeda.py',
    'courtyard': 'placement/courtyard_check.py',
    'bodies': 'placement/body_clearance.py',
    'channels': 'placement/channels.py',
    'gerber': 'verify/gerber.py',
    'drills': 'verify/drill_census.py',
    'mask': 'verify/mask_check.py',
    'outline': 'verify/outline_check.py',
    'clearance': 'verify/clearance.py',
    'raster': 'verify/raster.py',
    'nets': 'verify/netlist_assert.py',
    'reconcile': 'verify/pad_reconcile.py',
    'mesh': 'verify/mesh3d.py',
    'dsn-rewrite': 'routing/dsn_rewrite.py',
    'dsn-slim': 'routing/dsn_slim.py',
    'ses-import': 'routing/ses_import.py',
    'route-accept': 'routing/route_accept.py',
    'route-watch': 'routing/route_supervise.py',
}


def value(args, flag):
    if args.count(flag) != 1:
        raise ValueError(f'Provide exactly one {flag} with the actual project value')
    index = args.index(flag) + 1
    if index == len(args) or args[index].startswith('--'):
        raise ValueError(f'Missing value for {flag}')
    return args[index]


def inspection_arguments(tool, args):
    """Reject ignored/misspelled manual-argv switches before launching a checker."""
    configs = {
        'route-accept': (1, {'--baseline', '--protected', '--plane-nets', '--expect-open', '--clearance', '--top', '--json'}, set()),
        'mask': (2, {'--tol', '--top', '--json'}, {'--assume-all-pads', '--allow-partial-openings'}),
        'nets': (2, {'--plane-nets', '--json'}, set()),
    }
    if tool not in configs: return
    count, values, switches = configs[tool]
    seen, positional, i = set(), [], 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('-'):
            if len(positional) != count: raise ValueError('Input files must precede options')
            if arg not in values | switches: raise ValueError('Unknown option: ' + arg)
            if arg in seen: raise ValueError('Duplicate option: ' + arg)
            seen.add(arg)
            if arg in values:
                if i + 1 == len(args) or args[i+1].startswith('--'): raise ValueError('Missing value: ' + arg)
                raw = args[i+1]
                if arg == '--top':
                    if not raw.isdecimal() or int(raw) < 1: raise ValueError('--top must be a positive integer')
                elif arg in ('--tol', '--clearance'):
                    number = float(raw)
                    if not math.isfinite(number) or number < 0 or (arg == '--clearance' and number == 0):
                        raise ValueError(arg + ' must be finite and nonnegative (clearance positive)')
                elif arg in ('--protected', '--plane-nets', '--expect-open'):
                    names = raw.split(',')
                    if any(not name.strip() for name in names) or len({name.strip() for name in names}) != len(names):
                        raise ValueError(arg + ' requires unique nonempty names')
                elif not raw.strip(): raise ValueError('Empty option value: ' + arg)
                i += 1
        else: positional.append(arg)
        i += 1
    if len(positional) != count: raise ValueError('Expected %d input files for %s' % (count, tool))


def preflight(tool, args):
    if args == ['--selftest']: return
    inspection_arguments(tool, args)
    if tool == 'import':
        rules = json.loads(Path(value(args, '--rules')).read_text(encoding='utf-8'))
        layers = json.loads(Path(value(args, '--layers')).read_text(encoding='utf-8'))
        required = ('clearance','hole_to_hole','edge_clearance','via_pad','via_drill',
                    'pad_to_outline','min_courtyard_gap')
        for key in required:
            v = rules.get(key) if isinstance(rules,dict) else None
            if type(v) not in (int,float) or not math.isfinite(v) or v <= 0:
                raise ValueError(f'rules.{key} must be an explicit positive mm value')
        if rules['via_drill'] >= rules['via_pad']:
            raise ValueError('via_drill must be smaller than via_pad')
        required_layers = {'copper','top','bottom','solid_planes','assembly_outline',
                           'silkscreen','multi','board_outline','mirror_axis'}
        if not isinstance(layers,dict) or not required_layers <= layers.keys():
            raise ValueError('Provide the full measured layer map, including solid_planes and mirror_axis')
        for key in ('copper','solid_planes','silkscreen'):
            v = layers[key]
            if not isinstance(v,list) or any(type(n) is not int or n <= 0 for n in v) or len(set(v)) != len(v):
                raise ValueError(f'layers.{key} must be a list of unique positive layer IDs')
        for key in ('top','bottom','assembly_outline','multi','board_outline'):
            if type(layers[key]) is not int or layers[key] <= 0:
                raise ValueError(f'layers.{key} must be a positive layer ID')
        if (layers['top'] == layers['bottom'] or
            not {layers['top'],layers['bottom']} <= set(layers['copper']) or
            not set(layers['solid_planes']) <= set(layers['copper']) or
            layers['mirror_axis'] not in ('x','y')):
            raise ValueError('Inconsistent copper layers or mirror convention')
    for flag in {'clearance':('--rule','--res'), 'channels':('--track-width',)}.get(tool, ()):
        v = float(value(args,flag))
        if not math.isfinite(v) or v <= 0: raise ValueError(f'{flag} must be positive and finite')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tool', choices=sorted(TOOLS))
    parser.add_argument('args', nargs=argparse.REMAINDER)
    opts = parser.parse_args(argv)
    try:
        preflight(opts.tool,opts.args)
    except (ValueError,OSError) as error:
        print(f'INPUT ERROR: {error}',file=sys.stderr)
        return 2
    # Argument list, never a shell string. Child errors and coverage messages survive.
    return subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/TOOLS[opts.tool]),*opts.args]).returncode


if __name__=='__main__': raise SystemExit(main())
