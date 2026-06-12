# Experiment 129: Commit/PR Summary Current Archive Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 595
current handoff archive refresh.

## 596: Commit/PR Summary Current Archive Refresh

Output:

```text
outputs/experiments/596_commit_pr_summary_current_archive_refresh
```

Command:

```text
Update the commit/PR summary from run 592 so it includes run 595, the current
archive checksum, and docs/experiments/55-128.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 596
```

## Interpretation

The current commit-preparation artifact is now run 596. It supersedes run 592
for review/commit planning while preserving run 595 as the current packaged
archive.

## Next Decision

Refresh the next-action queue so commit preparation points to run 596 and
optional archive handoff points to run 595.
