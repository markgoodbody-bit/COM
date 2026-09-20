# THR missing-value reason — cross-domain transfer check

Date: 20 September 2026 — Europe/London

Status: **TRANSFER PRESSURE CONFIRMED / NO ADDITIONAL THR CHANGE**

## Question

Is draft PR #72 merely inheriting a cultural-heritage modelling debate, or does
the action-relevant distinction between reasons for missing values transfer to
other real domains?

## Public owner checks

### UK education statistics

Current Department for Education methodology distinguishes several states that
would be misleading if collapsed into one blank/unknown value, including:
- suppressed for disclosure risk;
- figures unavailable or field not applicable;
- low coverage;
- teacher assessment not provided;
- absent;
- unable to access;
- cheating;
- annulled.

These states have different meanings and downstream treatment.

### CDC healthcare preparedness

CDC's measles assessment material separately exposes:
- Unknown;
- Not assessed;
- Not applicable.

Again, these are not interchangeable.

## Result

The general relation survives cross-domain transfer:

```text
MISSING VALUE != ONE STATE
REASON FOR MISSINGNESS CAN CHANGE NEXT ACTION
```

But this does **not** earn:
- a THR global enum;
- a schema/validator migration;
- adoption of any one domain's vocabulary;
- a claim that the proposed PR #72 list is exhaustive.

PR #72's current documentation-only approach remains appropriately narrow.

```text
TRANSFER SUPPORT != UNIVERSAL TAXONOMY
DOMAIN CODES != THR CODES
```

No external contact.
No record 5.
No additional PR mutation.
