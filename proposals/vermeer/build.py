"""Validate and copy this isolated proposal only. No network or image transforms."""
import hashlib
import json
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image

ROOT = Path(__file__).resolve().parent
IMAGE_SHA = "2eb8819e4afe22c219d7fbd01766e41338c5fbe460d0d41c250f8c698fd39106"
RECEIPT_SHA = "2740dd8d2284044f17415db2f08f6edeb7b7b2f9d9df2b6327c9500724540867"
ROUTES = {
    "index.html": "works/johannes-vermeer/index.html",
    "work.css": "works/johannes-vermeer/work.css",
    "artwork.json": "art/vermeer.json",
    "acquisition.json": "art/vermeer-acquisition.json",
    "assets/staedel-1149-thumb-xl.jpg": "art/staedel-1149-thumb-xl.jpg",
}
OBJECT = "https://sammlung.staedelmuseum.de/en/work/the-geographer"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.links, self.tags, self.ids = [], [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        require(not any(k.startswith("on") for k in attrs), "Event handler")
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "img":
            self.images.append(attrs)
        if tag in {"a", "link"}:
            self.links.append(attrs.get("href", ""))


def validate(root=ROOT):
    record = json.loads((root / "artwork.json").read_text(encoding="utf-8"))
    require(sha((root / "acquisition.json").read_bytes()) == RECEIPT_SHA, "Acquisition history changed")
    pinned = {
        "creator": "Johannes Vermeer", "title": "The Geographer", "date": "1669",
        "medium": "Oil on canvas", "institution": "Städel Museum, Frankfurt am Main",
        "inventory_number": "1149", "object_url": OBJECT,
        "source_url": "https://cdn.staedelmuseum.de/images/49/7c/1149/thumb-xl.jpg",
        "source_category": "AUTHORITATIVE_RECORD_LINKED_THUMB_XL", "master_status": "UNKNOWN",
        "file": "/art/staedel-1149-thumb-xl.jpg", "width": 915, "height": 1024,
        "bytes": 147792, "sha256": IMAGE_SHA,
        "acquisition_receipt": "/art/vermeer-acquisition.json",
        "acquisition_receipt_sha256": RECEIPT_SHA, "project_response": None,
    }
    for key, value in pinned.items():
        require(record[key] == value, "Record drift: " + key)
    require(record["rights"]["label"] == "Public Domain" and record["rights"]["url"] == OBJECT, "Rights drift")
    image_path = root / "assets/staedel-1149-thumb-xl.jpg"
    data = image_path.read_bytes()
    require(len(data) == 147792 and sha(data) == IMAGE_SHA, "Image bytes changed")
    with Image.open(image_path) as image:
        require(image.size == (915, 1024) and image.mode == "RGB", "Image decode drift")
        require(not image.info.get("icc_profile") and image.getexif().get(274) is None, "Profile/orientation drift")
    html = (root / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    require(not set(page.tags) & {"script", "form", "iframe"}, "Active content")
    require(len(page.images) == 1, "One whole work required")
    img = page.images[0]
    require(img.get("src") == "../../art/staedel-1149-thumb-xl.jpg" and "srcset" not in img, "Unexpected image selection")
    require((img.get("width"), img.get("height")) == ("915", "1024") and bool(img.get("alt")), "Image dimensions/alt")
    require(record["visible_credit"] in html and record["museum_account"] in html, "Record/page wording drift")
    require(OBJECT in page.links and record["artist_url"] in page.links, "Museum routes missing")
    require(html.index("</figure>") < html.index('class="museum-note"'), "Account precedes work")
    for link in page.links:
        if link.startswith("#"):
            require(link[1:] in page.ids, "Missing anchor")
        elif not link.startswith("https://"):
            require(urljoin("/works/johannes-vermeer/", link).lstrip("/") in ROUTES.values(), "Missing local route")
    css = (root / "work.css").read_text(encoding="utf-8")
    require("max-width: 640px" in css and "max-width: 915px" in css and "height: auto" in css, "Native presentation bound missing")
    require("object-fit: cover" not in css and "background-image" not in css, "Crop/wallpaper")
    return {name: {"bytes": (root / name).stat().st_size, "sha256": sha((root / name).read_bytes())} for name in ROUTES}


def build():
    inventory = validate()
    target = ROOT.parents[1] / "outputs/vermeer-work-page"
    output_inventory = {}
    for name, route in ROUTES.items():
        destination = target / route
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
        require(sha(destination.read_bytes()) == inventory[name]["sha256"], "Output copy differs")
        output_inventory[route] = inventory[name]
    (target / "inventory.json").write_text(json.dumps(output_inventory, indent=2) + "\n", encoding="utf-8")
    require({p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()} == set(ROUTES.values()) | {"inventory.json"}, "Stale output; do not publish")
    print(f"PASS: {len(ROUTES)} exact static proposal files at {target}")


if __name__ == "__main__":
    build()
