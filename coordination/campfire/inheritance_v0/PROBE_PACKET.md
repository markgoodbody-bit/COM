# Inheritance Capsule v0 — probe packet status

Status: **INVALIDATED / DO NOT USE FOR MODEL CONSUMPTION**

The previously frozen reader-output and whole-packet hashes were generated before Codex review exposed parser/rendering defects and before the current repair.

Those hashes are therefore stale and are intentionally not repeated here as current evidence.

Do not provide the prior packet to any model.

A new probe packet may be frozen only after:
1. the exact repaired parser/test head is rerun successfully;
2. review confirms the read boundary has no blocking defect;
3. the adversarial capsule is re-read by that exact code;
4. the exact reader-output bytes are preserved;
5. fresh reader-output and whole-packet SHA-256 hashes are computed.

The model-level probe remains UNRUN.

`OLD PACKET != CURRENT READER OUTPUT`  
`FROZEN != VALID AFTER READER CHANGE`
