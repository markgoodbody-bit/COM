# Campfire Relay Simple-v1 — Windows PowerShell payload encoding guard

Date: 27 September 2026

Status: **TEST-ONLY GUARD MERGED / CURRENT PAYLOAD SAFE / INSTALLED RUNTIME UNCHANGED**

## Trigger

The 27 September Simple-v1 reinstall exposed a Windows PowerShell 5.1 carrier defect in the earlier installer path: raw GitHub CLI output had been decoded through the active console code page, producing mojibake in non-ASCII README text.

PR #266 repaired the fetch itself by consuming GitHub Contents API base64 and writing repository bytes directly.

A later hostile review found the remaining latent edge:

- Windows PowerShell 5.1 treats BOM-less script/module source as the active ANSI code page;
- a future non-ASCII byte in a directly written .ps1/.psm1 payload can therefore change parsing even though the repository bytes are correct;
- current installer-shipped PowerShell code is ASCII-safe.

## Guard — Relay PR #270

Candidate head:
b03c2e1086e2486d7111259874adc172b9ca8d7a

The regression derives the shipped .ps1/.psm1 filenames from the installer's own $files list and requires:

- at least one code payload is discovered;
- each named code payload exists in the tracked Simple-v1 source;
- every byte in each installer-shipped .ps1/.psm1 source file is <= 0x7F.

This is deliberately a temporary carrier invariant.

It does **not** claim PowerShell source should always be ASCII. The guard should be replaced when the installer/execution path deliberately guarantees a UTF-8-aware PowerShell carrier, for example through an agreed BOM/encoding strategy or a different runtime contract.

Pre-merge:
- Windows PowerShell run 36320921439 / SUCCESS;
- broad campfire-ci 36320921494 / SUCCESS.

Merge:
e53631d104f1aafb91850e492f51e1ca2377cefa

Post-merge Simple-v1:
36321019856 / SUCCESS

## Boundaries

No worker, supervisor, speech, receipt, authority or installer runtime behaviour changed in #270.

No install or restart was performed.

The installed host was last observed on the older pre-#266 Simple-v1 lineage, so this guard exists in maintained source and is **not** evidence of installed currentness.

    REPOSITORY_BYTES_CORRECT != POWERSHELL_DECODING_CORRECT
    CURRENT_PAYLOAD_ASCII_SAFE != FUTURE_ENCODING_PROBLEM_SOLVED
    TEST_GUARD != RUNTIME_UPDATE
    SOURCE_CURRENT != INSTALLED_CURRENT
