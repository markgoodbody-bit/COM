#!/usr/bin/env python3
"""Build an evidence-bound three-condition ATRS reader-use method pack.

Method only: no recruitment, participant data, scoring execution, or reader
benefit result. Conditions are generated locally from the same frozen source.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SEED = 20260917
CONDITIONS = ("FULL", "EXCERPT", "LENS")

TASKS = [
    "Using only the published Appeals and review field, what action, if any, does the field say someone can take next for review, challenge, correction, complaint, clarification, or help?",
    "Who does that field say can take the step? Preserve the stated role/scope.",
    "How can the step be initiated or reached? If no initiation route/channel is stated in that field, answer NOT STATED.",
    "What is the action about: tool output, broader decision/process, data use, general service/help, explanation/justification, or something else?",
    "Does the field describe the process/action as operating now, unavailable/no separate process, planned/not operating, or unclear?",
    "Identify the exact field sentence(s) supporting your answer.",
]

CASES: list[dict[str, Any]] = [
    {"case_id":"hra-proportionate-review","title":"Health Research Authority: Proportionate Review Toolkit","source_sha256":"5444c3a33252d980ce241070b82c688cc1ab8a556e43620e89dbd1a47655ac1b","appeals_text_sha256":"314c681768aad37f714328b7dd7fe5ed8b698f88f79c13b1a4c0f7d647f51581","primary_scored":True,"key":{"next_step":["submit a query about the tool outcome to HRA","contact HRA for further advice"],"actor":["user"],"channel":["queries@hra.nhs.uk"],"object_layer":["tool outcome","answering / tool-use guidance"],"status":["operating/current"],"limits":["review by a senior advisor is described; no statutory appeal right is inferred"]}},
    {"case_id":"nhsbsa-residency","title":"NHS BSA: Residency Checker for UK EHIC/GHIC/PRC/S2","source_sha256":"09bf1f39a852befdd89e5a89eed4ce46154b53b54d5ef112599f13dd3bdd9371","appeals_text_sha256":"a2fbc6269da87f18b80b72b2676416b48961dd372df791a25a23a78039b923ba","primary_scored":True,"key":{"next_step":["provide documentary evidence of residency","use the complaints process"],"actor":["customer"],"channel":["documentary evidence process","published complaints-policy URL"],"object_layer":["residency/application process"],"status":["operating/current"],"limits":["no entitlement or successful reversal is promised"]}},
    {"case_id":"ukho-tidal","title":"UKHO: Tidal Harmonic Analysis and Prediction","source_sha256":"26c162dc448de2e1025185b8352ed434af57f7a515f318de8b8f7a8c46899c0e","appeals_text_sha256":"62c42010a360985e43657dd512339b75d78f5698015a4d01cf5865d19f62485d","primary_scored":True,"key":{"next_step":["send user feedback through UKHO Customer Services"],"actor":["user"],"channel":["https://www.admiralty.co.uk/contact-us","UKHO Customer Services"],"object_layer":["tidal products/services feedback"],"status":["no formal appeal; feedback route operating/current"],"limits":["general feedback is not a formal appeal"]}},
    {"case_id":"nsi-polyai","title":"NS&I: PolyAI","source_sha256":"f677262e8da43fcee4360eef421eb72346199bdb37a02e5be7a60ad0ce855e8f","appeals_text_sha256":"22277dc7b924bfd78b011464debd1cca31d4980af25ebcee451567af87c18af9","primary_scored":True,"key":{"next_step":["request a human agent","use other NS&I contact channels","use the standard complaints process and escalation"],"actor":["customer"],"channel":["in-channel human-agent request","other NS&I contact channels","complaints/escalation process referenced without a locator in this field"],"object_layer":["response/help","broader complaint/escalation"],"status":["no formal appeal for PolyAI; other help/complaints routes described as current"],"limits":["no complaints-process locator appears in this field"]}},
    {"case_id":"qcovid","title":"Department for Health and Social Care and NHS Digital: QCovid algorithm","source_sha256":"b735c1e05831a9f9c2bb37822b312d6041a5e96ee6b3386c96f2a7b57de08783","appeals_text_sha256":"529319f6dff7610f07c83dd89e7f8ff0891a2e1827081e9ed9adec6301b98532","primary_scored":True,"key":{"next_step":["review the result with a clinician","refer to guidance pages for further clarification"],"actor":["patient"],"channel":["clinician","guidance pages"],"object_layer":["QCovid result / clarification"],"status":["review/clarification described as current"],"limits":["no formal appeal process is stated in this field"]}},
    {"case_id":"wilton-data-cleaning","title":"Wilton Park: Data Cleaning Tool","source_sha256":"6b43dcfe84152efb1da3bca5f61492cadc2eace5226234b549a365c19cb6a273","appeals_text_sha256":"fda19b2bb26f709c3b0b7d084c1c57d9c9c9465c992ddbc8ef634f60f37e28d4","primary_scored":True,"key":{"next_step":["request removal/deletion of personal data"],"actor":["individual","customer"],"channel":["dataprotectionofficer@wiltonpark.org.uk","privacy policy"],"object_layer":["data use/data rights"],"status":["operating/current data-removal route"],"limits":["relevance to reconsideration of a tool output is not established"]}},
    {"case_id":"cabinet-document-review","title":"Cabinet Office: Automated Digital Document Review","source_sha256":"f6cdd458d9e0e09701540b40f428a5423b636622948b48a90c1743d7f1ee0bf7","appeals_text_sha256":"ea13ffc50581153db63b80a931d07f2b04c97cf95f70a3c04f9368c5f458f330","primary_scored":True,"key":{"next_step":["request/receive justification in an appeal or FOI context"],"actor":["NOT STATED","UNCLEAR"],"channel":["NOT STATED","UNCLEAR"],"object_layer":["explanation/justification for deletion; not recovery of deleted file"],"status":["recovery/reversal unavailable after hard deletion; justification evidence retained"],"limits":["later explanation does not restore deleted material"]}},
    {"case_id":"darat","title":"Hampshire and Thames Valley Police: DARAT","source_sha256":"9b8c999ef1ab061673350ff191fa48230267698ee4661e8006af9a375c41dc09","appeals_text_sha256":"ad56e92b8738e2440d1cc61aaa3f26e997a82cf86130b1081b86ad54a60056fd","primary_scored":True,"key":{"next_step":["NOT STATED","UNCLEAR"],"actor":["NOT STATED","UNCLEAR"],"channel":["NOT STATED","UNCLEAR"],"object_layer":["review/appeal process not yet defined in the field"],"status":["planned/not operating; described as part of ethical review"],"limits":["future intention is not an operating route"]}},
    {"case_id":"national-highways-webchat","title":"National Highways: Highways Webchat","source_sha256":"cd2918b10c314ca4714822ef6351e76938d09acd40ba3c4bc12766e1b4f86d5f","appeals_text_sha256":"ca00f53b958810aad720c7aba9ccfb74023fada0eb7b2765381ffa498986c161","primary_scored":True,"key":{"next_step":["contact National Highways about an incorrect answer, concern or complaint"],"actor":["user"],"channel":["https://nationalhighways.co.uk/help-centre/","contact details in explainability statement"],"object_layer":["incorrect webchat answer / concern about operation"],"status":["operating/current"],"limits":["contact route does not by itself establish a formal appeal right"]}},
    {"case_id":"dbt-find-exporters","title":"DBT: Find Exporters","source_sha256":"4d3df859dd4dac508cf052c3da2e10ba6185f5d9c7e7ba4e2287a3f47103b0d2","appeals_text_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","primary_scored":False,"key":{"next_step":["NOT STATED"],"actor":["NOT STATED"],"channel":["NOT STATED"],"object_layer":["NOT STATED"],"status":["Appeals and review field not observed in frozen record"],"limits":["missing field is not evidence that no route or practice exists elsewhere"]}},
]


def load_audit_core():
    spec = importlib.util.spec_from_file_location("reader_use_audit_core", ROOT / "audit_core.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load audit_core.py")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def appeals_text(row: dict[str, Any]) -> str:
    return " || ".join(str(m.get("text", "")) for m in row.get("fields", {}).get("appeals_review", {}).get("matches", []))


def case_rules(values: list[str]) -> dict[str, Any]:
    return {
        "accepted_alternatives": [v for v in values if v not in {"NOT STATED", "UNCLEAR"}],
        "jointly_required": [],
        "accepted_not_stated": "NOT STATED" in values,
        "accepted_unclear": "UNCLEAR" in values,
        "one_faithful_alternative_is_sufficient": True,
    }


def validate(report: dict[str, Any], html_dir: Path):
    by_title = {str(r.get("title")): r for r in report.get("records", [])}
    selected = []
    for case in CASES:
        row = by_title.get(case["title"])
        if row is None: raise ValueError(f"missing frozen case: {case['title']}")
        if row.get("source_sha256") != case["source_sha256"]: raise ValueError(f"source identity mismatch: {case['case_id']}")
        if sha256_bytes(appeals_text(row).encode()) != case["appeals_text_sha256"]: raise ValueError(f"appeals evidence mismatch: {case['case_id']}")
        source_name = row.get("source_snapshot") or f"{case['source_sha256']}.html"
        raw = (html_dir / source_name).read_bytes()
        if sha256_bytes(raw) != case["source_sha256"]: raise ValueError(f"raw HTML identity mismatch: {case['case_id']}")
        selected.append((case, row, raw))
    return selected


STYLE = "body{font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:900px;margin:0 auto;padding:24px;color:#171717;background:#fff}h1{font-size:1.35rem}h2{font-size:1.05rem;margin-top:1.4rem}.note{color:#5d5d5d;font-size:.9rem}.source{white-space:pre-wrap;line-height:1.55;border-left:3px solid #aaa;padding-left:.8rem}.token-list{padding-left:1.3rem}.record-section{margin:1.15rem 0;padding-bottom:.8rem;border-bottom:1px solid #ddd}code{overflow-wrap:anywhere}"


def page_shell(title: str, body: str) -> bytes:
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>ATRS record task</title><style>{STYLE}</style></head><body><h1>{esc(title)}</h1><p class='note'>Study surface. Answer only from the published <strong>Appeals and review</strong> field. Outbound navigation is not part of this timed task.</p>{body}</body></html>".encode()


def full_surface(case, row, raw):
    core = load_audit_core(); sections = core.parse_sections(core.decode_page(raw)); blocks=[]
    for section in sections:
        body=f"<h2>{esc(section.heading)}</h2><p class='source'>{esc(section.text)}</p>"
        if section.hrefs: body += "<p class='note'>Published link destinations: " + "; ".join(f"<code>{esc(x)}</code>" for x in section.hrefs) + "</p>"
        blocks.append(f"<section class='record-section'>{body}</section>")
    return page_shell(case["title"], "".join(blocks))


def field_tokens(row):
    out=[]; seen=set()
    for match in row.get("fields",{}).get("appeals_review",{}).get("matches",[]):
        tokens=match.get("contact_tokens",{})
        for kind,key in (("link","hrefs"),("url","urls_in_text"),("email","emails"),("phone-like","phones")):
            for raw in tokens.get(key,[]) or []:
                item=(kind,str(raw).strip())
                if item[1] and item not in seen: seen.add(item); out.append(item)
    return out


def excerpt_surface(case,row):
    field=row.get("fields",{}).get("appeals_review",{}); text=appeals_text(row)
    if not field.get("section_present"):
        body="<h2>Appeals and review</h2><p class='source'>FIELD NOT OBSERVED IN FROZEN PAGE</p>"
    else:
        body=f"<h2>Appeals and review</h2><p class='source'>{esc(text)}</p>"; toks=field_tokens(row)
        if toks: body += "<p class='note'>Published link/contact text: " + "; ".join(f"<code>{esc(v)}</code>" for _,v in toks) + "</p>"
    return page_shell(case["title"],body)


def lens_surface(case,row):
    field=row.get("fields",{}).get("appeals_review",{}); text=appeals_text(row)
    if not field.get("section_present"):
        body="<h2>Published Appeals and review field</h2><p class='source'>FIELD NOT OBSERVED IN FROZEN PAGE</p>"
    else:
        body=f"<h2>Published Appeals and review passage</h2><p class='source'>{esc(text)}</p><h2>Published link and contact-like evidence in that passage</h2>"; toks=field_tokens(row)
        if toks: body += "<ul class='token-list'>"+"".join(f"<li><strong>{esc(k)}</strong>: <code>{esc(v)}</code></li>" for k,v in toks)+"</ul>"
        else: body += "<p class='note'>No link, URL, email or phone-like token was observed in this field. This does not mean no route exists.</p>"
        body += "<p class='note'>Token grouping is deterministic presentation of the same published field evidence; it is not an appeal-right or route-effectiveness classification.</p>"
    return page_shell(case["title"],body)


def write_surface(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(payload); return sha256_bytes(payload)


def build_schedules(scored_cases):
    schedules=[]
    for seq in range(6):
        rotation=seq%3; assignments={c["case_id"]:CONDITIONS[(i+rotation)%3] for i,c in enumerate(scored_cases)}
        order=[c["case_id"] for c in scored_cases]; random.Random(SEED+seq).shuffle(order)
        schedules.append({"sequence_id":f"S{seq+1}","seed":SEED+seq,"cases":[{"position":p,"case_id":cid,"condition":assignments[cid]} for p,cid in enumerate(order,1)]})
    return schedules


def build(report,html_dir,out_dir):
    validated=validate(report,html_dir); participant_dir=out_dir/"participant_pack"; private_dir=out_dir/"private_key"; surface_manifest={}; key_cases=[]; scored=[]; sentinel=None
    for case,row,raw in validated:
        payloads={"FULL":full_surface(case,row,raw),"EXCERPT":excerpt_surface(case,row),"LENS":lens_surface(case,row)}; targets={}
        for condition,payload in payloads.items():
            rel=Path("surfaces")/case["case_id"]/f"{condition.lower()}.html"; digest=write_surface(participant_dir/rel,payload); targets[condition]={"path":str(rel).replace('\\','/'),"sha256":digest,"bytes":len(payload)}
        surface_manifest[case["case_id"]]={"title":case["title"],"source_sha256":case["source_sha256"],"appeals_text_sha256":case["appeals_text_sha256"],"targets":targets}
        rules={k:case_rules(v) for k,v in case["key"].items() if k!="limits"}
        key_cases.append({"case_id":case["case_id"],"title":case["title"],"primary_scored":case["primary_scored"],"published_appeals_text":appeals_text(row),"component_rules":rules,"limits":case["key"]["limits"],"evidence_rule":"quoted/identified field wording must support the chosen answer; missing-field sentinel is not in the primary score"})
        if case["primary_scored"]: scored.append(case)
        else: sentinel={"case_id":case["case_id"],"status":"NON_SCORED_FIELD_ABSENCE_SENTINEL","targets":targets}
    schedules=build_schedules(scored); exposure={c["case_id"]:{x:0 for x in CONDITIONS} for c in scored}
    for s in schedules:
        for item in s["cases"]: exposure[item["case_id"]][item["condition"]]+=1
    if any(n!=2 for counts in exposure.values() for n in counts.values()): raise ValueError(f"condition imbalance: {exposure}")
    manifest={"status":"REPAIRED_METHOD_PACK_NO_PARTICIPANT_RESULT","study_scope":"PUBLISHED_APPEALS_AND_REVIEW_FIELD_ONLY","conditions":{"FULL":"all frozen main-section text; participant must locate Appeals and review field","EXCERPT":"same Appeals field evidence in a plain isolated excerpt","LENS":"same Appeals field evidence with deterministic token grouping"},"primary_contrasts":{"FULL_vs_EXCERPT":"field-location/scoping cost","EXCERPT_vs_LENS":"added value of structured presentation","FULL_vs_LENS":"combined descriptive contrast"},"tasks":TASKS,"randomisation_seed_base":SEED,"schedules":schedules,"surface_manifest":surface_manifest,"non_scored_sentinel":sentinel,"timing":{"network":"offline/local targets only","initial_scroll":0,"outbound_navigation":"disabled/not part of timed task","timer_start":"case target rendered and participant starts case","timer_stop":"response submitted","log":["sequence","case","condition","position","completion_status","elapsed_ms"]},"ceilings":["METHOD_PACK != HUMAN_RESULT","PROMPTED_FIELD_RETRIEVAL != UNSOLICITED_COMPREHENSION","TEN_PURPOSIVE_CASES != WHOLE_ATRS_REGISTER","ANSWER_KEY != OFFICIAL_INTERPRETATION","NO_HUMAN_DATA_COLLECTED"]}
    key={"status":"PRIVATE_PROVISIONAL_KEY_REQUIRES_INDEPENDENT_ADJUDICATION_BEFORE_HUMAN_RUN","scored_cases":9,"points_per_scored_case":6,"components":["next_step","actor","channel","object_layer","status","evidence"],"multiple_route_rule":"one faithful accepted alternative is sufficient unless jointly_required is non-empty","unsupported_inference_errors":"count separately; do not net against retrieval score","cases":key_cases}
    participant_dir.mkdir(parents=True,exist_ok=True); private_dir.mkdir(parents=True,exist_ok=True)
    (participant_dir/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
    (participant_dir/"TASKS.txt").write_text("\n\n".join(f"{i+1}. {q}" for i,q in enumerate(TASKS))+"\n")
    (private_dir/"answer_key.json").write_text(json.dumps(key,indent=2,ensure_ascii=False)+"\n")
    for s in schedules:
        with (participant_dir/f"schedule_{s['sequence_id']}.csv").open("w",newline="") as h:
            w=csv.writer(h); w.writerow(["position","case_id","condition","target_path","target_sha256"])
            for item in s["cases"]:
                target=surface_manifest[item["case_id"]]["targets"][item["condition"]]; w.writerow([item["position"],item["case_id"],item["condition"],target["path"],target["sha256"]])
    return manifest,key


def main():
    p=argparse.ArgumentParser(); p.add_argument("report",type=Path); p.add_argument("html_dir",type=Path); p.add_argument("--out-dir",type=Path,required=True); a=p.parse_args(); report=json.loads(a.report.read_text()); manifest,_=build(report,a.html_dir,a.out_dir); print(json.dumps({"status":manifest["status"],"scored_cases":9,"sentinel":manifest["non_scored_sentinel"]["case_id"],"schedules":len(manifest["schedules"]),"conditions":list(manifest["conditions"])},indent=2)); return 0


if __name__=="__main__": raise SystemExit(main())
