import copy,tempfile,unittest
from pathlib import Path
import workflow_io as io
import mechanical_envelope as mech
import check_evidence
from test_evidence_fixture import prepare

class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);prepare(self.root)
    def obs(self):return io.read(self.root/'mechanical-observation.json')
    def save(self,obs):io.save(self.root/'mechanical-observation.json',obs)
    def test_original_matches(self):self.assertEqual(mech.evaluate(self.root,'A')['state'],'DIMENSIONS_MATCH')
    def test_translation_does_not_change_dimensions(self):
        data=self.obs();data.pop('outline');data['board_bounds_mm']=[-70,11,-20,41];self.save(data)
        self.assertEqual(mech.evaluate(self.root,'A')['state'],'DIMENSIONS_MATCH')
    def test_wrong_size_blocks_g3(self):
        data=self.obs();data.pop('outline');data['board_bounds_mm'][2]=55;self.save(data)
        self.assertEqual(mech.evaluate(self.root,'A')['violations'][0]['axis'],'board_length')
        self.assertFalse(check_evidence.audit(self.root,'A','G3',design_gates=True)['records_complete'])
    def test_height_maximum_accepts_shorter_rejects_taller(self):
        for height,state in [(10,'DIMENSIONS_MATCH'),(13,'DIMENSIONS_MISMATCH')]:
            data=self.obs();data['assembled_height_mm']=height;self.save(data)
            self.assertEqual(mech.evaluate(self.root,'A')['state'],state)
    def test_contract_cannot_relax_accepted_size(self):
        data=io.read(self.root/'mechanical-contract.json');data['expected_mm']['board_length']=55;io.save(self.root/'mechanical-contract.json',data)
        with self.assertRaises(ValueError):mech.evaluate(self.root,'A')
    def test_changed_plan_invalidates_contract(self):
        data=io.read(self.root/'intake.json');data['proposal']['assembly_envelope_mm']['board_length']=55
        data['decision']['proposal_digest']=io.digest(data['proposal']);io.save(self.root/'intake.json',data)
        with self.assertRaises(ValueError):mech.evaluate(self.root,'A')
    def test_unknown_height_units_project_and_coverage(self):
        original=self.obs()
        for key,value in [('assembled_height_mm',None),('units','mil'),('project_id','other'),('coverage','partial'),('assembled_height_mm',True)]:
            data=copy.deepcopy(original);data[key]=value;self.save(data)
            with self.assertRaises((TypeError,ValueError)):mech.evaluate(self.root,'A')
    def test_changed_source_not_accepted(self):
        (self.root/'native.json').write_text('{"changed":true}')
        with self.assertRaises(ValueError):mech.evaluate(self.root,'A')
    def test_maximum_policy_must_be_in_accepted_proposal(self):
        data=io.read(self.root/'intake.json');data['proposal']['dimension_policy']={k:'maximum' for k in mech.FIELDS}
        data['decision']['proposal_digest']=io.digest(data['proposal']);io.save(self.root/'intake.json',data)
        io.save(self.root/'mechanical-contract.json',mech.derive(self.root,'A'))
        obs=self.obs();obs.pop('outline');obs['board_bounds_mm']=[0,0,45,25];self.save(obs)
        self.assertEqual(mech.evaluate(self.root,'A')['state'],'DIMENSIONS_MATCH')
    def test_fake_report_cannot_override_real_outline(self):
        obs=self.obs();obs['board_bounds_mm']=[0,0,45,30];self.save(obs)
        with self.assertRaises(ValueError):mech.evaluate(self.root,'A',True)
    def test_g5_requires_outline(self):
        obs=self.obs();obs.pop('outline');self.save(obs)
        with self.assertRaises(ValueError):mech.evaluate(self.root,'A',True)
    def test_open_and_curved_outlines_fail_explicitly(self):
        for text in ['%MOMM*%\nG02X0Y0I1J0D01*\nM02*','%MOMM*%\nM02*']:
            p=self.root/'bad.GKO';p.write_text(text)
            with self.assertRaises(ValueError):mech.outline_bounds(p)
    def test_comment_mentioning_arc_is_not_an_arc(self):
        p=self.root/'outline.GKO';p.write_text('G04 this exporter also supports G02 arcs*\n'+p.read_text())
        self.assertEqual(mech.outline_bounds(p),[0,0,50,30])
    def test_incomplete_and_unsupported_outline_never_passes(self):
        p=self.root/'outline.GKO';valid=p.read_text()
        bad=[valid.replace('%MOMM*%',''),valid.replace('%FSLAX26Y26*%',''),
             valid.replace('M02*',''),valid.replace('M02*','X99Y99D01'),
             valid+'X99Y99D01*',valid.replace('X0Y0D02','G99X0Y0D02')]
        bad += [valid.replace('D10*',code+'*\nD10*') for code in ('G70','G91','G99')]
        for text in bad:
            with self.subTest(text=text):
                p.write_text(text)
                with self.assertRaises(ValueError):mech.outline_bounds(p)

if __name__=='__main__':unittest.main()
