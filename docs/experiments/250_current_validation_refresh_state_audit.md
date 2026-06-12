# Experiment 250: Current Validation Refresh State Audit

## Purpose

Audit the validation/commit/queue refresh chain after runs 714-716.

## 717: Current Validation Refresh State Audit

Output:

```text
outputs/experiments/717_current_validation_refresh_state_audit
```

Command:

```text
Audit runs 714-716 for manifest, declared artifact, docs tracker, symlink,
validation, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_validation_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 714 validation status: pass
run 714 pytest passed: 268
run 714 git diff check status: clean
run 715 inventory status: inventory_ready
run 716 queue pointer checks: 15/15
run 715 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 717
```

## Interpretation

Runs 714-716 are internally consistent. The current queue points local
validation to run 714 and commit preparation to run 715 while preserving run
706 code self-review, run 710 archive coverage, and run 633 as the
checksum-valid but stale handoff archive.

## Next Decision

Use run 715 for commit preparation. Rebuild the external archive only if
handoff packaging is requested.
