import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
def mod(name):
    s=importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
lab=mod('lab'); incident=mod('incident')

def cfg():
    c=json.loads((ROOT/'config/lab.example.yml').read_text()); c.update(box_version='20260101.0.0',network_reviewed=True,compatibility_reviewed=True); return c

class ConfigTests(unittest.TestCase):
    def test_example_blocks(self):
        with self.assertRaises(lab.Block): lab.config_validate(json.loads((ROOT/'config/lab.example.yml').read_text()))
    def test_valid_fixture(self): self.assertEqual(lab.config_validate(cfg())['name'],'sre-lab')
    def test_duplicate(self):
        c=cfg(); c['nodes']['worker-1']['ip']=c['nodes']['master-1']['ip']
        with self.assertRaises(lab.Block): lab.config_validate(c)
    def test_pool_overlap(self):
        c=cfg(); c['network']['pool_start']='192.168.57.11'
        with self.assertRaises(lab.Block): lab.config_validate(c)
    def test_cidr_overlap(self):
        c=cfg(); c['network']['services']=c['network']['pods']
        with self.assertRaises(lab.Block): lab.config_validate(c)
    def test_unknown_key(self):
        c=cfg(); c['foo']=42
        with self.assertRaises(lab.Block): lab.config_validate(c)
    def test_review_required(self):
        c=cfg(); c['network_reviewed']=False
        with self.assertRaises(lab.Block): lab.config_validate(c)
    def test_exit_priority(self):
        self.assertEqual(lab.exit_code([{'code':3},{'code':1},{'code':2}]),2)
        self.assertEqual(lab.exit_code([{'code':3},{'code':1}]),1)
        self.assertEqual(lab.exit_code([{'code':3}]),3)
        self.assertEqual(lab.exit_code([{'code':0}]),0)
    def test_vm_foreign(self):
        with patch.object(lab,'vbox_vms',return_value={'sre-lab-master-1':'abc'}),patch.object(lab,'vagrant_id',return_value=None):
            with self.assertRaises(lab.Block): lab.owned(cfg(),{'vms':{},'interfaces':[]})
    def test_state_hash(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(lab,'LOCAL',Path(tmp)):
            c=cfg(); lab.state(c,True); c['nodes']['master-1']['memory']=4096
            with self.assertRaises(lab.Block): lab.state(c)
    def test_cluster_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(lab,'LOCAL',Path(tmp)):
            c=cfg(); p=Path(tmp)/'sre-lab.kubeconfig';p.write_text('fake')
            with patch.object(lab,'state',return_value={'cluster':{'uid':'ours'}}),patch.object(lab,'owned'),patch.object(lab,'cluster_signature',return_value={'uid':'other'}):
                with self.assertRaises(lab.Block): lab.guard(c)
    def test_passive_never_active(self):
        with patch.object(lab,'check_one',return_value='fixture'),patch.object(lab,'active_tests') as active,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lab.audit(cfg(),['host']),0); active.assert_not_called()
    def test_failed_prevents_active(self):
        with patch.object(lab,'check_one',side_effect=lab.Health('fixture')),patch.object(lab,'active_tests') as active,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lab.audit(cfg(),['host'],active=True),1); active.assert_not_called()
    def test_direct_script_authorization(self):
        with patch.object(lab,'config',return_value=cfg()),patch.object(lab,'authorize',side_effect=lab.Block('denied')),patch.object(lab,'provision') as mut:
            with self.assertRaises(lab.Block): lab.main(['provision'])
            mut.assert_not_called()
    def test_invalid_flags(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as ctx: lab.parser().parse_args(['validate','--unknown'])
        self.assertEqual(ctx.exception.code,2)
    def test_inventory_groups(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(lab,'LOCAL',Path(tmp)),patch.object(lab,'ssh_config',return_value={'IdentityFile':'/test/private','Port':'2200'}):
            lab.generate_inventory(cfg(),'enp0s8'); inv=lab.load(Path(tmp)/'inventory/kubespray/hosts.yml'); vars_=lab.load(Path(tmp)/'inventory/kubespray/group_vars/all.yml'); ch=inv['all']['children']
            self.assertEqual(set(ch['etcd']['hosts']),set(lab.CP)); self.assertEqual(set(ch['kube_node']['hosts']),set(lab.NODES[3:])); self.assertEqual(vars_['kube_vip_services_enabled'],False); self.assertEqual(inv['all']['hosts']['master-1']['ansible_host'],cfg()['nodes']['master-1']['ip'])
    def test_bootstrap_guard_no_mutation(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(lab,'LOCAL',Path(tmp)):
            with self.assertRaises(lab.Block): lab.bootstrap_check()

class IncidentTests(unittest.TestCase):
    def test_catalog(self):
        cases=incident.all_cases(); self.assertEqual(len(cases),16)
        for c in cases:
            self.assertNotIn('solution',c); self.assertTrue(incident.get_case(c['id'])['solution'])
    def test_session_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(incident,'SESSIONS',Path(tmp)),contextlib.redirect_stdout(io.StringIO()) as out:
            c=incident.get_case('INC-001'); i=incident.start(c); self.assertNotIn(c['solution'],out.getvalue()); incident.main(['evidence','1']); incident.main(['diagnosis','configuração logs']); incident.main(['verify']); p,s=incident.get_session(i); self.assertTrue(s['evaluation']['complete']); self.assertFalse(s['revealed']); incident.main(['recover']); _,new=incident.get_session(); self.assertNotEqual(i,new['session']); self.assertTrue(p.exists()); self.assertFalse(new['revealed'])
    def test_traversal(self):
        with self.assertRaises(ValueError): incident.get_case('../anything')
    def test_solution_explicit(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(incident,'SESSIONS',Path(tmp)),contextlib.redirect_stdout(io.StringIO()) as out:
            c=incident.get_case('INC-005'); incident.start(c); incident.main(['solution']); _,s=incident.get_session(); self.assertTrue(s['revealed']); self.assertIn(c['solution'],out.getvalue())

if __name__=='__main__': unittest.main()
