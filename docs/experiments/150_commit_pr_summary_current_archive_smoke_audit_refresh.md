# Experiment 150: Commit/PR Summary Current Archive Smoke-Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 616
archive refresh.

## 617: Commit/PR Summary Current Archive Smoke-Audit Refresh

Output:

```text
outputs/experiments/617_commit_pr_summary_current_archive_smoke_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 613 so it includes run 616, the current
archive SHA-256, the current 262-test validation state, and docs/experiments
55-150.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_smoke_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 617
```

## Interpretation

The current commit-preparation artifact is now run 617. It supersedes run 613
for review/commit planning while preserving run 616 as the current packaged
archive, run 591 as manuscript validation, run 610 as current local validation,
and run 612 as current state audit.

## Next Decision

Refresh the next-action queue so commit preparation points to run 617 and
archive handoff points to run 616.
