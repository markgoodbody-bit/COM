# NVIDIA Prototype request-shape correction — 19 September 2026

Status: **OWNER-PAGE CORRECTION / ADAPTER UPDATED / PRIOR LIVE WITNESS REMAINS VALID**

Mark supplied the current NVIDIA Build Prototype page for:
`nvidia/nemotron-3-super-120b-a12b`.

Current page example shows:
- base URL: `https://integrate.api.nvidia.com/v1`;
- model: `nvidia/nemotron-3-super-120b-a12b`;
- `temperature=0.5`;
- `top_p=1`;
- `max_tokens=1024` in the example.

Earlier COM wording described `temperature=1.0 / top_p=0.95` as current owner guidance. That wording is now stale/overstated.

The prior live EvidenceWatch probe remains a valid interoperability witness because:
- it reached the real NVIDIA endpoint;
- the selected model responded;
- structured output parsed;
- the call ended `NVIDIA_PROBE_OK`.

It does **not** prove one sampling configuration is semantically preferable.

EvidenceWatch branch was updated to mirror the current Prototype page's visible sampling shape:
`temperature=0.5 / top_p=1`.

No change to the provider-witness conclusion.

```text
OLD SAMPLING CLAIM = CORRECTED
LIVE PROVIDER INTEROP WITNESS = STILL PASS
```
