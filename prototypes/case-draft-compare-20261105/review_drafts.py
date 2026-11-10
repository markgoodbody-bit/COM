#!/usr/bin/env python3
"""Human entry to the existing offline comparison; never opens a browser or uploads."""
import argparse
from pathlib import Path
import sys
import tempfile

import compare
import html_report


def selected_path(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] == '"':
        text = text[1:-1]
    if not text:
        raise compare.CompareError('Choose an older draft and a newer draft.')
    return Path(text).expanduser().resolve(strict=True)


def review_files(before, after, summary=False, report_parent=None):
    before, after = Path(before).resolve(strict=True), Path(after).resolve(strict=True)
    if before.samefile(after):
        raise compare.CompareError('The same file was selected twice; choose two different drafts.')
    # The default remains beside the newer input. Explicit storage uses only an
    # existing folder chosen by the writer, never an implicit new parent path.
    if report_parent is None:
        parent = after.parent
    else:
        try:
            parent = Path(report_parent).expanduser().resolve(strict=True)
        except (OSError, RuntimeError):
            raise compare.CompareError('Selected report folder is not available.') from None
        if not parent.is_dir():
            raise compare.CompareError('Selected report location must be an existing folder.')
    a, b = compare._read(before), compare._read(after)
    # Complete parsing and bounded rendering before creating any output folder.
    differences = compare.changes(compare.parse_json(a), compare.parse_json(b))
    report = html_report.render_html(differences, compare.sha256(a), compare.sha256(b), summary)
    folder = Path(tempfile.mkdtemp(prefix='draft-review-', dir=str(parent)))
    destination = folder / 'comparison.html'
    try:
        compare._atomic(destination, report)
    except BaseException:
        # Remove only this newly allocated empty folder, never existing files.
        try:
            folder.rmdir()
        except OSError:
            pass
        raise
    return destination


def main(argv=None, ask=input):
    parser = argparse.ArgumentParser(description='Review two saved drafts privately, without changing either file')
    parser.add_argument('before', nargs='?', help='older draft; otherwise ask for it')
    parser.add_argument('after', nargs='?', help='newer draft; otherwise ask for it')
    parser.add_argument('--summary', action='store_true', help='counts-only HTML, without authored values or file fingerprints')
    parser.add_argument('--report-parent', metavar='FOLDER',
                        help='write the new report subfolder inside an existing folder you choose; default is beside the newer draft')
    args = parser.parse_args(argv)
    if sys.version_info < (3, 10):
        print('This kit needs an existing Python 3.10 or newer.', file=sys.stderr)
        return 2
    print('Review two saved JSON drafts')
    print('Counts-only report.' if args.summary else 'Private detailed report: it will contain your draft text.')
    try:
        before = selected_path(args.before if args.before is not None else ask('Older draft: drag its file here, then press Enter: '))
        after = selected_path(args.after if args.after is not None else ask('Newer draft: drag its file here, then press Enter: '))
        destination = review_files(before, after, args.summary, args.report_parent)
    except (EOFError, KeyboardInterrupt):
        print('\nCancelled. No report created.')
        return 1
    except compare.CompareError as exc:
        print('No report created: ' + str(exc), file=sys.stderr)
        return 2
    except (OSError, UnicodeError, RecursionError):
        print('No report created. Check the selected files and folder permissions.', file=sys.stderr)
        return 2
    print('Report saved in a new folder in the selected folder:' if args.report_parent
          else 'Report saved in a new folder beside the newer draft:')
    print(str(destination))
    print('Open comparison.html to read it. Your two drafts were not changed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
