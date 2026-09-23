"""Bind accepted envelope dimensions to observed board extents; not full mechanical acceptance."""
import argparse
from pathlib import Path
import workflow_io as io
import intake_review
import evidence_binding as eb
import importlib.util,re,sys

FIELDS=('board_length','board_width','assembled_height')
DEFAULT_POLICY={'board_length':'exact','board_width':'exact','assembled_height':'maximum'}

def derive(root, baseline):
    data=io.read(eb.local(root,'intake.json'))
    checked=intake_review.evaluate(root,data,baseline)
    if not checked['detailed_design_allowed']:raise ValueError('Accepted/delegated design plan required')
    policy=data['proposal'].get('dimension_policy',DEFAULT_POLICY)
    if not isinstance(policy,dict) or set(policy)!=set(FIELDS) or any(v not in ('exact','maximum') for v in policy.values()):
        raise ValueError('Dimension policy must explicitly cover all axes')
    return {'schema':1,'project_id':data['project_id'],'baseline_id':baseline,
            'intake_digest':io.digest(data),'expected_mm':data['proposal']['assembly_envelope_mm'],
            'policy':policy,'axes':'board_length=X, board_width=Y, assembled_height=total Z extent',
            'scope':'accepted envelope dimensions only; no mounting/cavity/antenna/pad acceptance'}

def outline_bounds(path):
    text=path.read_text('utf8')
    # Strict supported subset before the more permissive vendor tokenizer.
    tokens=[];pos=0
    for match in re.finditer(r'%[^%]*%|[^*%]*\*',text,re.S):
        if text[pos:match.start()].strip():raise ValueError('Unparsed outline content')
        tokens.append(match.group().strip());pos=match.end()
    if text[pos:].strip():raise ValueError('Truncated outline content')
    formats=units=0;ended=False
    for token in tokens:
        if ended:raise ValueError('Content after outline terminator')
        if token.startswith('%'):
            body=token[1:-1].strip()
            if not body.endswith('*'):raise ValueError('Unterminated outline parameter')
            for statement in body[:-1].split('*'):
                statement=statement.strip()
                if re.fullmatch(r'FSLAX[1-6][1-6]Y[1-6][1-6]',statement):formats+=1
                elif statement=='MOMM':units+=1
                elif re.fullmatch(r'ADD\d+C,[0-9]+(?:\.[0-9]+)?',statement):pass
                elif statement in ('LPD','IPPOS'):pass
                elif re.fullmatch(r'(?:TF|TA|TO|TD)[^*%]*',statement):pass
                else:raise ValueError('Unsupported outline parameter: '+statement)
        else:
            command=token[:-1].strip()
            if command.startswith('G04 '):continue
            if command=='M02':ended=True;continue
            if formats!=1 or units!=1:raise ValueError('Outline needs one explicit format and mm unit declaration')
            if not re.fullmatch(r'(?:G0?1)?(?:D[1-9][0-9]+|(?:X-?\d+)?(?:Y-?\d+)?D0?[12])|G0?1',command):
                raise ValueError('Unsupported outline command: '+command)
    if not ended or formats!=1 or units!=1:raise ValueError('Incomplete outline header or terminator')
    # Curved extents must not silently inherit a polygon approximation's bounds.
    commands=re.sub(r'G0?4[^*]*\*','',text,flags=re.I)
    if re.search(r'G0?[23](?=[^0-9]|$)',commands,re.I):raise ValueError('Curved outline needs independently verified exact extents')
    module_path=Path(__file__).resolve().parents[1]/'vendor/pcb-skill-toolkit/scripts/verify/outline_check.py'
    spec=importlib.util.spec_from_file_location('_pcb_envelope_outline',module_path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    points,closed,pens,bounds=module.outline_of(module.GB.parse_gerber(text))
    if not closed:raise ValueError('Outline is not closed')
    return list(bounds)

def evaluate(root, baseline, require_outline=False):
    contract=io.read(eb.local(root,'mechanical-contract.json'))
    expected=derive(root,baseline)
    if contract!=expected:raise ValueError('Mechanical contract differs from accepted intake; regenerate without changing intent')
    state=eb.design(root,baseline)
    observed=io.read(eb.local(root,'mechanical-observation.json'))
    if not isinstance(observed,dict) or type(observed.get('schema')) is not int or observed['schema']!=1:raise ValueError('Observation schema=1 required')
    if state['project_id']!=contract['project_id'] or observed.get('project_id')!=contract['project_id'] or observed.get('baseline_id')!=baseline:raise ValueError('Mechanical project/baseline mismatch')
    if observed.get('units')!='mm' or observed.get('coverage')!='complete':raise ValueError('Complete mm geometry required')
    source=observed.get('source');eb.reference(root,source)
    if source not in state['inputs']:raise ValueError('Observation source is not a current design input')
    bounds=observed.get('board_bounds_mm')
    if not isinstance(bounds,list) or len(bounds)!=4:raise ValueError('Board bounds [minX,minY,maxX,maxY] required')
    for value in bounds:io.finite(value,'board bound')
    if 'outline' in observed:
        outline=observed['outline'];path=eb.reference(root,outline)
        if outline not in state['inputs']:raise ValueError('Outline is not a current design input')
        measured=outline_bounds(path)
        if any(abs(a-b)>1e-6 for a,b in zip(bounds,measured)):raise ValueError('Declared bounds differ from parsed manufacturing outline')
        bounds=measured
    elif require_outline:raise ValueError('G5 envelope needs a bound manufacturing outline')
    actual={'board_length':bounds[2]-bounds[0],'board_width':bounds[3]-bounds[1],
            'assembled_height':io.finite(observed.get('assembled_height_mm'),'total assembly height')}
    if any(not io.finite(v,k)>0 for k,v in actual.items()):raise ValueError('Positive dimensions required')
    violations=[]
    for axis in FIELDS:
        a,b=actual[axis],contract['expected_mm'][axis]
        # Numeric representation allowance only, not a user-adjustable fabrication tolerance.
        ok=abs(a-b)<=1e-6 if contract['policy'][axis]=='exact' else a<=b+1e-6
        if not ok:violations.append({'axis':axis,'expected_mm':b,'actual_mm':a,'policy':contract['policy'][axis]})
    return {'state':'DIMENSIONS_MATCH' if not violations else 'DIMENSIONS_MISMATCH','baseline_id':baseline,
            'project_id':contract['project_id'],'actual_mm':actual,'violations':violations,
            'intake_digest':contract['intake_digest'],'observation_digest':io.digest(observed),
            'outline_measured':'outline' in observed,
            'scope':'envelope only; assembly height is a sourced observation, not a 3D collision test'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['derive','check']);p.add_argument('--root',type=Path,required=True);p.add_argument('--baseline',required=True)
    a=p.parse_args()
    try:
        root=io.no_link(a.root).resolve(strict=True)
        result=derive(root,a.baseline) if a.action=='derive' else evaluate(root,a.baseline)
        if a.action=='derive':io.save(root/'mechanical-contract.json',result)
        print(io.encoded(result).decode());return int(a.action=='check' and result['state']!='DIMENSIONS_MATCH')
    except (ValueError,TypeError,KeyError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
