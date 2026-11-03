"""Real Chromium DOM interaction acceptance for optional case-card draft review.

Requires preinstalled Playwright Python and Chromium. No browser installation,
network/server access, credentials, provider APIs or source modifications.
Loads exact local HTML+JS in memory because some managed Chromium builds block
file:// navigation. Thus this proves browser DOM behaviour, NOT file:// use.
Data are fictional; all evidence/state/deadline labels remain author claims.
Run: python3 tests/browser_review_acceptance.py
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import os
from playwright.sync_api import sync_playwright
import json, hashlib

root=Path(__file__).resolve().parent.parent
html=root/'case_intake.html'
checks=[]
def check(label, condition):
    assert condition, label
    checks.append(label)

with sync_playwright() as p:
    executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not executable:
        raise RuntimeError('NOT_RUN: installed Chromium unavailable; no browser installation attempted')
    browser=p.chromium.launch(executable_path=executable, headless=True, args=['--no-sandbox'])
    context=browser.new_context(accept_downloads=True, viewport={'width':390,'height':844})
    page=context.new_page()
    errors=[]; requests=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('request',lambda r: requests.append(r.url) if r.url.startswith(('http://','https://')) else None)
    # In-memory real browser DOM. file:// path, CSP and offline launch remain unverified.
    html_src=html.read_text().replace('<script src="./case_intake.js" defer></script>', '')
    page.set_content(html_src)
    page.add_script_tag(content=(root/'case_intake.js').read_text())
    page.evaluate("document.dispatchEvent(new Event('DOMContentLoaded'))")
    check('real DOM content loaded', page.title()=='Case card — offline fill-in')
    check('JS attached in real browser DOM', page.locator('#rows-claims .row').count()==1)
    page.locator('#case-title').fill('Fictional bus notice')
    claim=page.locator('#rows-claims .row').first
    claim.locator('[data-field=evidence]').select_option('reported')
    injected='<script>window.bad=1</script>\n## VERIFIED BY AUTHORITY'
    claim.locator('[data-field=text]').fill(injected)
    page.locator('[data-add=parties]').click()
    party=page.locator('#rows-parties .row').first
    party.locator('[data-field=name]').fill('Passenger')
    party.locator('[data-field=aim]').fill('Keep a reachable stop')
    page.locator('[data-add=possibilities]').click()
    pos=page.locator('#rows-possibilities .row').first
    pos.locator('[data-field=party]').fill('Passenger')
    pos.locator('[data-field=description]').fill('Request notice')
    pos.locator('[data-field=state]').select_option('possible')
    page.locator('#return-fields [data-field=unresolved]').fill('When did the change actually occur?')
    page.locator('#review-draft').focus()
    page.keyboard.press('Enter')
    review=page.locator('#draft-review')
    check('review visible', review.is_visible())
    check('literal markup remains text', injected in review.inner_text() and review.locator('script').count()==0)
    check('author-labeled source', 'author evidence label; unverified' in review.inner_text())
    check('aim and possibility appear', 'Keep a reachable stop' in review.inner_text() and 'not permission or execution' in review.inner_text())
    check('review receives keyboard focus', review.evaluate('(e) => document.activeElement === e'))
    check('no runtime XSS', not page.evaluate('Boolean(window.bad)'))
    claim.locator('[data-field=text]').fill('An altered notice, still only reported')
    check('stale review hidden after edit', review.is_hidden() and review.inner_text()=='')
    page.locator('#review-draft').click()
    check('fresh review reflects edit', 'An altered notice' in review.inner_text() and injected not in review.inner_text())
    safe={'title':'Imported synthetic account','claims':[{'kind':'change','text':'No new corroboration','evidence':'unknown'}], 'correction':{'window':'unknown'}}
    payload=json.dumps(safe).encode('utf-8')
    page.locator('#import-json').set_input_files({'name':'safe.json','mimeType':'application/json','buffer':payload})
    page.wait_for_function("document.querySelector('#case-title').value === 'Imported synthetic account'")
    check('safe import changed draft', page.locator('#case-title').input_value() == 'Imported synthetic account')
    check('successful import clears review', review.is_hidden() and review.inner_text()=='')
    page.locator('#review-draft').click()
    check('imported unknown window not closed', 'author reports unknown; not a closed window' in review.inner_text())
    check('imported unknown source stays unknown', 'No new corroboration' in review.inner_text() and 'author evidence label; unverified' in review.inner_text())
    # A rejected duplicate-key import must leave both the edited case and review intact.
    before=review.inner_text()
    invalid=b'{"title":"X","title":"Y","claims":[{"kind":"change","text":"A","evidence":"unknown"}]}'
    page.locator('#import-json').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':invalid})
    page.wait_for_function("document.querySelector('#status').textContent.includes('Import refused')")
    check('duplicate-key import refused in Chromium', 'duplicate JSON key' in page.locator('#status').inner_text())
    check('failed import preserves review and form', review.inner_text()==before and page.locator('#case-title').input_value()==safe['title'])
    with page.expect_download() as d:
        page.get_by_role('button', name='Check and download JSON').click()
    download=d.value
    with TemporaryDirectory() as temp:
        output=Path(temp)/'observed-downloaded.json'
        download.save_as(output)
        exported=json.loads(output.read_text())
        check('export exact source content', exported==safe)
        digest=hashlib.sha256(output.read_bytes()).hexdigest()
    check('no external HTTP', requests==[])
    check('no exceptions', errors==[])
    check('390px viewport no horizontal overflow', page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
    print('CHROMIUM',browser.version,'URL',page.url)
    print('PASS',len(checks),'checks:',' | '.join(checks))
    print('DOWNLOADED_SHA256', digest)
    browser.close()
