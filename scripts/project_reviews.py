"""Source-bound optional engineering reviews. No EDA writes or supplier approval."""
import argparse
from pathlib import Path
import workflow_io as io
import evidence_binding as eb


def exact(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys.split()):
        raise ValueError('Invalid fields: '+label)
    return value


def index(rows, key, label, allow_empty=False):
    if not isinstance(rows, list) or (not rows and not allow_empty):
        raise ValueError('Nonempty list required: '+label)
    result = {}
    for row in rows:
        if not isinstance(row, dict): raise ValueError('Invalid row: '+label)
        name = io.text(row.get(key), label+' identity')
        if name != name.strip() or name in result: raise ValueError('Duplicate/untrimmed identity: '+label)
        result[name] = row
    return result


def assembly(expected, observed):
    exact(expected, 'coordinate_frame components position_tolerance_mm angle_tolerance_deg', 'assembly contract')
    exact(observed, 'coordinate_frame bom submitted imported manual_browser_edits', 'assembly observation')
    frame = exact(expected['coordinate_frame'],'units origin axes angle_view rotation bottom','coordinate frame')
    io.text(frame['origin'],'coordinate origin')
    required={'units':'mm','axes':'X-right/Y-down','angle_view':'assembly-side','rotation':'clockwise','bottom':'normalized'}
    if any(frame[k]!=v for k,v in required.items()): raise ValueError('Unsupported coordinate convention')
    exact(observed['coordinate_frame'],'units origin axes angle_view rotation bottom','observed coordinate frame')
    if frame != observed['coordinate_frame']: raise ValueError('Coordinate conventions differ; normalize from documented adapter')
    pt = io.finite(expected['position_tolerance_mm'], 'position tolerance')
    at = io.finite(expected['angle_tolerance_deg'], 'angle tolerance')
    if not 0 < pt <= .1 or not 0 < at <= 1: raise ValueError('Tolerance outside supported limits')
    if type(observed['manual_browser_edits']) is not bool: raise ValueError('Explicit browser edit state required')
    components = index(expected['components'], 'ref', 'board components')
    wanted = {}
    for ref, row in components.items():
        exact(row, 'ref fitted part x_mm y_mm side rotation_deg', 'board component')
        if type(row['fitted']) is not bool: raise ValueError('Explicit fitted state required')
        if row['fitted']: wanted[ref] = row
    if not wanted: raise ValueError('Assembly review requires populated components')
    failures = []
    if observed['manual_browser_edits']: failures.append({'kind':'unreconciled_browser_edits'})
    for field in ('bom', 'submitted', 'imported'):
        actual = index(observed[field], 'ref', field, allow_empty=True)
        for ref in sorted(set(wanted) | set(actual)):
            if ref not in wanted or ref not in actual:
                failures.append({'kind':'reference_set', 'table':field, 'ref':ref}); continue
            a, b = wanted[ref], actual[ref]
            exact(b, 'ref part' if field == 'bom' else 'ref part x_mm y_mm side rotation_deg', field+' row')
            if io.text(a['part'],'part') != io.text(b['part'],'part'):
                failures.append({'kind':'part_mismatch','table':field,'ref':ref})
            if field == 'bom': continue
            for row in (a,b):
                if row['side'] not in ('Top','Bottom'): raise ValueError('Unsupported board side')
                for axis in ('x_mm','y_mm','rotation_deg'): io.finite(row[axis], axis)
                if not 0 <= row['rotation_deg'] < 360: raise ValueError('Normalize angles to [0,360)')
            dx,dy = b['x_mm']-a['x_mm'],b['y_mm']-a['y_mm']
            angle = abs((b['rotation_deg']-a['rotation_deg']+180)%360-180)
            if a['side'] != b['side'] or (dx*dx+dy*dy)**.5 > pt or angle > at:
                failures.append({'kind':'pose_mismatch','table':field,'ref':ref,'dx_mm':dx,'dy_mm':dy,'angle_deg':angle})
    return failures


def states(expected, observed):
    exact(expected, 'modes exclusive_groups', 'state contract')
    exact(observed, 'modes', 'state observation')
    wanted = index(expected['modes'], 'name', 'expected modes')
    actual = index(observed['modes'], 'name', 'observed modes')
    groups = expected['exclusive_groups']
    if not isinstance(groups,list): raise ValueError('Exclusive groups must be a list')
    for group in groups:
        if not isinstance(group,list) or len(group)<2 or len(set(group))!=len(group):
            raise ValueError('Exclusive group needs unique signal names')
        for signal in group: io.text(signal,'signal')
    failures = []
    for name in sorted(set(wanted)|set(actual)):
        if name not in wanted or name not in actual:
            failures.append({'kind':'mode_coverage','mode':name}); continue
        for row in (wanted[name],actual[name]):
            exact(row,'name signals','mode')
            if not isinstance(row['signals'],dict) or not row['signals']: raise ValueError('Nonempty signals required')
            for key,value in row['signals'].items():
                io.text(key,'signal')
                if value not in ('0','1','Z','off','on'): raise ValueError('Unknown signal value')
        a,b = wanted[name]['signals'],actual[name]['signals']
        if a != b: failures.append({'kind':'state_mismatch','mode':name,'expected':a,'observed':b})
        for group in groups:
            if any(key not in a or key not in b for key in group): raise ValueError('Exclusive group signal not covered in every mode')
            for label, values in (('contract',a),('observation',b)):
                if sum(values[key] in ('1','on') for key in group)>1:
                    failures.append({'kind':'driver_contention','mode':name,'source':label,'signals':group})
    return failures


def variant(expected, observed):
    keys='variant_id generator_sha256 parameters output_roles'
    exact(expected,keys,'variant contract');exact(observed,keys,'variant observation')
    for row in (expected,observed):
        io.text(row['variant_id'],'selected variant')
        digest=row['generator_sha256']
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest): raise ValueError('Invalid generator digest')
        if not isinstance(row['parameters'],dict) or not row['parameters']: raise ValueError('Effective parameters required')
        roles=row['output_roles']
        if not isinstance(roles,list) or not roles or len(set(roles))!=len(roles): raise ValueError('Unique output roles required')
        for role in roles: io.text(role,'output role')
    return [{'kind':'inactive_variant_or_configuration','field':key} for key in keys.split() if io.encoded(expected[key])!=io.encoded(observed[key])]


def port(expected, observed):
    exact(expected,'donor allowed_changes','port contract')
    exact(observed,'target','port observation')
    before,after=expected['donor'],observed['target']
    for data in (before,after):
        if not isinstance(data,dict) or not data: raise ValueError('Complete scoped object map required')
        for key,value in data.items():
            io.text(key,'object identity')
            if value is None: raise ValueError('Null reserved for absent objects in change allowances')
    rules=index(expected['allowed_changes'],'object','allowed changes',allow_empty=True)
    for key,row in rules.items():
        exact(row,'object before after reason','change')
        io.text(row['reason'],'change reason')
        if io.encoded(row['before'])==io.encoded(row['after']): raise ValueError('No-op change allowance')
        if io.encoded(before.get(key))!=io.encoded(row['before']): raise ValueError('Allowance differs from donor')
    failures=[]
    for key in sorted(set(before)|set(after)|set(rules)):
        a,b=before.get(key),after.get(key)
        if key in rules:
            if io.encoded(b)!=io.encoded(rules[key]['after']): failures.append({'kind':'required_change_not_realized','object':key})
        elif io.encoded(a)!=io.encoded(b): failures.append({'kind':'unapproved_port_change','object':key})
    return failures


def release(expected, observed):
    exact(expected,'revision roles','release contract');exact(observed,'artifacts','release observation')
    io.text(expected['revision'],'release revision')
    roles=expected['roles']
    if not isinstance(roles,list) or not roles or any(not isinstance(r,str) or not r.strip() for r in roles) or len(set(roles))!=len(roles):
        raise ValueError('Unique required release roles needed')
    actual=index(observed['artifacts'],'role','release artifacts',allow_empty=True)
    failures=[]
    for role in sorted(set(roles)|set(actual)):
        if role not in actual or role not in roles: failures.append({'kind':'release_role_coverage','role':role});continue
        exact(actual[role],'role revision file','release artifact')
        if actual[role]['revision']!=expected['revision']: failures.append({'kind':'mixed_release_revision','role':role})
    return failures


CHECKERS={'assembly':assembly,'states':states,'variant':variant,'port':port,'release':release}


def evaluate(root, plan, baseline):
    exact(plan,'schema project_id baseline_id reviews','review plan')
    if type(plan['schema']) is not int or plan['schema']!=1 or plan['baseline_id']!=baseline: raise ValueError('Review schema/baseline mismatch')
    design=eb.design(root,baseline)
    if design['project_id']!=plan['project_id']: raise ValueError('Review project mismatch')
    reviews=index(plan['reviews'],'id','reviews');results=[]
    for ident,row in reviews.items():
        exact(row,'id kind contract observation evidence','review')
        if row['kind'] not in CHECKERS: raise ValueError('Unsupported review kind')
        if not isinstance(row['evidence'],list) or not row['evidence']: raise ValueError('Source evidence required')
        refs=[row['contract'],row['observation'],*row['evidence']]
        for ref in refs:
            eb.reference(root,ref)
            if ref not in design['inputs']: raise ValueError('Review input not in current design baseline')
        if row['contract']['path']==row['observation']['path']: raise ValueError('Expectation cannot be its own observation')
        expected=io.read(eb.reference(root,row['contract']));observed=io.read(eb.reference(root,row['observation']))
        if row['kind']=='variant' and expected.get('generator_sha256') not in {r['sha256'] for r in row['evidence']}:
            raise ValueError('Generator file must be bound as source evidence')
        failures=CHECKERS[row['kind']](expected,observed)
        if row['kind']=='release':
            for artifact in observed['artifacts']:
                ref=artifact['file'];eb.reference(root,ref)
                if ref not in design['inputs']: raise ValueError('Release artifact not in frozen baseline')
                refs.append(ref)
        results.append({'id':ident,'kind':row['kind'],'state':'BLOCKED' if failures else 'CHECK_OK','findings':failures,'inputs':refs})
    # Detect ordinary concurrent source changes before reporting success.
    if eb.design(root,baseline)!=design: raise ValueError('Design changed during review')
    return {'state':'BLOCKED' if any(r['state']=='BLOCKED' for r in results) else 'CHECK_OK',
            'project_id':plan['project_id'],'baseline_id':baseline,'plan_digest':io.digest(plan),'reviews':results,
            'scope':'declared sourced data only; no fresh EDA capture, physical fit, transient analysis or supplier visual approval'}


def check(root, name, baseline):
    path=eb.local(root,name)
    ref={'path':name,'sha256':io.file_hash(path)}
    if ref not in eb.design(root,baseline)['inputs']: raise ValueError('Review plan not frozen in current baseline')
    result=evaluate(root,io.read(path),baseline)
    eb.reference(root,ref)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--plan',required=True);p.add_argument('--baseline',required=True);a=p.parse_args()
    try:
        root=io.no_link(a.root).resolve(strict=True)
        result=check(root,a.plan,a.baseline)
        print(io.encoded(result).decode());return int(result['state']!='CHECK_OK')
    except (ValueError,TypeError,KeyError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
