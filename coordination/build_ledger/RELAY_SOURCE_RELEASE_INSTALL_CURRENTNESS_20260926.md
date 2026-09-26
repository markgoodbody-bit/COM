# Campfire Relay — source / release / installed-version currentness repair

Date: 26 September 2026

Status: **MERGED TO RELAY MAIN / DOCUMENTATION + COORDINATION ONLY / INSTALLED RUNTIME STILL UNKNOWN**

Trigger:
Relay `main` still stated that the active Windows Production installation "remains v0.18.2.1" and called that the immediate installed rollback source. That statement depended on historical host evidence and had outlived its observation window.

Freshly rechecked source facts before repair:
- Relay main before candidate: `4e7bdf95fee04638fe5b5ae84147f97c39a84d72`;
- `package.json.version = 0.18.34`;
- annotated tag `campfire-production-v0.18.34` dereferences to commit `15b51dd484acc4f12dc979cc7d791e12efd6c597`;
- latest published GitHub Release listing returned `campfire-production-v0.18.33`, published 6 August 2026;
- current installed Windows runtime and usable rollback build were **not freshly observed by this aperture**.

Repair:
- Relay PR #261;
- reviewed head `904ccf6806c8dac44cfeff235a9cb479458fad93`;
- `README.md` now separates repository source, production-named tag, published GitHub Release and installed runtime;
- `coordination/STATUS.md` stops presenting historical v0.18.2.1 installation evidence as current inventory;
- `coordination/WORKSTREAMS.md` labels its older branch detail as historical unless reverified.

Hosted review:
- exact-head `campfire-ci` `36236885881 / SUCCESS`;
- post-merge `campfire-ci` `36236969264 / SUCCESS`.

Merged Relay main:
`73cfcbd4d583e575fc36f604f30448b1532bed81`

Stale PR #215 is closed unmerged as superseded by #261.

Preserve:

```text
REPOSITORY SOURCE != INSTALLED RUNTIME
PRODUCTION-NAMED TAG != LIVE INSTALLATION
LATEST GITHUB RELEASE != INSTALLED VERSION
PACKAGE VERSION != ACTIVATION
HISTORICAL HOST RECEIPT != CURRENT INVENTORY
UNKNOWN INSTALLED VERSION != BROKEN INSTALLATION
```

Non-changes:
- no `package.json` mutation;
- no tag/release creation or deletion;
- no installer/service/watchdog mutation;
- no host restart;
- no credential/provider use;
- no Production activation.

Related maintained Simple-v1 branch remains separate:
`framework/campfire-square-simple-v1@f4fa18220957acb00a1ed938432043edb2e27837`

Its unattended MODEL operation from #258 is reverted by #259 and must not be reported as current capability.
