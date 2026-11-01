"""In-memory Chromium keyboard test; file:// transport NOT tested."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    ctx = browser.new_context(accept_downloads=True)
    page = ctx.new_page()
    requests, errors = [], []
    page.on('request', lambda req: requests.append(req.url) if req.url.startswith(('http:', 'https:')) else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    html = (ROOT/'case_intake.html').read_text().replace('<script src="./case_intake.js" defer></script>', '')
    page.set_content(html)
    page.add_script_tag(content=(ROOT/'case_intake.js').read_text())
    page.evaluate("document.dispatchEvent(new Event('DOMContentLoaded'))")
    page.wait_for_function("document.querySelectorAll('#rows-claims .row').length === 1")
    assert page.title() == 'Case card — offline fill-in'

    add = page.locator('[data-add=claims]')
    add.focus()
    page.keyboard.press('Enter')
    assert page.locator('#rows-claims .row').count() == 2
    second = page.locator('#rows-claims .row').nth(1)
    assert second.get_attribute('aria-label') == 'Case claim 2 of 2', 'Dynamic groups need unique accessible context'
    assert second.locator('[data-field=kind]').evaluate('(el) => document.activeElement === el'), 'Keyboard Add must focus the new row'
    second.locator('[data-remove]').focus()
    page.keyboard.press('Enter')
    assert page.locator('#rows-claims .row').count() == 1
    assert add.evaluate('(el) => document.activeElement === el'), 'Keyboard Remove must restore a valid focus target'
    assert page.locator('#rows-claims .row').first.get_attribute('aria-label') == 'Case claim 1 of 1'

    for kind, label in [('parties', 'Person or group'), ('possibilities', 'Possible next action')]:
        button = page.locator(f'[data-add={kind}]')
        button.focus()
        page.keyboard.press('Enter')
        row = page.locator(f'#rows-{kind} .row').last
        assert row.get_attribute('aria-label') == f'{label} 1 of 1'
        assert row.locator('[data-field]').first.evaluate('(el) => document.activeElement === el')
        row.locator('[data-remove]').focus()
        page.keyboard.press('Enter')
        assert page.locator(f'#rows-{kind} .row').count() == 0
        assert button.evaluate('(el) => document.activeElement === el')

    for _ in range(23):
        add.click()
    assert page.locator('#rows-claims .row').count() == 24
    add.click()
    assert page.locator('#rows-claims .row').count() == 24, 'Cannot create an unexportable 25th claim'
    assert '24' in page.locator('#status').inner_text()
    assert not requests, f'Unexpected network calls: {requests}'
    assert not errors, f'Unexpected page errors: {errors}'
    browser.close()
print('IN-MEMORY KEYBOARD PASS: row count/labels, focus Add/Remove, cap 24, no HTTP, no page error')
