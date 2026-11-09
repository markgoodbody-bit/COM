# One source candidate for the optional case-draft comparison tool

Build acquired the complete nine-file tree at `aa8635dda2e0ee24751d1b50d0e4ed8e6f419184`, including the HTML reader (`59045884`), summary privacy correction (`72553751`), report-size guard (`aa8635dd`) and preceding comparison/overflow fixes. The full inherited suite ran together: **53 tests passed, zero failures**, Python standard library, cloud workspace, 9 November 2026. Earlier isolated test counts remain history; this is the first acquired Build integration result for the complete candidate.

No domain ethics decision is automated here. It compares authored JSON fields, can recognise exact complete row permutations when requested, and renders a report. It does not check whether a changed claim is true or whether either document follows a case-card schema.

## Run from this folder

Requires an existing Python 3.10 or later. No package installation, account, API key or internet connection is needed.

```sh
python html_report.py examples/before.json examples/after.json --output comparison.html
```

Open `comparison.html` in a browser to read the two versions beside each other. This integration executed the CLI and checked the emitted HTML as text; it did not run a browser or assistive technology. For a counts-only view, add `--summary`. Counts can still disclose information; full reports contain authored text. Keep reports private unless their contents have been checked for sharing.

For a plain-text report:

```sh
python compare.py examples/before.json examples/after.json
```

To check the complete source suite:

```sh
python -m unittest discover -p 'test_*.py' -v
```

The two examples are clearly authored fiction. They show how an evidence label and maintenance account changed; comparison output is not proof of a real user report, funded team or improvement in the world. Neither input is modified. Generated reports are deliberately not checked into the source tree.

## Integration boundaries

The maintained candidate is saved on a Build source branch. COM main, released ME/TRACE, the public website, the installed game and every private draft are unchanged. No extra scheduled audit, model run, runtime wake or manual COMSYNC is required to use this source candidate. The remaining browser/reader-use questions are open without requiring another test loop before somebody chooses to use the tool.
