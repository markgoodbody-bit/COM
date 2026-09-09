"""One-time proportional viewing copies; no network and no parent mutation."""
import hashlib
import json
from pathlib import Path

import PIL
from PIL import Image, features

ROOT = Path(__file__).resolve().parent
PARENT_HASH = "fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d"


def describe(file):
    data = file.read_bytes()
    with Image.open(file) as image:
        width, height = image.size
    return dict(file=file.name, width=width, height=height, bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest())


def prepare():
    parent = ROOT / "assets/bible-quilt-delivered.jpg"
    if describe(parent)["sha256"] != PARENT_HASH:
        raise ValueError("Acquired parent differs from the frozen receipt")
    # Pin the first preparation environment. Other encoders may produce different bytes.
    if PIL.__version__ != "12.2.0" or features.version("jpg") != "8.0":
        raise ValueError("Use the recorded Pillow/JPEG versions; do not silently repin")
    variants = []
    with Image.open(parent) as source:
        if source.size != (2880, 2412) or source.mode != "RGB":
            raise ValueError("Unexpected source dimensions or colour mode")
        for width, quality in [(720, 85), (1440, 86)]:
            height = round(source.height * width / source.width)
            resized = source.resize((width, height), Image.Resampling.LANCZOS)
            target = ROOT / f"assets/bible-quilt-{width}.jpg"
            resized.save(target, format="JPEG", quality=quality, subsampling=2,
                         optimize=False, progressive=False,
                         icc_profile=source.info.get("icc_profile", b""))
            variants.append({**describe(target), "quality": quality,
                             "parent_sha256": PARENT_HASH})
    record = dict(parent=describe(parent), variants=variants,
                  tool=f"Pillow {PIL.__version__}; JPEG {features.version('jpg')}",
                  settings="Lanczos proportional resize; nearest integer height; JPEG subsampling=2, optimize=false, progressive=false; source ICC retained; no EXIF copied, no orientation transform, no crop, retouch or generative operation.",
                  prepared_on="2026-09-09")
    (ROOT / "responsive.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    if describe(parent)["sha256"] != PARENT_HASH:
        raise ValueError("Parent changed during preparation")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    prepare()
