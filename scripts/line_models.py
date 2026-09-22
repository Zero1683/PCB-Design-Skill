"""Bounded quasi-static, isolated microstrip estimates. No fabrication or SI approval."""
import itertools
import math
import workflow_io as io

MODEL = 'hammerstad-jensen-quasistatic-v1'
REFERENCE = 'https://qucs.sourceforge.net/tech/node75.html'
KEYS = ('width_mm', 'height_mm', 'copper_mm', 'er')


def microstrip(width_mm, height_mm, copper_mm, er):
    for key, value in zip(KEYS, (width_mm, height_mm, copper_mm, er)):
        io.finite(value, key)
    if min(width_mm, height_mm) <= 0 or copper_mm < 0:
        raise ValueError('Positive W/H and nonnegative copper thickness required')
    ratio, thickness = width_mm / height_mm, copper_mm / height_mm
    # Deliberately narrower engineering-use domain than the published zero-thickness formula.
    if not (1 <= er <= 20 and .1 <= ratio <= 20 and thickness <= .1 and copper_mm / width_mm <= .2):
        raise ValueError('Outside supported microstrip domain; use an applicable solver')
    extra_air = 0 if thickness == 0 else thickness / math.pi * math.log1p(
        4 * math.e / thickness * math.tanh(math.sqrt(6.517 * ratio)) ** 2)
    extra_dielectric = extra_air * (1 + 1 / math.cosh(math.sqrt(er - 1))) / 2
    corrected = ratio + extra_dielectric
    a = 1 + math.log((corrected**4 + (corrected / 52)**2) / (corrected**4 + .432)) / 49
    a += math.log1p((corrected / 18.1)**3) / 18.7
    b = .564 * ((er - .9) / (er + 3)) ** .053
    effective = (er + 1) / 2 + (er - 1) / 2 * (1 + 10 / corrected) ** (-a * b)
    def air_impedance(u):
        f = 6 + (2 * math.pi - 6) * math.exp(-(30.666 / u) ** .7528)
        return 376.730313668 / (2 * math.pi) * math.log(f / u + math.sqrt(1 + (2 / u)**2))
    zr = air_impedance(corrected)
    return {'impedance_ohm': zr / math.sqrt(effective),
            'effective_er': effective * (air_impedance(ratio + extra_air) / zr)**2}


def calculate(item):
    if item.get('geometry') != 'isolated_microstrip' or item.get('soldermask') is not False or item.get('nearby_coplanar_copper') is not False:
        raise ValueError('Only isolated uncoated microstrip supported; masked/coplanar/differential geometry requires another solver')
    values = {key: item[key] for key in KEYS}
    result = microstrip(**values)
    if 'ranges' in item:
        ranges = item['ranges']
        if not isinstance(ranges, dict) or set(ranges) != set(KEYS): raise ValueError('Supply all four explicit input ranges')
        for key, limits in ranges.items():
            if not isinstance(limits, list) or len(limits) != 2: raise ValueError('Range needs [min,max]')
            low, high = [io.finite(v, key) for v in limits]
            if not low <= values[key] <= high: raise ValueError('Nominal must lie within ordered range')
        points = [microstrip(**dict(zip(KEYS, combination)))['impedance_ohm']
                  for combination in itertools.product(*(ranges[k] for k in KEYS))]
        result.update(sampled_corner_min_ohm=min(points), sampled_corner_max_ohm=max(points), corner_count=len(points))
    if 'target_ohm' in item:
        target = io.finite(item['target_ohm'], 'target')
        if target <= 0: raise ValueError('Target must be positive')
        result['nominal_error_ohm'] = result['impedance_ohm'] - target
    result['model'] = MODEL
    result['reference'] = REFERENCE
    return result


def synthesize(item):
    target = io.finite(item['target_ohm'], 'target')
    bounds = item.get('width_bounds_mm')
    if not isinstance(bounds, list) or len(bounds) != 2: raise ValueError('Explicit width search bounds required')
    low, high = [io.finite(x, 'width bound') for x in bounds]
    if target <= 0 or not 0 < low < high: raise ValueError('Invalid target/search bounds')
    def at(width): return calculate({**item, 'width_mm': width})['impedance_ohm']
    if 'ranges' in item: raise ValueError('Synthesize nominal first, then evaluate explicit tolerance ranges')
    if not at(high) <= target <= at(low): raise ValueError('Target not bracketed within supported bounds')
    for _ in range(60):
        middle = (low + high) / 2
        if at(middle) > target: low = middle
        else: high = middle
    width = (low + high) / 2
    return {**calculate({**item, 'width_mm': width}), 'suggested_width_mm': width,
            'width_requires_fabrication_grid_rounding_and_recheck': True}
