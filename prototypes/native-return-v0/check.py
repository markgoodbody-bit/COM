"""Fixed read-only PSFH check. No queue, network, model, shell or execution grant."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

TASK = 'COM888-PSFH-RETURN-01'
SOURCE = '20af84afa73014d5809b587f0a892035725be4c5'
NAMES = ('llms.txt', 'challenge.html', 'index.html')

def read_file(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
            raise ValueError('not a bounded regular file')
        raw = os.read(fd, 65537)
        if len(raw) > 65536: raise ValueError('oversize')
        return raw
    finally:
        os.close(fd)

def inspect(root):
    if root.is_symlink() or (root/'fixtures').is_symlink():
        raise ValueError('symlink directory')
    pins=json.loads(read_file(root/'pins.json'))
    if set(pins)!=set(NAMES):raise ValueError('unexpected fixture inventory')
    texts={}; hashes={}
    for name in NAMES:
        raw=read_file(root/'fixtures'/name)
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=pins[name]['sha256'] or len(raw)!=pins[name]['bytes']:
            raise ValueError('fixture integrity mismatch')
        hashes[name]=digest;texts[name]=raw.decode('utf-8')
    entrance=texts['llms.txt'][:5000]
    checks={
      'html_fallback_within_first5000_characters':'https://pleasestartfromhere.com/explore/challenge.html' in entrance,
      'discussion_route_within_first5000_characters':'https://pleasestartfromhere.com/discussion/' in entrance,
      'local_draft_not_submission':'does not submit it' in entrance,
      'challenge_account_boundary':'needs a GitHub account' in texts['challenge.html'],
      'challenge_no_response_promise':'No response time is promised' in texts['challenge.html'],
      'challenge_discussion_link':'href="https://pleasestartfromhere.com/discussion/"' in texts['challenge.html'],
      'discussion_no_intake':'does not receive submissions' in texts['index.html'],
    }
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'fixture_sha256':hashes}

def main():
    root=Path(__file__).absolute().parent
    started=datetime.now(timezone.utc).isoformat()
    print(json.dumps({'event':'START','task_id':TASK,'guest_clock_utc':started,
                      'clock_authenticated':False,'authority':'EXTERNAL_OPERATOR_ONLY'}),flush=True)
    try:result=inspect(root)
    except (OSError,ValueError,KeyError,UnicodeError) as error:
        result={'status':'UNKNOWN','error_type':type(error).__name__}
    result.update(task_id=TASK,source_commit=SOURCE,
                  observed_at_utc=datetime.now(timezone.utc).isoformat(),
                  clock_authenticated=False,evidence_level='LOCAL_STATIC_SOURCE_CHECK',
                  model_invoked=False,execution_authority=False,
                  replay_prevention='NOT_IMPLEMENTED_EXTERNAL_OPERATOR_ONE_SHOT_REQUIRED')
    payload=json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    print(json.dumps({'event':'TERMINAL','result':result,
                      'result_sha256':hashlib.sha256(payload.encode()).hexdigest()},sort_keys=True),flush=True)
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
