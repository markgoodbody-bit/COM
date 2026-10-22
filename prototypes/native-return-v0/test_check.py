import hashlib,json,shutil,tempfile,unittest
from pathlib import Path
import check
class Checks(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)/'task'
  shutil.copytree(Path(__file__).parent,self.root,ignore=shutil.ignore_patterns('__pycache__'))
 def test_fixed_source(self):self.assertEqual(check.inspect(self.root)['status'],'PASS')
 def test_changed_bytes_refused(self):
  (self.root/'fixtures/llms.txt').write_text('unexpected')
  with self.assertRaises(ValueError):check.inspect(self.root)
 def test_symlink_refused(self):
  p=self.root/'fixtures/llms.txt';p.unlink();p.symlink_to('challenge.html')
  with self.assertRaises(OSError):check.inspect(self.root)
 def test_missing_fallback_fails_with_matching_hash(self):
  p=self.root/'fixtures/llms.txt';raw=p.read_bytes().replace(b'https://pleasestartfromhere.com/explore/challenge.html',b'https://pleasestartfromhere.com/explore/challenge.md')
  p.write_bytes(raw);pins=json.loads((self.root/'pins.json').read_text());pins['llms.txt'].update(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));(self.root/'pins.json').write_text(json.dumps(pins))
  self.assertEqual(check.inspect(self.root)['status'],'FAIL')
if __name__=='__main__':unittest.main(verbosity=2)
