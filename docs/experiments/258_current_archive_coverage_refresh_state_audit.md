# Experiment 258: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage/commit/queue refresh chain after runs 722-724.

## 725: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/725_current_archive_coverage_refresh_state_audit
```

Command:

```text
Audit runs 722-724 for manifest, declared artifact, docs tracker, symlink,
archive coverage, inventory, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_archive_coverage_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 722 archive audit status: pass
run 722 archive checksum match: true
run 723 inventory status: inventory_ready
run 724 queue pointer checks: 15/15
run 723 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 725
```

## Interpretation

Runs 722-724 are internally consistent. The current queue points archive
coverage to run 722 and commit preparation to run 723 while preserving run 714
local validation, run 718 code self-review, and run 633 as the checksum-valid
but stale handoff archive.

## Next Decision

Use run 723 for commit preparation, or refresh local validation if a newer
full-suite timestamp is needed.
