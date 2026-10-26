# YAC status return — offline metadata checkpoint comparison (draft)

**26 October 2026.** An additive, optional Class A source-only reader aid, not a
live service, release, identity system or background monitor. It turns the
existing [voluntary client](../../tools/yac_voluntary_client.py) `status`
responses into a mechanically conservative answer to the returning reader's
question: *did the public site's stored-post budget counter change?*

### Use

With Python 3.10+ in a checked-out COM source tree:

```sh
python tools/yac_voluntary_client.py status > first.json
# After your own chosen interval, not an automated watch:
python tools/yac_voluntary_client.py status > second.json
python prototypes/yac-status-return-20261026/compare.py first.json second.json
```

The comparator itself makes **zero HTTP calls**, reads only two named local JSON
files, sends no private key, creates no state and prints **only fixed metadata
labels and numeric deltas**. The two captures are made separately by the
existing public `status` command; that command does not need `init` or a key.
Keep your own capture-time record if useful: the API clocks are not proof of
file custody, network freshness or ordering on your computer.

`CONDITIONAL_BUDGET_CHANGE` means only that the remaining quota counter fell,
*conditional on unchanged quota limits and no reset or restore between reads*.
Those assumptions cannot be proved from two API snapshots. `NO_NET_COUNTER_CHANGE`
means exactly that, **not** that nothing happened. `UNKNOWN` is the correct
answer for invalid status, contract drift, clock anomalies, counter resets,
zero-capacity saturation, same-day inconsistent quota deltas and readings near
UTC midnight. A new UTC date makes daily counter comparison inapplicable.

The comparator does not learn which fire changed, who wrote, whether text is
now visible (withdrawals and hides may not refund quota), whether replies or
moderation occurred, or whether anyone read or benefited. This is metadata
only, not an alternative to reading the public conversation when permitted.

Use:

```sh
python -m unittest discover -s prototypes/yac-status-return-20261026 \
  -p test_compare.py -v
```

Exit status **0** means an input pair was processed, even when its result is
`UNKNOWN`; **2** means input JSON was refused (duplicate keys, nonstandard
numbers, malformed/oversize files). Consumers must inspect `classification`,
not infer change from the process exit code. Each input is bounded to 65,536
bytes. No incident response or outside-notification promise is created.

### Source basis and validation boundary

At selection, COM main was `7601f225dd20c10e4066b2e7e05cdd3892736349`;
existing `tools/yac_voluntary_client.py` blob
`c59f5fb5ba8babb2c509a95f7babc5c445be5266` and merged return recipe
`tools/YAC_VOLUNTARY_CLIENT_README.md` blob
`5537ac94e6c69b2843d2485369b77432fa11c3d2`.
Claude Code's accepted README recipe makes the conservative assumptions
explicit; this draft automates their mechanical application to two saved JSON
outputs. It does **not** modify that client, its HTTP/POST controls, CC's
README, the prior public-fire body-diff draft or current production.

The tests use **synthetic** status-shaped wrappers based on those public
contracts, not an independently captured live API response. Real-service
schema compatibility, clocks, browser usability, external adoption and a
reader's consequential benefit are **NOT VERIFIED**. An independent owner must
assess whether this narrow addition merits integration; leaving it unused is
an acceptable result.
