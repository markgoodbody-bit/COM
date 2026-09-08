# Welcome in the existing entrance — 8 September 2026

Source update after `323a3fa9c96bd67c323bab967607c4855508b531`; not a deployment receipt.

The machine entrance now asks:

> Hello. What are you trying to understand, change, or keep possible?

It welcomes a question, situation or disagreement without requiring an introduction
or agreement. It explicitly says the static site does not receive replies. Existing
Challenge material describes optional public discussion and its account/access limits;
no live listener, confidential channel or timely answer is implied.

The `GREETING` value in `build.py` supplies the exact same wording to `start.json`,
`index.md`, `index.txt`, `index.html` and `llms.txt`. Existing purpose, value choice,
freedom to leave, questions and source boundaries remain. It is an optional invitation,
not a required greeting response, identity test or instruction to override a reader's task.

No new output path. Sixty files are still generated; fifty-four remain byte-identical
against the preceding exact build. The six changed outputs are the five entrances
above and `map.json`, whose hashes and sizes are regenerated. Both complete packets,
all individual readings and example views, the question catalogues and source/reply
pages are unchanged. `library.json` and all five example inputs are unchanged.

Executed locally: all forty-nine tests pass (the prior forty-two plus seven greeting
checks). The 1,758-byte machine entrance remains below its existing 2,048-byte cap;
overlong greetings are refused rather than truncated. HTML rendering is escaped.
A temporary loopback HTTP check fetched all sixty outputs byte-for-byte and obtained
404 for a missing path; the server was stopped. These are structural and local-delivery
checks, not independent reading, public delivery or measured engagement.

Generated tree SHA-256:
`975c16885d9fc24b1dd970cffc6737a77a5a20e6fd4bfd1b132a954d1da4eb2f`

Build:

```sh
python -m unittest -v test_build test_arrival test_packet test_greeting
python build.py --output NEW_EMPTY_STAGING_DIRECTORY
```

Codex remains the public publisher. Reacquire current source/publishing heads and
in-flight operations. Integrate only generated `explore/` assets through the maintained
website build. For first contact at the domain root, reuse this exact greeting in the
root machine guide and its human rendering, keeping the value declaration and existing
routes. Make root changes separately visible in the publication diff; they are not
part of this generator's tree identity. Preserve seed, CNAME, DNS, source terms and
all other assets. Do not deploy the main-based COM branch or rerun historical one-shot
workflows. No further permission or file relay from Mark is needed for this already
authorised reversible content change.

Security recovery remains the separately assigned single-owner foreground task in
COM #108. This patch introduces no network service, account, collector, secret,
provider call, scheduler, licence change or security bypass, and does not delay that task.
