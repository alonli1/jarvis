# JARVIS Phase F continuation — strict Landlock read isolation for PhysicsIntern role processes

Continue from commit:

```text
d3adf91 docs: record Phase F capsule isolation blocker
```

Current state:

- F01 passed independent oracle validation and remains provisionally imported.
- F02–F05 remain unaccepted.
- PhysicsIntern bootstrap succeeded.
- Honey/plugin isolation succeeded.
- A recovered Codex runtime can execute model calls.
- Process-isolated role dispatch was implemented and smoke-tested.
- The process-isolated role could escape its capsule by reading the F02 parent workspace via `../../../`.
- `bubblewrap` is installed but cannot create user namespaces on this host.
- Do not weaken the scientific isolation requirement merely to make Phase F pass.

Do not redo F01.

The purpose of this continuation is to test one final local containment mechanism: a **strict unprivileged Landlock read allowlist applied outside Codex**, before each role `codex exec` starts.

If strict Landlock containment cannot be proven, stop Phase F locally and record a genuine host-capability blocker.

---

## 1. Why Codex's existing sandbox is insufficient

Do not assume `--sandbox read-only` or Codex's legacy Linux Landlock mode provides input confidentiality.

The current Codex Linux implementation may permit full-filesystem reads while using Landlock primarily to restrict writes. The failed F02 capsule test already demonstrates that cwd/sandbox selection alone is insufficient on this host.

Therefore:

- do not reuse the failed capsule-only assumption;
- do not rely on prompt instructions to prevent reading parent files;
- do not use bubblewrap because user namespaces are unavailable;
- do not modify global kernel settings;
- do not require root.

---

## 2. Probe native Landlock capability directly

Before implementing anything substantial, probe whether the running kernel supports enforceable unprivileged Landlock filesystem restrictions.

Use one or more of:

- an already-installed trustworthy Landlock CLI;
- a tiny direct syscall probe;
- a small program based on the Linux kernel Landlock userspace API.

The probe must be **fail-closed**:
- "unsupported";
- "permission denied";
- "ruleset not enforced";
- partial/no-op enforcement

all count as failure.

Record:
- kernel version;
- detected Landlock ABI;
- whether unprivileged `restrict_self` succeeds;
- the exact probe used.

Do not rely only on `/sys/kernel/security/landlock` existing or not existing.

If native Landlock cannot actually enforce a ruleset, stop and record the blocker. Do not continue with F02.

---

## 3. Prefer an existing auditable Landlock runner

Before writing a new sandbox implementation, check for a suitable already-installed runner such as a Landlock allowlist launcher.

If one is present, inspect its provenance/help/source/package metadata sufficiently to confirm:

- default-deny handled filesystem rights;
- explicit read/read-execute allowlists;
- explicit read-write allowlists;
- restrictions inherited across `exec` and descendants;
- failure if Landlock is unsupported/not enforced.

Do not use a tool that silently falls back to no isolation.

If no suitable runner is installed, build a **minimal Phase-F-only launcher** from a pinned, auditable Landlock implementation or a small direct syscall program.

Do not add a large sandbox framework to Jarvis production code solely for Phase F.

Do not modify upstream PhysicsIntern.

---

## 4. Required Landlock policy

The launcher must handle at minimum the filesystem rights required to deny:

- `READ_FILE`;
- `READ_DIR`;
- `EXECUTE`;

outside explicitly allowed paths.

Also handle relevant newer filesystem rights supported by the detected ABI when needed for correct write confinement, such as:

- `WRITE_FILE`;
- `REMOVE_DIR`;
- `REMOVE_FILE`;
- `MAKE_*`;
- `REFER`;
- `TRUNCATE`;

Use the detected ABI rather than assuming the newest kernel.

The policy must be allowlist-based.

Anything not granted is denied for handled rights.

---

## 5. Build the role filesystem view as an allowlist

For each role dispatch, allow only the minimum required paths.

### Role-specific writable paths

Grant read/write only to:

```text
<ROLE_CAPSULE>/
<ROLE_CODEX_HOME>/   # only if the recovered Codex runtime needs to write there
```

and any tiny dedicated temp directory created specifically for that role:

```text
<ROLE_TMP>/
```

Do not grant `/tmp` wholesale.

### Role-specific readable paths

Grant read access to:

```text
<ROLE_CAPSULE>/
<ROLE_CODEX_HOME>/
```

plus only the system/runtime paths required for the recovered Codex executable to start and make its authenticated model request.

Determine these empirically and minimally.

Likely categories may include:

```text
/recovered/codex/binary/path
/usr/bin or exact required executables
/usr/lib
/lib
/lib64
/etc/ssl
/etc/ca-certificates
/etc/resolv.conf
/etc/hosts
/etc/nsswitch.conf
/dev/null
/dev/urandom
```

but do not blindly grant all of `/etc`, `/home`, `/tmp`, or `/proc`.

Resolve symlinks before constructing grants where appropriate.

If the recovered Codex binary lives under a broader directory containing sensitive user files, prefer copying the executable and required runtime assets into a dedicated Phase-F runtime directory rather than granting that broad parent.

---

## 6. Isolate CODEX_HOME

Each role process must use a dedicated Phase-F Codex home that contains only what the recovered runtime requires.

Do not grant read access to the user's whole:

```text
~/.codex
```

Do not grant:

```text
/home/alonli
```

or the user's home directory generally.

Reuse the already-successful isolated Codex-home strategy from runtime recovery if available.

The role-specific/reusable isolated home may contain only necessary:

- authentication material;
- minimal config;
- freshly compatible model metadata/cache if generated by the recovered runtime.

It must not contain:
- Honey;
- unrelated plugins;
- prior conversation history;
- Jarvis repository files;
- PhysicsIntern oracle files;
- unrelated user data.

Plugins must remain disabled at process level.

---

## 7. Environment hygiene

Before launching a role, sanitize environment variables.

Do not expose environment variables that point to:

- the Jarvis repository;
- the F02 parent workspace;
- oracle/reference directories;
- Honey/plugin locations;
- unrelated credentials.

Keep only variables required for:
- Codex authentication/runtime;
- TLS/network;
- locale;
- dedicated HOME/CODEX_HOME/TMPDIR;
- explicit Phase-F runtime configuration.

Record an allowlisted environment-key manifest, but never log secret values.

---

## 8. Strict pre-scientific isolation test

Before F02 resumes, the Landlock launcher must pass a deliberate adversarial filesystem test.

Create:

```text
<ROLE_CAPSULE>/input/allowed_sentinel.txt
<F02_PARENT>/forbidden_sentinel.txt
<JARVIS_REPO>/forbidden_jarvis_sentinel.txt   # only if safe to create temporarily
```

The sandboxed test process must demonstrate:

### Must succeed
- read `allowed_sentinel.txt`;
- list permitted capsule directories;
- write into role output/temp locations;
- execute the recovered Codex binary and required system tools.

### Must fail with permission denied/inaccessible
- `cat ../../../.../forbidden_sentinel.txt`;
- absolute-path read of F02 parent sentinel;
- absolute-path read of Jarvis sentinel;
- `find`/`ls` on the F02 parent directory;
- opening the user's home generally;
- opening `~/.codex` outside the isolated Phase-F Codex home;
- traversing symlink tricks from capsule to forbidden paths.

Test both:
- direct shell commands under the launcher;
- a plugin-disabled trivial `codex exec` instructed to attempt the same reads.

The Codex model must not be told the contents of forbidden sentinels.

Capture exit codes/stderr.

If **any forbidden read succeeds**, containment fails. Stop. Do not weaken the test.

Remove temporary sentinels afterward if they were newly created.

---

## 9. Descendant inheritance test

The containment must survive process trees.

Under the Landlock launcher verify:

```text
launcher
  -> codex exec
      -> shell/tool subprocess
          -> another subprocess
```

and confirm the deepest descendant still cannot read forbidden files.

Landlock restrictions should be inherited and irreversible for descendants; verify rather than assume.

---

## 10. Do not rely on Codex's internal filesystem sandbox

Once the external Landlock policy is active, Codex's own sandbox may remain enabled as defense in depth, but it is not the confidentiality boundary.

The external Landlock launcher is responsible for denying parent-workspace reads.

Do not configure Codex in a way that requires bubblewrap on this host if that causes execution failure.

Use the already-recovered runtime configuration that works, nested inside the external Landlock boundary.

---

## 11. Preserve PhysicsIntern fresh-context semantics

After containment passes, resume the Phase-F process-isolated dispatcher.

For every Surveyor/Deriver/Computer/Reviewer/Critic/etc. role:

1. create a new staged role capsule;
2. create/use its isolated Codex home/runtime state;
3. apply strict Landlock before `codex exec`;
4. disable plugins/Honey;
5. start a completely fresh Codex session/process;
6. provide only PhysicsIntern-permitted inputs;
7. validate its artifact contract;
8. integrate the result through the coordinator;
9. destroy or archive the capsule according to Phase-F provenance policy.

No role gets access to the parent PhysicsIntern workspace merely because it is on the same machine.

---

## 12. Reviewer independence test

Before accepting F02, specifically verify a reviewer process cannot read:

- Deriver transcript/session files;
- coordinator scratch notes;
- sibling reviewer output;
- private oracle;
- expected answer;
- F01 private evaluator data;
- F02 files not explicitly staged into that review capsule.

Record the review capsule manifest and denied-path test evidence.

---

## 13. Resume F02–F05 only after containment is proven

If all isolation tests pass, resume the preserved F02 case.

Do not redo F01.

Run F02–F05 under the strict Landlock transport and retain the same scientific acceptance conditions:

- PhysicsIntern methodology;
- fresh-context role separation;
- independent review;
- private oracle/reference validation;
- Jarvis provenance/telemetry import.

Do not count the containment smoke tests as scientific cases.

---

## 14. Record the transport accurately

If successful, Phase F must record:

```text
native Codex spawn_agent transport: unusable in this host
capsule-only process isolation: failed confidentiality test
bubblewrap: unavailable due user-namespace restriction
external unprivileged Landlock allowlist: PASS/FAIL
```

If Landlock passes, describe the implementation as a **Phase-F host transport adapter**, not as an upstream PhysicsIntern feature.

---

## 15. Jarvis architectural lesson if successful

Record, but do not prematurely productionize, this requirement:

Fresh-context scientific agents need two separate contracts:

```text
ContextIsolation
FilesystemIsolation
```

A fresh model session is not enough.

Future Jarvis transports should expose verifiable capabilities such as:

```text
fresh_context: bool
read_allowlist_enforced: bool
write_allowlist_enforced: bool
plugin_isolation: bool
network_policy: ...
provenance_capture: bool
```

Scientific orchestration should refuse sensitive independent-review workflows when required capabilities are absent.

---

## 16. True stop condition

If strict unprivileged Landlock cannot be enforced on this host, or if the recovered Codex process cannot operate under a policy strict enough to deny F02/Jarvis reads, then stop Phase F locally.

At that point write/update the blocker stating that F02–F05 require one of:

- a VM/container host with real mount/filesystem isolation;
- a separate Unix account/worker;
- a remote disposable worker;
- a future Codex runtime with enforceable restricted-read sandboxing.

Do not attempt:
- chmod tricks under the same UID;
- cwd-only isolation;
- prompt-only secrecy;
- copying the oracle somewhere "hard to guess";
- manual cache hacks;
- global kernel/security changes;
- root escalation.

F01 remains valid.

Proceed autonomously with the Landlock probe and fail-closed isolation test now.
