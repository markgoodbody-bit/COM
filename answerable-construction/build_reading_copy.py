"""Render the existing working paper, without rewriting it. Requires ReportLab."""
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'planning/ANSWERABLE_CONSTRUCTION_WORKING_PAPER_v0_1.md'
OUTPUT = ROOT / 'output/pdf/Answerable_Construction_Working_Paper_v0_1.pdf'


def typography(text):
    # Typesetting only: source file is never changed.
    return text.replace('\u2014', '-').replace('\u2013', '-').replace('\u2011', '-')


def inline(text):
    text = html.escape(typography(text))
    text = re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)', r'<link href="\2" color="#865126">\1</link>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8">\1</font>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)


def build():
    revision = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--', str(SOURCE.relative_to(ROOT))], cwd=ROOT, text=True).strip()
    source_path = SOURCE.relative_to(ROOT).as_posix()
    raw = subprocess.check_output(['git', 'show', revision + ':' + source_path], cwd=ROOT)
    if SOURCE.read_bytes().replace(b'\r\n', b'\n') != raw.replace(b'\r\n', b'\n'):
        raise ValueError('Commit source edits before generating a revision-pinned reading copy')
    digest = hashlib.sha256(raw).hexdigest()
    styles = {
        'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=11, leading=15.5, spaceAfter=8),
        'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=23, leading=28, spaceAfter=17),
        'h2': ParagraphStyle('h2', fontName='Times-Bold', fontSize=15, leading=19, spaceBefore=17, spaceAfter=9, keepWithNext=True),
        'h3': ParagraphStyle('h3', fontName='Times-Bold', fontSize=12, leading=16, spaceBefore=12, spaceAfter=7, keepWithNext=True),
        'quote': ParagraphStyle('quote', fontName='Times-Italic', fontSize=11, leading=15.5, leftIndent=12, borderPadding=8, spaceBefore=5, spaceAfter=12),
        'code': ParagraphStyle('code', fontName='Courier', fontSize=7.5, leading=10.5, backColor=colors.HexColor('#f2f0ed'), borderPadding=8, spaceBefore=5, spaceAfter=12),
        'note': ParagraphStyle('note', fontName='Helvetica', fontSize=8, leading=11, spaceAfter=9),
        'bullet': ParagraphStyle('bullet', fontName='Times-Roman', fontSize=11, leading=15, leftIndent=13, firstLineIndent=-9, spaceAfter=4)
    }
    story, para, code = [], [], None

    def flush():
        if para:
            story.append(Paragraph(inline(' '.join(para)), styles['body']))
            para.clear()

    for line in raw.decode('utf-8').splitlines():
        if line.startswith('```'):
            flush()
            if code is None:
                code = []
            else:
                story.append(Preformatted(typography('\n'.join(code)), styles['code']))
                code = None
            continue
        if code is not None:
            code.append(line)
            continue
        if not line.strip() or line == '---':
            flush()
        elif line.startswith('# '):
            flush()
            story.append(Paragraph(inline(line[2:]), styles['title']))
        elif line.startswith('## '):
            flush()
            story.append(Paragraph(inline(line[3:]), styles['h2']))
        elif line.startswith('### '):
            flush()
            story.append(Paragraph(inline(line[4:]), styles['h3']))
        elif line.startswith('> '):
            flush()
            story.append(Paragraph(inline(line[2:]), styles['quote']))
        elif line.startswith('- ') or re.match(r'^\d+\. ', line):
            flush()
            story.append(Paragraph(inline(line), styles['bullet']))
        else:
            para.append(line.strip())
            if line.endswith('  '):
                flush()
    flush()
    if code is not None:
        raise ValueError('Unclosed source code fence')
    story += [Spacer(1, 12), Paragraph('Reading-copy provenance', styles['h3']),
              Paragraph('Derived from the unchanged Markdown working paper. This reading copy is not a formal release. Dash glyphs are normalised for typesetting; wording and order are retained. Source links are clickable.', styles['note']),
              Paragraph('Source revision: ' + revision, styles['note']),
              Paragraph('Source SHA-256: ' + digest, styles['note'])]

    def page(canvas, doc):
        canvas.saveState()
        w, h = doc.pagesize
        canvas.setStrokeColor(colors.HexColor('#b5987d'))
        canvas.line(23*mm, h-18*mm, w-23*mm, h-18*mm)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#5a6266'))
        canvas.drawString(23*mm, h-15*mm, 'ANSWERABLE CONSTRUCTION')
        canvas.drawString(23*mm, 15*mm, 'WORKING PAPER - NOT CANON')
        canvas.drawRightString(w-23*mm, 15*mm, str(doc.page))
        canvas.restoreState()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=(210*mm, 297*mm), leftMargin=23*mm, rightMargin=23*mm,
                            topMargin=25*mm, bottomMargin=24*mm, title='Answerable Construction - Working Paper v0.1',
                            author='Mark with AI collaborators', invariant=1)
    doc.build(story, onFirstPage=page, onLaterPages=page)
    record = {'source_path': str(SOURCE.relative_to(ROOT)).replace('\\', '/'), 'source_revision': revision,
              'source_sha256': digest, 'pdf_path': str(OUTPUT.relative_to(ROOT)).replace('\\', '/'),
              'pdf_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
              'status': 'derived reading copy; not formal release or canon',
              'typesetting': 'ASCII dash normalisation; Markdown emphasis and links rendered; added source-provenance note'}
    (OUTPUT.parent / 'reading-copy.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    build()
