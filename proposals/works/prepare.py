"""Explicit one-time source-bound copies. Normal build does not transform images."""
import hashlib
import json
import shutil
from pathlib import Path
import PIL
from PIL import Image, features

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = Path('C:/Users/markg/Downloads')
JOBS = [
    ('atkins', '291638', None, [720, 1440]),
    ('shen', '49549', None, [720, 1200]),
    ('lewis', 'saam_1994.17', 'SAAM-1994.17_1', [720, 1440]),
    ('lewis', 'saam_1994.17', 'SAAM-1994.17_2', [720, 1440]),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    custody = json.loads((DOWNLOADS / 'DEV/COM/evidence/PSFH_HUMAN_ART_BATCH_A_ACQUISITION_20260909.json').read_text(encoding='utf-8'))
    output = {}
    for work, oid, view, widths in JOBS:
        r = next(r for r in custody['records'] if r['object_id'] == oid and r.get('view_id') == view)
        source = DOWNLOADS / r['local_batch_directory'] / r['file']
        assert digest(source) == r['sha256'] and source.stat().st_size == r['bytes']
        assets = ROOT / work / 'assets'
        assets.mkdir(parents=True, exist_ok=True)
        stem = view or work
        parent = assets / (stem + '-source.jpg')
        if parent.exists():
            assert digest(parent) == r['sha256'], 'Refuse source overwrite'
        else:
            shutil.copyfile(source, parent)
        with Image.open(parent) as im:
            assert im.mode == 'RGB' and im.getexif().get(274) in (None, 1)
            icc = im.info.get('icc_profile')
            variants = []
            for width in widths:
                assert width <= im.width
                height = round(im.height * width / im.width)
                copy = im.resize((width, height), Image.Resampling.LANCZOS)
                name = f'{stem}-{width}.jpg'
                target = assets / name
                copy.save(target, 'JPEG', quality=86, subsampling=2, optimize=False, progressive=False, icc_profile=icc)
                variants.append(dict(file=name, width=width, height=height, bytes=target.stat().st_size,
                                     sha256=digest(target), parent_sha256=r['sha256']))
        public_receipt = {k:v for k,v in r.items() if k not in {'local_batch_directory','raw_receipt','raw_receipt_sha256','presentation_status'}}
        entry = dict(source=public_receipt, parent_file=parent.name, variants=variants,
                     tool=dict(pillow=PIL.__version__, jpeg=features.version('jpg')), settings=dict(
                     filter='Lanczos', quality=86, subsampling=2, optimize=False, progressive=False,
                     mode='RGB retained', icc='retained byte-for-byte', exif='No EXIF copied; orientation absent or1',
                     crop=False, upscale=False), purpose='Smaller full-frame delivery copies; originals remain linked. Not colour-fidelity validation.')
        output.setdefault(work, []).append(entry)
    for work, views in output.items():
        (ROOT / work / 'images.json').write_text(json.dumps(views,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Prepared8 full-frame viewing copies;4 exact sources retained. Pillow', PIL.__version__)
    for work, views in output.items():
        for v in views:
            print(work, [(x['width'], x['bytes'], x['sha256']) for x in v['variants']])


if __name__ == '__main__':
    main()
