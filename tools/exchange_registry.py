#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
SCHEMA_VERSION='exchange-artifact-registry-v0.2'
def now_utc(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def empty_registry(): return {'schema':SCHEMA_VERSION,'generation':0,'updated_at':now_utc(),'reconciliations':[],'artifacts':{}}
def load_registry(path):
    if not path.exists(): return empty_registry()
    d=json.loads(path.read_text(encoding='utf-8'))
    if d.get('schema')!=SCHEMA_VERSION: raise SystemExit(f"unsupported registry schema: {d.get('schema')!r}")
    if not isinstance(d.get('artifacts'),dict): raise SystemExit('invalid registry: artifacts must be an object')
    if not isinstance(d.get('generation',0),int): raise SystemExit('invalid registry: generation must be an integer')
    if not isinstance(d.get('reconciliations',[]),list): raise SystemExit('invalid registry: reconciliations must be an array')
    d.setdefault('generation',0); d.setdefault('reconciliations',[]); return d
@contextmanager
def registry_lock(path:Path)->Iterator[None]:
    path.parent.mkdir(parents=True,exist_ok=True); lp=path.with_suffix(path.suffix+'.lock')
    try: fd=os.open(lp,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError: raise SystemExit(f'registry is write-locked: {lp} (remove only after establishing no writer is active)')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(json.dumps({'pid':os.getpid(),'created_at':now_utc()})+'\n')
        yield
    finally:
        try: lp.unlink()
        except FileNotFoundError: pass
def save_registry(path,d):
    d['generation']=int(d.get('generation',0))+1; d['updated_at']=now_utc(); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8'); os.replace(tmp,path)
def sha256_file(path):
    h=hashlib.sha256(); total=0
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): total+=len(chunk); h.update(chunk)
    return h.hexdigest(),total
def req(d,i):
    try:return d['artifacts'][i]
    except KeyError:raise SystemExit(f'unknown artifact: {i}')
def latest_rec(d):
    r=d.get('reconciliations',[]); return r[-1] if r else None
def cmd_register(a):
    p=Path(a.registry)
    with registry_lock(p):
        d=load_registry(p)
        if a.id in d['artifacts']: raise SystemExit(f'artifact already exists: {a.id}; corrections require a new artifact identity plus supersession')
        hh,bb=a.sha256,a.bytes; src='DECLARED'
        if a.file:
            fh,fb=sha256_file(Path(a.file))
            if hh and hh.lower()!=fh: raise SystemExit('provided --sha256 disagrees with measured --file')
            if bb is not None and bb!=fb: raise SystemExit('provided --bytes disagrees with measured --file')
            hh,bb,src=fh,fb,'MEASURED'
        elif hh is None or bb is None: raise SystemExit('declared artifact identity requires both --sha256 and --bytes; use --file to measure instead')
        r={'artifact_id':a.id,'locator':a.locator,'sha256':hh.lower(),'bytes':bb,'identity_source':src,'publication_commit':a.commit,'created_by':a.created_by,'observed_at':a.observed_at or now_utc(),'supersedes':[],'superseded_by':[],'verification_witnesses':[],'review_target_hashes':sorted(set(h.lower() for h in (a.review_target_hash or [])))}
        d['artifacts'][a.id]=r; save_registry(p,d)
    print(json.dumps(r,indent=2,sort_keys=True)); return 0
def reachable(d,start,target):
    seen=set(); stack=[start]
    while stack:
        cur=stack.pop()
        if cur==target:return True
        if cur in seen:continue
        seen.add(cur); r=d['artifacts'].get(cur)
        if r:stack.extend(r.get('superseded_by',[]))
    return False
def fork_ancestors(d,i):
    forks=set(); seen=set(); stack=[i]
    while stack:
        cur=stack.pop()
        if cur in seen:continue
        seen.add(cur); r=d['artifacts'].get(cur)
        if not r:continue
        if len(r.get('superseded_by',[]))>1:forks.add(cur)
        stack.extend(r.get('supersedes',[]))
    return sorted(forks)
def cmd_supersede(a):
    p=Path(a.registry)
    with registry_lock(p):
        d=load_registry(p); old=req(d,a.old); new=req(d,a.new)
        if a.old==a.new:raise SystemExit('an artifact cannot supersede itself')
        if reachable(d,a.new,a.old):raise SystemExit('supersession would create a cycle')
        if a.new not in old['superseded_by']:old['superseded_by'].append(a.new);old['superseded_by'].sort()
        if a.old not in new['supersedes']:new['supersedes'].append(a.old);new['supersedes'].sort()
        save_registry(p,d)
    print(json.dumps({'old':old,'new':new},indent=2,sort_keys=True)); return 0
def cmd_reconcile(a):
    p=Path(a.registry); w={'observed_at':a.observed_at or now_utc(),'reconciled_against':a.against,'coverage':a.coverage,'method':a.method,'observer':a.observer,'evidence_ref':a.evidence_ref}
    with registry_lock(p):d=load_registry(p);d.setdefault('reconciliations',[]).append(w);save_registry(p,d)
    print(json.dumps(w,indent=2,sort_keys=True));return 0
def rt_summary(r):
    ws=[w for w in r.get('verification_witnesses',[]) if w.get('witness_kind')=='ROUND_TRIP_COPY']
    if not ws:return {'latest_result':'UNKNOWN','latest_observed_at':None,'validity':'NO_WITNESS'}
    x=ws[-1]; return {'latest_result':'TRUE' if x.get('match') else 'FALSE','latest_observed_at':x.get('observed_at'),'validity':'OBSERVED_AT_TIME_ONLY','witness_count':len(ws)}
def cmd_resolve(a):
    d=load_registry(Path(a.registry)); r=req(d,a.id); succ=r.get('superseded_by',[]); forks=fork_ancestors(d,a.id); rec=latest_rec(d)
    status='FORKED' if len(succ)>1 else ('SUPERSEDED' if succ else 'CURRENT_IN_REGISTRY')
    if a.historical: allowed,reason,rc=True,'explicit historical review',0
    elif status=='FORKED':allowed,reason,rc=False,'lineage forks at this artifact; choose an explicit successor/lineage',3
    elif status=='SUPERSEDED':allowed,reason,rc=False,'known-superseded object; name the successor or pass --historical',3
    elif rec is None and not a.allow_unreconciled:allowed,reason,rc=False,'no registry reconciliation witness; no-successor-recorded is not enough to establish a current review target',5
    else:allowed,reason,rc=True,('current in bounded registry with reconciliation witness' if rec else 'current in bounded registry; unreconciled use explicitly allowed'),0
    out={'registry_generation':d.get('generation',0),'registry_updated_at':d.get('updated_at'),'last_reconciliation':rec,'artifact':r,'status':status,'successors':succ,'fork_ancestors':forks,'round_trip':rt_summary(r),'review_allowed':allowed,'reason':reason}
    print(json.dumps(out,indent=2,sort_keys=True));return rc
def cmd_verify(a):
    p=Path(a.registry)
    def obs(d):
        r=req(d,a.id); mh,mb=sha256_file(Path(a.file)); eh,eb=r.get('sha256'),r.get('bytes'); match=(eh is not None and eh.lower()==mh and eb is not None and eb==mb)
        return r,{'artifact_id':a.id,'method':'local-file-sha256+bytes','source':str(Path(a.file)),'measured_sha256':mh,'measured_bytes':mb,'expected_sha256':eh,'expected_bytes':eb,'match':match,'observed_at':now_utc()}
    if a.record_witness:
        if a.witness_kind=='ROUND_TRIP_COPY' and not a.source_ref:
            raise SystemExit('--source-ref is required for ROUND_TRIP_COPY witnesses')
        with registry_lock(p):
            d=load_registry(p);r,o=obs(d);o['witness_kind']=a.witness_kind;o['source_ref']=a.source_ref;r.setdefault('verification_witnesses',[]).append(o);save_registry(p,d)
    else:
        d=load_registry(p);_,o=obs(d);o['witness_kind']=a.witness_kind;o['source_ref']=a.source_ref
    print(json.dumps(o,indent=2,sort_keys=True));return 0 if o['match'] else 4
def cmd_list(a):
    d=load_registry(Path(a.registry)); rec=latest_rec(d); cur=[]
    for r in d['artifacts'].values():
        if r.get('superseded_by'):continue
        forks=fork_ancestors(d,r['artifact_id']);cur.append({'artifact':r,'lineage_status':'CONTESTED_FORK' if forks else 'UNFORKED_IN_REGISTRY','fork_ancestors':forks,'round_trip':rt_summary(r)})
    cur.sort(key=lambda x:x['artifact']['artifact_id']); print(json.dumps({'registry_generation':d.get('generation',0),'registry_updated_at':d.get('updated_at'),'last_reconciliation':rec,'current':cur},indent=2,sort_keys=True));return 0
def parser():
    p=argparse.ArgumentParser();p.add_argument('--registry',default='exchange/artifacts.json');s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('register');q.add_argument('--id',required=True);q.add_argument('--locator');q.add_argument('--file');q.add_argument('--sha256');q.add_argument('--bytes',type=int);q.add_argument('--commit');q.add_argument('--created-by');q.add_argument('--observed-at');q.add_argument('--review-target-hash',action='append');q.set_defaults(func=cmd_register)
    q=s.add_parser('supersede');q.add_argument('--old',required=True);q.add_argument('--new',required=True);q.set_defaults(func=cmd_supersede)
    q=s.add_parser('reconcile');q.add_argument('--against',required=True);q.add_argument('--coverage',required=True);q.add_argument('--method',required=True);q.add_argument('--observer',required=True);q.add_argument('--evidence-ref');q.add_argument('--observed-at');q.set_defaults(func=cmd_reconcile)
    q=s.add_parser('resolve');q.add_argument('--id',required=True);q.add_argument('--historical',action='store_true');q.add_argument('--allow-unreconciled',action='store_true');q.set_defaults(func=cmd_resolve)
    q=s.add_parser('verify-file');q.add_argument('--id',required=True);q.add_argument('--file',required=True);q.add_argument('--record-witness',action='store_true');q.add_argument('--witness-kind',choices=['LOCAL_COPY','ROUND_TRIP_COPY'],default='LOCAL_COPY');q.add_argument('--source-ref');q.set_defaults(func=cmd_verify)
    q=s.add_parser('list-current');q.set_defaults(func=cmd_list)
    return p
def main():a=parser().parse_args();return a.func(a)
if __name__=='__main__':raise SystemExit(main())
