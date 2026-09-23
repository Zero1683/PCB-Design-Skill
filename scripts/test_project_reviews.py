import copy,tempfile,unittest
from pathlib import Path
import project_reviews as pr
import workflow_io as io
import evidence_binding as eb
import local_checks as lc


def assembly_data():
    pose={'ref':'U1','part':'C123','x_mm':10,'y_mm':20,'side':'Top','rotation_deg':0}
    expected={'coordinate_frame':{'units':'mm','origin':'mounting datum','axes':'X-right/Y-down','angle_view':'assembly-side','rotation':'clockwise','bottom':'normalized'},
              'components':[{**pose,'fitted':True},{**pose,'ref':'R1','fitted':False}],
              'position_tolerance_mm':.02,'angle_tolerance_deg':.1}
    observed={'coordinate_frame':expected['coordinate_frame'],'bom':[{'ref':'U1','part':'C123'}],
              'submitted':[dict(pose)],'imported':[dict(pose)],'manual_browser_edits':False}
    return expected,observed


class ProjectReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
    def prepare(self,kind,a,b):
        io.save(self.root/'expected.json',a);io.save(self.root/'actual.json',b)
        (self.root/'source.txt').write_text('Captured synthetic raw data; test only')
        ref=lambda n:{'path':n,'sha256':io.file_hash(self.root/n)}
        self.plan={'schema':1,'project_id':'fixture','baseline_id':'A','reviews':[
            {'id':'review','kind':kind,'contract':ref('expected.json'),'observation':ref('actual.json'),'evidence':[ref('source.txt')]}]}
        io.save(self.root/'project-reviews.json',self.plan)
        io.save(self.root/'design-baseline.json',eb.snapshot(self.root,'fixture',['doc'],'A',
            ['expected.json','actual.json','source.txt','project-reviews.json']))
    def test_assembly_normal(self):self.assertEqual(pr.assembly(*assembly_data()),[])
    def test_assembly_rejects_reference_part_pose_and_browser_edits(self):
        for field,value in [('x_mm',11),('rotation_deg',180),('side','Bottom'),('part','C999')]:
            a,b=assembly_data();b['imported'][0][field]=value
            self.assertTrue(pr.assembly(a,b))
        a,b=assembly_data();b['bom']=[];self.assertTrue(pr.assembly(a,b))
        a,b=assembly_data();b['manual_browser_edits']=True;self.assertTrue(pr.assembly(a,b))
    def test_dnp_unexpected_duplicate_and_missing(self):
        for table in ('bom','submitted','imported'):
            a,b=assembly_data();b[table]=[];self.assertTrue(pr.assembly(a,b))
            a,b=assembly_data();b[table].append({**b[table][0],'ref':'R1'});self.assertTrue(pr.assembly(a,b))
            a,b=assembly_data();b[table].append(b[table][0].copy())
            with self.assertRaises(ValueError):pr.assembly(a,b)
    def test_units_nan_and_unbounded_tolerance_rejected(self):
        a,b=assembly_data();b['coordinate_frame']='inch'
        with self.assertRaises(ValueError):pr.assembly(a,b)
        a,b=assembly_data();a['coordinate_frame']['units']='inch'
        with self.assertRaises(ValueError):pr.assembly(a,b)
        a,b=assembly_data();b['imported'][0]['x_mm']=float('nan')
        with self.assertRaises(ValueError):pr.assembly(a,b)
        a,b=assembly_data();a['position_tolerance_mm']=100
        with self.assertRaises(ValueError):pr.assembly(a,b)
    def test_euclidean_position_tolerance(self):
        a,b=assembly_data();b['imported'][0]['x_mm']+=.019;b['imported'][0]['y_mm']+=.019
        self.assertTrue(pr.assembly(a,b))
    def test_state_expected_and_contention(self):
        a={'modes':[{'name':'boot','signals':{'cpu':'0','loader':'1'}}],'exclusive_groups':[['cpu','loader']]}
        b={'modes':copy.deepcopy(a['modes'])};self.assertEqual(pr.states(a,b),[])
        b['modes'][0]['signals']['cpu']='1';self.assertTrue(pr.states(a,b))
        a['modes'][0]['signals']['cpu']='1';self.assertTrue(pr.states(a,b))
    def test_state_mode_and_signal_coverage(self):
        a={'modes':[{'name':'boot','signals':{'a':'0','b':'0'}}],'exclusive_groups':[['a','b']]}
        b={'modes':[{'name':'run','signals':{'a':'0','b':'0'}}]};self.assertTrue(pr.states(a,b))
        b={'modes':[{'name':'boot','signals':{'a':'0'}}]}
        with self.assertRaises(ValueError):pr.states(a,b)
    def test_variant_wrong_selection_and_parameters(self):
        a={'variant_id':'B','generator_sha256':'a'*64,'parameters':{'length_mm':40},'output_roles':['pcb','schematic']}
        self.assertEqual(pr.variant(a,copy.deepcopy(a)),[])
        for field,value in [('variant_id','A'),('parameters',{'length_mm':41}),('generator_sha256','b'*64),('output_roles',['pcb'])]:
            b=copy.deepcopy(a);b[field]=value;self.assertTrue(pr.variant(a,b))
    def test_variant_requires_real_generator_evidence(self):
        a={'variant_id':'B','generator_sha256':'a'*64,'parameters':{'length_mm':40},'output_roles':['pcb']}
        self.prepare('variant',a,a)
        with self.assertRaises(ValueError):pr.check(self.root,'project-reviews.json','A')
    def test_type_sensitive_parameters_and_port_values(self):
        a={'variant_id':'B','generator_sha256':'a'*64,'parameters':{'enabled':1},'output_roles':['pcb']}
        b=copy.deepcopy(a);b['parameters']['enabled']=True;self.assertTrue(pr.variant(a,b))
        a={'donor':{'U1':{'pin_count':1}},'allowed_changes':[]}
        self.assertTrue(pr.port(a,{'target':{'U1':{'pin_count':True}}}))
        a['allowed_changes']=[{'object':'U1','before':{'pin_count':True},'after':{'pin_count':2},'reason':'test'}]
        with self.assertRaises(ValueError):pr.port(a,{'target':{'U1':{'pin_count':2}}})
    def test_release_roles_revisions_and_missing_files(self):
        a={'revision':'A','roles':['gerber']}
        b={'artifacts':[{'role':'gerber','revision':'A','file':{'path':'source.txt','sha256':'a'*64}}]}
        self.assertEqual(pr.release(a,b),[])
        b['artifacts'][0]['revision']='B';self.assertTrue(pr.release(a,b))
        self.assertTrue(pr.release(a,{'artifacts':[]}))
        b['artifacts'][0]['revision']='A';self.prepare('release',a,b)
        with self.assertRaises(ValueError):pr.check(self.root,'project-reviews.json','A')
    def test_release_bound_normal_then_file_drift(self):
        (self.root/'source.txt').write_text('Captured synthetic raw data; test only')
        b={'artifacts':[{'role':'gerber','revision':'A','file':{'path':'source.txt','sha256':io.file_hash(self.root/'source.txt')}}]}
        self.prepare('release',{'revision':'A','roles':['gerber']},b)
        self.assertEqual(pr.check(self.root,'project-reviews.json','A')['state'],'CHECK_OK')
        (self.root/'source.txt').write_text('different')
        with self.assertRaises(ValueError):pr.check(self.root,'project-reviews.json','A')
    def test_g5_invokes_present_reviews_and_blocks_failure(self):
        from test_evidence_fixture import prepare
        import check_evidence
        prepare(self.root)
        a,b=assembly_data();b['imported'][0]['side']='Bottom';self.prepare('assembly',a,b)
        report=check_evidence.audit(self.root,'A','G5',design_gates=True)
        self.assertEqual(report['project_reviews']['state'],'BLOCKED')
        self.assertIn('Applicable project reviews have unresolved findings',report['record_errors'])
    def test_port_change_whitelist_and_required_changes(self):
        a={'donor':{'connector':{'x':0},'width':30},'allowed_changes':[{'object':'width','before':30,'after':40,'reason':'accepted enclosure'}]}
        b={'target':{'connector':{'x':0},'width':40}};self.assertEqual(pr.port(a,b),[])
        b['target']['connector']['x']=1;self.assertTrue(pr.port(a,b))
        b={'target':{'connector':{'x':0},'width':30}};self.assertTrue(pr.port(a,b))
    def test_port_add_remove_and_no_null_objects(self):
        a={'donor':{'keep':1,'remove':2},'allowed_changes':[{'object':'remove','before':2,'after':None,'reason':'removed interface'},{'object':'add','before':None,'after':3,'reason':'new interface'}]}
        self.assertEqual(pr.port(a,{'target':{'keep':1,'add':3}}),[])
        with self.assertRaises(ValueError):pr.port(a,{'target':{'keep':None}})
    def test_bound_inputs_plan_and_stale_sources(self):
        self.prepare('assembly',*assembly_data());self.assertEqual(pr.check(self.root,'project-reviews.json','A')['state'],'CHECK_OK')
        (self.root/'source.txt').write_text('Changed capture')
        with self.assertRaises(ValueError):pr.check(self.root,'project-reviews.json','A')
    def test_wrong_project_and_self_observation_rejected(self):
        self.prepare('assembly',*assembly_data())
        self.plan['project_id']='other'
        with self.assertRaises(ValueError):pr.evaluate(self.root,self.plan,'A')
        self.plan['project_id']='fixture';self.plan['reviews'][0]['observation']=self.plan['reviews'][0]['contract']
        with self.assertRaises(ValueError):pr.evaluate(self.root,self.plan,'A')
    def test_local_runner_cache_and_bound_input_change(self):
        self.prepare('assembly',*assembly_data())
        batch={'schema':1,'jobs':[{'id':'review','kind':'project-reviews','inputs':['project-reviews.json'],'options':{'baseline':'A'}}]}
        self.assertEqual(lc.run(self.root,batch)['jobs'][0]['state'],'CHECK_OK')
        self.assertEqual(lc.run(self.root,batch)['cached_jobs'],1)
        (self.root/'source.txt').write_text('Changed source')
        result=lc.run(self.root,batch);self.assertEqual(result['cached_jobs'],0);self.assertEqual(result['jobs'][0]['state'],'ERROR')


if __name__=='__main__':unittest.main()
