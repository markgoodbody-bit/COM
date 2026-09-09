import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build


class ShelfTests(unittest.TestCase):
    def test_three_new_records(self):
        for work,_,_ in build.NEW:build.check_new(work)

    def reject_record_change(self, work, name, change):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/work
            shutil.copytree(build.PROPOSALS/work,dest)
            path=dest/name
            data=json.loads(path.read_text(encoding='utf-8'));change(data)
            path.write_text(json.dumps(data),encoding='utf-8')
            with patch.object(build,'PROPOSALS',Path(tmp)), self.assertRaises(ValueError):build.check_new(work)

    def test_reject_master(self):
        self.reject_record_change('atkins','artwork.json',lambda r:r.update(master_status='MASTER'))

    def test_reject_interpretation(self):
        self.reject_record_change('shen','artwork.json',lambda r:r.update(project_response='This proves TRACE'))

    def test_reject_artist_drift(self):
        self.reject_record_change('lewis','artwork.json',lambda r:r.update(creator='Anonymous'))

    def test_reject_duplicate_sculpture_view(self):
        self.reject_record_change('lewis','images.json',lambda r:r.__setitem__(1,r[0]))

    def test_reject_detached_copy(self):
        self.reject_record_change('atkins','images.json',lambda r:r[0]['variants'][0].update(parent_sha256='0'*64))

    def test_reject_false_dimensions(self):
        self.reject_record_change('shen','images.json',lambda r:r[0]['variants'][0].update(height=720))

    def test_expected_output_pages(self):
        inv=json.loads((build.OUT/'inventory.json').read_text())
        pages={k for k in inv if k.endswith('.html')}
        self.assertEqual(pages,{'works/index.html','works/harriet-powers/index.html','works/johannes-vermeer/index.html','works/anna-atkins/index.html','works/shen-zhou/index.html','works/edmonia-lewis/index.html'})
        powers=(build.OUT/'works/harriet-powers/index.html').read_text(encoding='utf-8')
        self.assertEqual(powers.count('<li>'),11)
        self.assertIn('Powers insisted',powers)
        self.assertNotIn('does not yet reproduce',powers)
        self.assertNotIn('index.html',inv)

    def test_exact_copied_outputs(self):
        inv=json.loads((build.OUT/'inventory.json').read_text())
        for route,pin in inv.items():
            data=(build.OUT/route).read_bytes()
            self.assertEqual(len(data),pin['bytes']);self.assertEqual(build.sha(data),pin['sha256'])

    def test_mobile_gutters_do_not_scale_with_text(self):
        for work in ['powers','vermeer']:
            self.assertIn('padding: 0 16px', (build.PROPOSALS/work/'work.css').read_text())


if __name__=='__main__':unittest.main()
