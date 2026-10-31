"""Optional local browser smoke; requires externally installed Playwright/Chromium. Not needed at runtime."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context=browser.new_context(accept_downloads=True)
    page=context.new_page()
    requests=[]
    page.on('request',lambda request: requests.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
    errors=[]
    page.on('pageerror', lambda err:errors.append(str(err)))
    html=(root/'case_intake.html').read_text()
    html=html.replace('<script src="./case_intake.js" defer></script>', '')
    page.set_content(html)
    page.add_script_tag(content=(root/'case_intake.js').read_text())
    page.evaluate("document.dispatchEvent(new Event('DOMContentLoaded'))")
    page.locator('#case-title').fill('Synthetic: case form route')
    page.locator('#case-scope').fill('Imaginary context')
    page.locator('#rows-claims [data-field=text]').fill('## ASSERTED VERIFIED\n<svg onload=alert(1)>')
    page.locator('#rows-claims [data-field=evidence]').select_option('unknown')
    page.locator('[data-add=parties]').click()
    page.locator('#rows-parties [data-field=name]').fill('Person A')
    page.locator('#rows-parties [data-field=aim]').fill('Keep access')
    page.locator('#rows-parties [data-field=boundary]').fill('Avoid unsafe route')
    with page.expect_download() as download_event:
        page.get_by_text('Check and download JSON').click()
    download=download_event.value
    payload=Path(download.path()).read_text()
    obj=json.loads(payload)
    assert obj['claims'][0]['evidence']=='unknown'
    assert obj['claims'][0]['text']=='## ASSERTED VERIFIED\n<svg onload=alert(1)>'
    assert obj['parties'][0]['name']=='Person A'
    assert 'correction' not in obj
    assert download.suggested_filename=='case-card-draft.json'
    fixture=root/'examples'/'browser_roundtrip.json'
    fixture.write_text(payload)
    page.locator('#case-title').fill('NOT SAVED')
    page.locator('#import-json').set_input_files(str(fixture))
    page.wait_for_function("document.getElementById('status').textContent.includes('imported') || document.getElementById('status').textContent.includes('Import refused')")
    assert page.locator('#case-title').input_value()=='Synthetic: case form route'
    assert page.locator('#rows-claims [data-field=text]').input_value()=='## ASSERTED VERIFIED\n<svg onload=alert(1)>'
    duplicate=root/'examples'/'browser_invalid.json'
    duplicate.write_text('{"title":"A","title":"B","claims":[]}')
    page.locator('#import-json').set_input_files(str(duplicate))
    page.wait_for_function("document.getElementById('status').textContent.includes('Import refused')")
    assert 'Import refused' in page.locator('#status').inner_text()
    assert page.locator('#case-title').input_value()=='Synthetic: case form route'
    assert not requests, requests
    assert not errors, errors
    print('BROWSER_SMOKE PASS: local export/import, blocked duplicate, faithful adversarial text, no HTTP requests, no page exceptions')
    browser.close()
