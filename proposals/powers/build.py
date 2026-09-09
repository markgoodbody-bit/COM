"""Build only this isolated proposal; normal PSFH build untouched."""
import hashlib
import json
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image

ROOT = Path(__file__).resolve().parent
PARENT = "fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d"
RECEIPT = "a78d84f490d0331724150ab6ac2a0cd8690ab067ddd214db7e8da360b9d2288f"
PINS = {720: (603, 201415, "c424b6927b35b4546850b317a303699cad952d1852d1e9c6d77dc246e29ba802"),
        1440: (1206, 862531, "816b56a1f0f650c882fa151b7c30d0a6e5d32fe218a70bfee675004b9bb9c59f")}
FILES = ["index.html", "work.css", "artwork.json", "responsive.json", "acquisition.json",
         "assets/bible-quilt-delivered.jpg", "assets/bible-quilt-720.jpg", "assets/bible-quilt-1440.jpg"]
ROUTES = dict(zip(FILES, ["works/harriet-powers/index.html", "works/harriet-powers/work.css",
    "art/harriet-powers.json", "art/harriet-powers-responsive.json", "art/harriet-powers-acquisition.json",
    "art/bible-quilt-delivered.jpg", "art/bible-quilt-720.jpg", "art/bible-quilt-1440.jpg"]))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.links, self.tags = [], [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        require(not any(k.startswith("on") for k in attrs), "Event handlers forbidden")
        if tag == "img":
            self.images.append(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))


def validate(root=ROOT):
    record = json.loads((root / "artwork.json").read_text(encoding="utf-8"))
    responsive = json.loads((root / "responsive.json").read_text(encoding="utf-8"))
    require(sha((root / "acquisition.json").read_bytes()) == RECEIPT, "Acquisition receipt changed")
    require(record["master_status"] == "UNKNOWN", "Master status overclaim")
    require(record["creator"] == "Harriet Powers" and record["title"] == "Bible Quilt", "Creator/work changed")
    require(record["date"] == "1885–1886" and record["institution"] == "National Museum of American History, Smithsonian Institution", "Date/institution changed")
    require(record["acquisition_receipt"] == "/art/harriet-powers-acquisition.json" and
            record["responsive_record"] == "/art/harriet-powers-responsive.json", "Provenance route changed")
    require(record["sha256"] == PARENT and record["parent_file"] == "/" + ROUTES[FILES[5]], "Parent identity changed")
    require((record["width"], record["height"], record["bytes"]) == (2880, 2412, 2671829), "Parent record dimensions/bytes")
    require(record["source_url"] == "https://ids.si.edu/ids/deliveryService?id=NMAH-75-2984", "Source route changed")
    require(record["object_url"] == "https://americanhistory.si.edu/collections/object/nmah_556462", "Object route changed")
    require(record["rights"]["observation_receipt"].endswith("#issuecomment-5604591035") and
            "not Codex acquisition-time" in record["rights"]["observation_by"], "Rights attribution collapsed")
    require(record["rights"]["url"] == "https://www.si.edu/openaccess", "Rights URL changed")
    parent = root / FILES[5]
    require(sha(parent.read_bytes()) == PARENT and parent.stat().st_size == 2671829, "Parent bytes changed")
    with Image.open(parent) as source:
        require(source.size == (2880, 2412), "Decoded parent dimensions")
        icc = source.info.get("icc_profile")
    require(responsive["parent"] == dict(file=parent.name, width=2880, height=2412, bytes=2671829, sha256=PARENT), "Responsive parent changed")
    require([v["width"] for v in responsive["variants"]] == [720, 1440], "Missing/extra/reordered variants")
    for v in responsive["variants"]:
        width = v["width"]
        height, count, digest = PINS[width]
        require(v["file"] == f"bible-quilt-{width}.jpg", "Variant path changed")
        require((v["height"], v["bytes"], v["sha256"]) == (height, count, digest), "Variant pin changed")
        require(v["parent_sha256"] == PARENT, "Derivative detached from source")
        data = (root / "assets" / v["file"]).read_bytes()
        require(len(data) == count and sha(data) == digest, "Derivative bytes changed")
        with Image.open(root / "assets" / v["file"]) as image:
            require(image.size == (width, height), "Decoded derivative dimensions")
            require(image.info.get("icc_profile") == icc, "Source ICC not retained")
    html = (root / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    require(not set(page.tags) & {"script", "form", "iframe"}, "Active content forbidden")
    require(len(page.images) == 1, "One complete work, no repeated image")
    require(page.images[0]["src"] == "../../art/bible-quilt-1440.jpg", "Wrong fallback")
    require(page.images[0]["srcset"] == "../../art/bible-quilt-720.jpg 720w, ../../art/bible-quilt-1440.jpg 1440w", "Wrong responsive route")
    require(bool(page.images[0].get("alt")), "Missing alt text")
    require(html.index("The maker's recorded account") < html.index("Our response · PSFH"), "Maker account must precede response")
    require(record["creator_account"]["statement"] in html and record["project_response"]["text"] in html, "Record/page wording differs")
    require(record["visible_credit"] in html.replace("<cite>", "").replace("</cite>", ""), "Visible credit drift")
    require(record["object_url"] in page.links and record["rights"]["url"] in page.links, "Source/rights route missing")
    for link in page.links:
        if not link.startswith(("https://", "#")):
            resolved = urljoin("/works/harriet-powers/", link).lstrip("/")
            require(resolved in ROUTES.values(), "Local route missing or outside proposal")
    return {name: {"bytes": (root / name).stat().st_size, "sha256": sha((root / name).read_bytes())} for name in FILES}


def build():
    inventory = validate()
    target = ROOT.parents[1] / "outputs/powers-work-page"
    output_inventory = {}
    for name in FILES:
        destination = target / ROUTES[name]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
        require(sha(destination.read_bytes()) == inventory[name]["sha256"], "Output copy differs")
        output_inventory[ROUTES[name]] = inventory[name]
    (target / "inventory.json").write_text(json.dumps(output_inventory, indent=2) + "\n", encoding="utf-8")
    require({p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()} ==
            set(ROUTES.values()) | {"inventory.json"}, "Unexpected stale output; do not publish")
    print(f"PASS: {len(FILES)} exact static proposal files at {target}")


if __name__ == "__main__":
    build()
