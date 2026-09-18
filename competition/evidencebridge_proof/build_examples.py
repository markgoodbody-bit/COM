#!/usr/bin/env python3
from pathlib import Path
from evidencebridge import load_bundle, render_html, validate_bundle

ROOT=Path(__file__).resolve().parent
FIXTURES=ROOT/"fixtures"
OUT=ROOT/"generated"

def main():
    OUT.mkdir(exist_ok=True)
    for path in sorted(FIXTURES.glob("*.json")):
        bundle=load_bundle(path)
        validate_bundle(bundle)
        target=OUT/f"{path.stem}.html"
        target.write_text(render_html(bundle), encoding="utf-8")
        print(target.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
