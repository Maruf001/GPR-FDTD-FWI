# Experiment 246: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage/commit/queue refresh chain after runs 710-712.

## 713: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/713_current_archive_coverage_refresh_state_audit
```

Command:

```text
Audit runs 710-712 for manifest, declared artifact, docs tracker, symlink,
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
run 710 archive audit status: pass
run 710 archive checksum match: true
run 711 inventory status: inventory_ready
run 712 queue pointer checks: 15/15
run 711 summary pointer checks: 7/7
planning doc pointer checks: 7/7
git diff --check: clean after run 713
```

## Interpretation

Runs 710-712 are internally consistent. The current queue points archive
coverage to run 710 and commit preparation to run 711 while preserving run 702
local validation, run 706 code self-review, and run 633 as the checksum-valid
but stale handoff archive.

## Next Decision

Use run 711 for commit preparation, or refresh full-suite validation if the
next handoff needs a newer local validation timestamp than run 702.
