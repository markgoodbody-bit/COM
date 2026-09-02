# Framework Local Steward RC.9 exact-artifact audit

Date: 2026-09-02 UTC  
Receipt: `FW-STEWARD-RC9-AUDIT-20260902-001`

## Object reviewed

```text
file: Framework-Local-Steward-0.1.0-rc.9.zip
bytes: 47,284
zip sha256: 5e3dfae421331e35e0d8b4ab907a366b191b1ef1cc144a9905a5961d3057f57f
src/steward.mjs sha256: 51b0136a616304a5778a6e38e925b6d72c6541009b7ebdb676df13356dc0d0d1
```

The uploaded bytes exactly match the single RC.9 candidate previously reported
by Claude Code. The package manifest verifies. The exact extracted Node suite
passes 15/15, and `src/steward.mjs` and its test module pass Node syntax checks.

## Verdict

```text
HOLD / DO NOT INSTALL RC.9
LIVE RC.8 REMAINS THE PRESERVED SERVICE
```

RC.9's build-identity mechanism is real: the executing server hashes its own
module, publishes that hash through health and bounded status, and the normal
installer path compares the running version and source hash with the packaged
bytes. No outbound-network or command-execution primitive was found in the
server; job execution remains restricted to hashing, verification and exact
receipt scanning.

The package is nevertheless not safe to install as released:

1. The dashboard badge is hard-coded `RC.8` while the module and package report
   `0.1.0-rc.9`.
2. The installer and uninstaller call a scheduled task "owned" after checking
   only its description, executable and arguments. They do not bind the task to
   the current-user principal, limited run level, interactive logon type, exact
   logon trigger, task path or enabled state. A disabled or elevated task with
   matching text/action can therefore be retained by install and removed by
   uninstall.
3. `Register-ScheduledTask -Force` leaves a check/use race in which a task that
   appears after preflight can be overwritten.
4. Public `-NoStart` skips runtime/version/source/PID/ledger checks but still
   reports installation success; on a running upgrade it can stop the service
   without replacing the runtime witness.
5. Existing control-token ACLs are accepted without revalidation. Process
   ownership relies on substring matching of a raw command line. The
   uninstaller does not explicitly force a non-zero terminating refusal.
6. Upgrade file replacement is not transactional. This is disclosed in the
   README, but a post-stop copy/start/health failure can leave the prior service
   stopped or application bytes mixed. No native failed-upgrade recovery witness
   accompanies RC.9.

## Divergent RC.8 caution

Two different artifacts used the RC.8 label. The preserved live service has
source SHA-256 `ef679820...`; the separately reviewed RC.8 donor has source
SHA-256 `ab4a0cfe...`. RC.9 is not a clean delta from that reviewed donor and
uses different ledger-head, mission-currentness and failure-disposition shapes.
Those differences must not be described as newly introduced RC.9 regressions
without the exact live RC.8 source/data model. The live witness already reports a
matched `ledger-head`, consistent with RC.9's installed-line lineage. This
ambiguity reinforces the need for exact build identity; it does not clear RC.9.

## Bounded successor candidates

A distinct `0.1.0-rc.10` candidate was constructed from the exact RC.9 bytes.
It makes only safety/identity repairs:

- dashboard release badge derives from the executing version;
- install and uninstall bind task ownership to the task path, current user,
  limited/interactive principal, exact current-user logon trigger and enabled
  settings, in addition to exact action/description;
- task registration no longer uses `-Force` and is re-read and verified;
- existing token ACLs must be protected and grant allow access only to the
  current Windows identity;
- process matching is end-anchored to the exact server argument;
- uninstall refusals explicitly exit non-zero;
- `-NoStart` cannot stop a running upgrade and its clean-install output is
  explicitly staged/unwitnessed;
- `-AuditOnly` performs a read-only native preflight over package tests, token,
  markers, persistence, live process/listener, health identity and ledger.

RC.10's manifest verified and its Node suite passed 15/15. Its native
`-AuditOnly` execution also parsed and ran the full suite, then correctly made no
installed-state mutation. It refused because live RC.8 does not yet publish the
`source_sha256` field introduced by RC.9. That refusal exposed an audit-design
error: the pre-upgrade audit required the old service to possess the capability
being introduced by the upgrade.

```text
candidate: Framework-Local-Steward-0.1.0-rc.10-CANDIDATE.zip
bytes: 49,725
zip sha256: 9005f896c38b15bc35fd82203f3b96168ea277ce130b043552d77b37b550ff66
src sha256: 8fa942ac37ffa04c7e5ac23b789200384ae4ddd3559e20f2079dad69f1c89d53
```

RC.11 supersedes RC.10 without weakening post-upgrade identity. For a legacy
service that lacks self-reported source identity, read-only audit hashes the
exact installed server file and binds its path to the verified Node process and
sole loopback listener, explicitly labelling the result
`LEGACY_ON_DISK_ONLY`. If a service does report a source hash, RC.11 requires
health, status and the installed file to match. A normal RC.11 installation must
still restart and self-report the exact packaged source hash before success.

```text
candidate: Framework-Local-Steward-0.1.0-rc.11-CANDIDATE.zip
bytes: 50,178
zip sha256: f95f23246be17623c1ecf4063f544b0b45543bc7d5cd9a0ffebf9376ea5627d6
src sha256: e4efba655e82ca3fc781b1da6c7a35caf1888f67018dc7423254c531ce565cba
manifest: 8/8 PASS
Node suite: 15/15 PASS
gate: READ-ONLY NATIVE AUDIT ONLY / NOT INSTALL APPROVAL
```

No install, service stop, external post, provider spend or Square actuation
occurred while producing this audit.

## RC.11 native upgrade result

The operator ran RC.11 `-AuditOnly` first. It returned
`PASS_NO_MUTATION`, confirmed the protected current-user token ACL and exact
scheduled task, bound the sole port-4318 listener to live PID 43432, reported a
locally consistent 37-entry ledger, and identified the legacy on-disk RC.8
source as `ef679820eba2c963890a48efeaf4361860dbf57eac357651595644fa571e9b06`.

Before upgrade, the operator verified the RC.11 ZIP SHA-256 and copied the full
RC.8 application directory to a timestamped Downloads backup. The normal RC.11
installer then returned:

```text
FRAMEWORK STEWARD RUNNING UPGRADE WITNESS: PASS
Upgrade: 0.1.0-rc.8 -> 0.1.0-rc.11
Ledger: 37 -> 38 events
Receipt: Framework-Steward-Upgrade-Witness-20260902T125357Z.json
Receipt SHA-256: a3b78573868c20da077d993bffc7bbd15a161cbcc54e015e4e5f7d0b83c3116a
```

This establishes successful package tests on Windows, owned-service stop and
replacement, exact RC.11 version/source self-identification, preserved install
identity, scheduled-task start, and retained-ledger advancement. The receipt
facts above are witnessed from the operator transcript; the receipt JSON bytes
have not been independently ingested.

At this point it did not establish actual relaunch at the next Windows sign-in,
externally anchored ledger completeness, transactional failed-upgrade rollback,
uninstall, or Unicode-profile behavior. The later witness below closes the first
item for one natural restart only. RC.8 application backup remains preserved.


## RC.11 natural Windows restart witness

After a normal user-initiated Windows restart, the operator ran the frozen
read-only persistence check. It returned `PASS_AFTER_RESTART`:

```text
boot: 2026-09-02T18:23:46.5+01:00
scheduled-task last run: 2026-09-02T18:23:57+01:00
service process start: 2026-09-02T18:24:04.7099091+01:00
version: 0.1.0-rc.11
PID: 17748
task state: 4 / RUNNING
task result: 267009 / 0x41301 / TASK_RUNNING
source matches installed bytes: true
ledger_ok: true
ledger entries: 43
head_state: MATCHED
```

The scheduled task and service process both started after the recorded operating
system boot. The running module reported the same SHA-256 as the installed
`src/steward.mjs`, and the internally consistent ledger advanced from 38 to 43
entries. This establishes one actual natural restart relaunch of the exact RC.11
build. It does not establish universal future persistence, transactional
failed-upgrade rollback, uninstall behavior, external ledger anchoring or every
Windows policy/profile environment.
