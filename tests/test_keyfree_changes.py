"""Offline read-only cursor regressions; no real network or participant records."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import yac_voluntary_client as c
from test_yac_voluntary_client import FakeResponse,FakeOpener

class KeyfreeChanges(unittest.TestCase):
 def run_read(self,argv,opener):
  output=io.StringIO()
  with contextlib.redirect_stdout(output):code=c.main(argv,opener=opener)
  return code,json.loads(output.getvalue())
 def test_keyfree_page_ignores_private_state_and_preserves_cursor(self):
  op=FakeOpener((200,{'items':[],'next_since':17,'has_more':True}))
  with patch.object(c,'_private_path',side_effect=AssertionError('private path touched')),patch.object(c,'_save_state',side_effect=AssertionError('state written')):
   code,out=self.run_read(['--state','unused-private-path','changes','--since','12'],op)
  self.assertEqual(code,0);self.assertEqual(out['result']['next_since'],17)
  self.assertTrue(out['result']['has_more']);self.assertEqual(len(op.calls),1)
  call=op.calls[0];self.assertEqual(call['url'],c.BASE+'/api/changes?since=12')
  self.assertEqual(call['method'],'GET');self.assertIsNone(call['body'])
  self.assertFalse(any(k.lower() in ('authorization','x-yac-submission-key') for k in call['headers']))
 def test_zero_cursor_valid(self):
  op=FakeOpener((200,{'items':[],'next_since':0}))
  code,out=self.run_read(['changes','--since','0'],op)
  self.assertEqual(code,0);self.assertTrue(op.calls[0]['url'].endswith('since=0'))
 def test_invalid_cursor_refused_before_network(self):
  for cursor in ('-1',str(c.MAX_ID+1),'not-an-id'):
   op=FakeOpener()
   with self.subTest(cursor=cursor),contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as error:
    c.main(['changes','--since',cursor],opener=op)
   self.assertEqual(error.exception.code,2);self.assertEqual(op.calls,[])
 def test_timeout_unknown_once_no_private_state(self):
  class Timeout:
   calls=0
   def open(self,*a,**kw):self.calls+=1;raise TimeoutError()
  op=Timeout()
  with patch.object(c,'_private_path',side_effect=AssertionError('private path touched')):
   code,out=self.run_read(['changes','--since','3'],op)
  self.assertEqual(code,1);self.assertEqual(op.calls,1)
  self.assertEqual(out['result']['outcome'],'UNKNOWN')
 def test_no_flag_keeps_participant_state_requirement(self):
  op=FakeOpener()
  with patch.object(c,'_read_state',side_effect=c.ClientError('missing')),contextlib.redirect_stderr(io.StringIO()):
   self.assertEqual(c.main(['changes'],opener=op),2)
  self.assertEqual(op.calls,[])
if __name__=='__main__':unittest.main()
