#!/usr/bin/env python3
from __future__ import annotations
import argparse, gzip, http.cookiejar, json, os, subprocess, tempfile, time, urllib.parse, urllib.request
import uuid
from pathlib import Path
from datetime import datetime, timezone

THREAD="https://psfh.invalid/guestbook"
SITE="psfh"
MARKER="PSFH_RESTORE_GUARD_SYNTHETIC_MARK_20260918"
IMAGE="ghcr.io/umputun/remark42:v1.16.4@sha256:980e0e76a6f241cd181f44c5b4d686f0d8cd7f552e11deb3bdcba223b2c3b866"

def run(args, check=True):
    cp=subprocess.run(args,text=True,capture_output=True)
    if check and cp.returncode!=0:
        raise RuntimeError(f"command failed {args!r}\n{cp.stdout}\n{cp.stderr}")
    return cp

def req(opener,url,method="GET",payload=None,xsrf=None,basic=None):
    data=None if payload is None else json.dumps(payload).encode()
    headers={}
    if payload is not None: headers["Content-Type"]="application/json"
    if xsrf: headers["X-XSRF-TOKEN"]=xsrf
    r=urllib.request.Request(url,data=data,headers=headers,method=method)
    if basic:
        import base64
        token=base64.b64encode(f"{basic[0]}:{basic[1]}".encode()).decode()
        r.add_header("Authorization",f"Basic {token}")
    with opener.open(r,timeout=10) as resp:
        return resp.status, resp.read()

def find(opener,base):
    _,body=req(opener,f"{base}/api/v1/find?site={SITE}&url={urllib.parse.quote(THREAD,safe=':/')}&format=plain")
    return json.loads(body)

def contains(payload):
    return MARKER in json.dumps(payload,ensure_ascii=False)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--port",type=int,default=8084)
    args=ap.parse_args()
    base=f"http://127.0.0.1:{args.port}"
    # Never remove a fixed-name container that another invocation may own.
    container=f"psfh-remark42-restore-guard-{uuid.uuid4().hex}"
    result={"format":"psfh-remark42-restore-guard/0.1","owner_image":IMAGE,"real_person_data":False}
    with tempfile.TemporaryDirectory(prefix="psfh-r42-guard-") as td:
        os.chmod(td,0o777)
        try:
            run(["docker","run","-d","--name",container,"-p",f"127.0.0.1:{args.port}:8080",
                 "-v",f"{td}:/srv/var","-e",f"REMARK_URL={base}","-e",f"SITE={SITE}",
                 "-e","SECRET=psfh-restore-guard-secret-0123456789abcdef","-e","AUTH_ANON=true",
                 "-e","ADMIN_PASSWD=psfh-restore-guard-admin",IMAGE])
            for _ in range(30):
                try:
                    with urllib.request.urlopen(f"{base}/ping",timeout=2) as r:
                        if r.status==200: break
                except Exception: time.sleep(1)
            jar=http.cookiejar.CookieJar()
            opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            req(opener,f"{base}/auth/anonymous/login?user=restore_guard&aud={SITE}")
            xsrf=next(c.value for c in jar if c.name=="XSRF-TOKEN")
            status,body=req(opener,f"{base}/api/v1/comment?site={SITE}",method="POST",xsrf=xsrf,
                            payload={"text":MARKER,"locator":{"site":SITE,"url":THREAD}})
            if status!=201: raise RuntimeError(status)
            comment=json.loads(body); cid=comment["id"]
            run(["docker","exec","-e","REMARK_URL=http://127.0.0.1:8080",container,"backup","-s",SITE])
            backups=run(["docker","exec",container,"sh","-lc","find /srv/var/backup -maxdepth 1 -type f -name '*.gz' -print | sort"]).stdout.splitlines()
            backup=backups[-1]
            local=Path(td)/"pre-delete.gz"; run(["docker","cp",f"{container}:{backup}",str(local)])
            with gzip.open(local,"rb") as fh: result["pre_delete_backup_contains_marker"]=MARKER.encode() in fh.read()

            status,_=req(opener,f"{base}/api/v1/comment/{cid}?site={SITE}&url={urllib.parse.quote(THREAD,safe=':/')}",
                         method="PUT",xsrf=xsrf,payload={"text":"","summary":"accepted synthetic removal","delete":True})
            if status!=200: raise RuntimeError(f"initial delete {status}")
            result["current_after_accepted_removal_contains_marker"]=contains(find(opener,base))

            tombstone={
                "site":SITE,"url":THREAD,"comment_id":cid,
                "accepted_removal_at":datetime.now(timezone.utc).isoformat(),
                "receipt_id":"synthetic-removal-001"
            }
            tombstone_path=Path(td)/"removal-receipt.json"
            tombstone_path.write_text(json.dumps(tombstone,sort_keys=True),encoding="utf-8")
            result["removal_receipt_contains_removed_text"]=MARKER in tombstone_path.read_text(encoding="utf-8")

            run(["docker","exec","-e","REMARK_URL=http://127.0.0.1:8080",container,"restore","-f",Path(backup).name,"-s",SITE])
            time.sleep(.5)
            result["after_restore_before_replay_contains_marker"]=contains(find(opener,base))

            url=f"{base}/api/v1/admin/comment/{cid}?site={SITE}&url={urllib.parse.quote(THREAD,safe=':/')}"
            status,_=req(opener,url,method="DELETE",basic=("admin","psfh-restore-guard-admin"))
            result["replay_admin_delete_status"]=status
            time.sleep(.2)
            result["after_tombstone_replay_contains_marker"]=contains(find(opener,base))
            result["comment_id_survived_restore"]=cid in json.dumps(find(opener,base))
        finally:
            run(["docker","rm","-f",container],check=False)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
    ok=(result["pre_delete_backup_contains_marker"] is True
        and result["current_after_accepted_removal_contains_marker"] is False
        and result["removal_receipt_contains_removed_text"] is False
        and result["after_restore_before_replay_contains_marker"] is True
        and result["replay_admin_delete_status"]==200
        and result["after_tombstone_replay_contains_marker"] is False)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if ok else 1

if __name__=="__main__":
    raise SystemExit(main())
