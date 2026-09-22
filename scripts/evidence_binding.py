"""Bind check observations to hashed on-disk design inputs. Does not inspect an unsaved EDA session."""
import argparse
from datetime import datetime
from pathlib import Path
import workflow_io as io
from report_provenance import identity


def local(root, name):
    io.text(name, 'local path')
    if Path(name).is_absolute() or '..' in Path(name).parts or ':' in name:
        raise ValueError('Expected project-relative file path')
    path = io.no_link(root / name)
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file() or path.stat().st_size == 0:
        raise ValueError('Missing or empty local file: ' + name)
    return path


def reference(root, ref):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}:
        raise ValueError('Expected path/sha256 reference')
    path = local(root, ref['path'])
    if io.file_hash(path) != ref['sha256']:
        raise ValueError('File changed: ' + ref['path'])
    return path


def snapshot(root, project, documents, baseline, paths):
    root = io.no_link(root).resolve(strict=True)
    io.text(project,'project ID');io.text(baseline,'baseline')
    if not documents or len(set(documents)) != len(documents):raise ValueError('Unique document IDs required')
    for doc in documents:io.text(doc,'document ID')
    if not paths or len(set(paths)) != len(paths):raise ValueError('Unique design input paths required')
    return {'schema':1,'project_id':project,'document_ids':documents,'baseline_id':baseline,
            'inputs':[{'path':name,'sha256':io.file_hash(local(root,name))} for name in paths]}


def design(root, baseline):
    root = io.no_link(root).resolve(strict=True)
    data = io.read(local(root,'design-baseline.json'))
    if not isinstance(data,dict) or data.get('schema')!=1 or data.get('baseline_id')!=baseline:
        raise ValueError('Design baseline mismatch')
    io.text(data.get('project_id'),'project ID')
    docs=data.get('document_ids')
    if not isinstance(docs,list) or not docs or any(not isinstance(d,str) or not d.strip() for d in docs) or len(set(docs))!=len(docs):
        raise ValueError('Unique native document IDs required')
    inputs=data.get('inputs')
    if not isinstance(inputs,list) or not inputs:raise ValueError('Design inputs required')
    names=set()
    for item in inputs:
        reference(root,item)
        if item['path'] in names:raise ValueError('Duplicate design input')
        names.add(item['path'])
    return data


def tool_digest(name):
    bundles={'check_connectivity.py':['check_connectivity.py','audit_design.py'],
             'audit_design.py':['audit_design.py'], 'component_cost.py':['component_cost.py','workflow_io.py'],
             'check_constraints.mjs':['check_constraints.mjs','design_constraints.mjs']}
    if name not in bundles:raise ValueError('Unsupported checker')
    files = bundles[name] + ([] if name.endswith('.mjs') else ['report_provenance.py', 'workflow_io.py'])
    return io.digest({n:io.file_hash(Path(__file__).parent/n) for n in files})


def machine_status(root, report, current=None, inputs=None):
    """Parse supported saved tool outputs, never shell/eval a caller-provided expression."""
    if not isinstance(report,dict):raise ValueError('Machine report must be an object')
    path=reference(root,report['output'])
    tool=report['tool']
    if not isinstance(tool,dict) or set(tool)!={'name','sha256'}:raise ValueError('Tool identity required')
    allowed={'check_connectivity.py','audit_design.py','component_cost.py','check_constraints.mjs'}
    if tool['name'] not in allowed:raise ValueError('Unsupported machine report; use documented manual review')
    script=Path(__file__).parent/tool['name']
    if tool_digest(tool['name'])!=tool['sha256']:raise ValueError('Checker version changed')
    output=io.read(path)
    if not isinstance(output,dict):raise ValueError('Machine report must be an object')
    name=tool['name']
    if current is None:
        saved = io.read(local(root, 'design-baseline.json'))
        current = design(root, saved.get('baseline_id'))
    identity(output, current)
    if inputs is None: inputs = current['inputs']
    by_hash = {}
    for entry in inputs:
        source_path = reference(root, entry)
        by_hash.setdefault(entry['sha256'], []).append(source_path)
    sources = output.get('source_inputs')
    roles = (['snapshot', 'contract'] if name == 'check_connectivity.py' else
             ['quote'] if name == 'component_cost.py' else
             ['snapshot', 'constraints'] if name == 'check_constraints.mjs' else
             ['left', 'right'] if output.get('scope') == 'normalized-record-comparison' else ['snapshot'])
    if not isinstance(sources, list) or len(sources) != len(roles):
        raise ValueError('Report must identify every actual checker input; rerun legacy reports')
    primary = {'left', 'right', 'snapshot', 'quote'}
    design_hashes = {entry['sha256'] for entry in current['inputs']}
    for entry, role in zip(sources, roles):
        if not isinstance(entry, dict) or set(entry) != {'role', 'sha256'} or entry['role'] != role or not isinstance(entry['sha256'], str):
            raise ValueError('Invalid report input provenance')
        digest = entry['sha256']
        if digest not in by_hash or (role in primary and digest not in design_hashes):
            raise ValueError('Report source does not match current bound design inputs')
        identity(io.read(by_hash[digest][0]), current)
    if name=='check_connectivity.py':
        if output.get('scope')!='declared-pin-net-expectations-only' or not output.get('rules'):raise ValueError('Wrong connectivity report')
        if not isinstance(output['rules'],list) or any(not isinstance(v,dict) for v in output['rules']):raise ValueError('Invalid connectivity rules')
        valid=output.get('expectations_match') is True and all(v.get('status')=='PASS' for v in output['rules'])
    elif name=='audit_design.py':
        if output.get('scope')=='normalized-record-comparison':valid=output.get('records_match') is True and output.get('differences')==[]
        elif output.get('scope')=='conservative-body-envelope-screen-only':valid=output.get('suspect_pairs')==[] and output.get('missing_geometry')==[] and type(output.get('checked_components')) is int and output['checked_components']>0
        else:raise ValueError('Unsupported design report scope')
    elif name=='component_cost.py':
        if not isinstance(output.get('rows'),list) or not output['rows']:raise ValueError('Empty component quote report')
        valid=output.get('status')=='COMPLETE_QUOTE' and output.get('issues')==[] and all(isinstance(row,dict) and row.get('status')=='QUOTED' for row in output['rows'])
    else:
        # CLI includes an envelope; inspect the evaluator report under result.
        value=output.get('result',output)
        if not isinstance(value,dict) or type(value.get('checked')) is not int:raise ValueError('Invalid constraint result')
        valid=value.get('state')=='PASS' and value.get('violations')==[] and value.get('checked',0)>0
    return 'PASS' if valid else 'FAIL'


def evaluate(root, baseline, rows, through):
    root=io.no_link(root).resolve(strict=True)
    current=design(root,baseline)
    data=io.read(local(root,'check-bindings.json'))
    if not isinstance(data,dict) or data.get('schema')!=1 or data.get('project_id')!=current['project_id'] or data.get('baseline_id')!=baseline:
        raise ValueError('Check binding identity mismatch')
    bindings=data.get('checks')
    if not isinstance(bindings,list):raise ValueError('Check bindings must be a list')
    by_id={}
    for b in bindings:
        if not isinstance(b,dict):raise ValueError('Binding must be an object')
        ident=io.text(b.get('id'),'binding ID')
        if ident in by_id:raise ValueError('Duplicate binding ID')
        by_id[ident]=b
    current_digest=io.digest(current)
    modes={}
    for row in rows:
        if row.get('stage') not in {f'G{i}' for i in range(int(through[1:])+1)} or row.get('status') not in ('PASS','N_A'):continue
        ident=row['id'];b=by_id.get(ident)
        if row.get('baseline_id')!=baseline:raise ValueError('CSV baseline mismatch: '+ident)
        if b is None:raise ValueError('Missing design binding: '+ident)
        if b.get('design_digest')!=current_digest:raise ValueError('Stale design binding: '+ident)
        for key, expected in (('project_id', current['project_id']), ('baseline_id', baseline)):
            if key in b and b[key] != expected: raise ValueError('Binding identity mismatch: '+ident)
        if b.get('status')!=row['status']:raise ValueError('CSV/binding outcome mismatch: '+ident)
        stamp=datetime.fromisoformat(io.text(b.get('checked_at'),'checked_at').replace('Z','+00:00'))
        if stamp.tzinfo is None:raise ValueError('Binding timestamp needs timezone')
        io.text(b.get('method'),'method')
        inputs=b.get('inputs');evidence=b.get('evidence')
        if not isinstance(inputs,list) or not inputs or not isinstance(evidence,list) or not evidence:
            raise ValueError('Bound inputs and evidence required: '+ident)
        for entry in inputs+evidence:reference(root,entry)
        names={entry['path'] for entry in evidence}
        csv_names={name.strip() for name in row['evidence_path'].split(';') if name.strip()}
        if names!=csv_names:raise ValueError('CSV/binding evidence mismatch: '+ident)
        mode=b.get('mode');modes[ident]=mode
        if mode=='machine':
            report=b.get('report')
            if not isinstance(report,dict) or report.get('output') not in evidence:raise ValueError('Report must be bound evidence')
            if ident in {v['id'] for v in io.read(Path(__file__).resolve().parents[1]/'assets/design-check-registry.json')['checks']}:raise ValueError('Builtin gates require composite review; use subordinate machine check IDs')
            if machine_status(root,report,current,inputs)!=b['status']:raise ValueError('Machine output contradicts status: '+ident)
        elif mode=='manual':
            for key in ('reviewer','finding','basis'):io.text(b.get(key),key)
        else:raise ValueError('Use explicit machine or manual review mode')
    return {'state':'BOUND_TO_CURRENT_FILES','project_id':current['project_id'],'design_digest':current_digest,
            'checks':modes,'scope':'on-disk provenance and supported report outcomes; execution authenticity and unsaved EDA state not assessed'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--project',required=True);p.add_argument('--baseline',required=True)
    p.add_argument('--document',action='append',required=True);p.add_argument('--input',action='append',required=True)
    a=p.parse_args()
    try:
        data=snapshot(a.root,a.project,a.document,a.baseline,a.input)
        io.save(a.root/'design-baseline.json',data,exclusive=True)
        print('Created design-baseline.json; check bindings must come from actual observations.')
    except (ValueError,KeyError,TypeError,OSError) as exc:p.exit(2,'ERROR: '+str(exc)+'\n')
if __name__=='__main__':raise SystemExit(main())
