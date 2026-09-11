"""Render an explicit historical snapshot; never poll, schedule, or grant authority."""
import argparse
import html
import sys
from pathlib import Path
from validate import HERE, read_json, validate


def text(value):
    return html.escape(str(value)).replace("\n", " ").replace("\r", " ").replace("|", "&#124;").replace("`", "&#96;").replace("[", "&#91;").replace("]", "&#93;")


def render(data):
    errors = validate(data)
    if errors:
        raise ValueError("\n".join(errors))
    lines = ["# Build status", "", f"Recorded snapshot: {text(data['recorded_at'])}.", "",
             "These are observed states, not live status or permission. Re-read the linked source and branch before acting. No freshness guarantee or automatic monitoring.", "",
             "| Work | Owner | Observed state | Next action |", "| --- | --- | --- | --- |"]
    for lane in data["lanes"]:
        lines.append("| " + " | ".join(text(lane[k]) for k in ["work_id", "owner", "state", "next_action"]) + " |")
    for lane in data["lanes"]:
        lines += ["", f"## {text(lane['work_id'])}: {text(lane['title'])}", "",
                  f"Observed {text(lane['observed_at'])}: {text(lane['repository'])}, branch {text(lane['branch'])}, head `{lane['observed_head']}`.", "",
                  "Write scope: " + (", ".join(text(p) for p in lane["write_scope"]) or "none") + ".",
                  "No-touch: " + "; ".join(text(p) for p in lane["no_touch"]) + ".",
                  "Hand-back: " + text(lane["handback_event"]) + "."]
        if lane["state"] == "waiting":
            lines += ["Blocker: " + text(lane["blocker"]) + ".", "Unblocks when: " + text(lane["unblocks_when"]) + "."]
        lines += ["", "Sources: " + " · ".join(f"[source {i+1}](<{url}>)" for i, url in enumerate(lane["sources"])) + "."]
        if lane["receipt"]:
            lines.append(f"[Recorded receipt](<{lane['receipt']}>).")
    lines += ["", "Closed work remains recorded. A successful build grants no wider authority.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", nargs="?", type=Path, default=HERE / "ledger.json")
    parser.add_argument("--output", type=Path, help="Write generated Markdown; otherwise stdout")
    args = parser.parse_args()
    try:
        result = render(read_json(args.ledger))
        if args.output:
            if args.output.resolve() in {args.ledger.resolve(), (HERE / "schema.json").resolve()}:
                raise ValueError("output cannot overwrite ledger or schema")
            args.output.write_text(result, encoding="utf-8", newline="\n")
        else:
            sys.stdout.write(result)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"NOT RENDERED: {exc}\n")


if __name__ == "__main__":
    main()
