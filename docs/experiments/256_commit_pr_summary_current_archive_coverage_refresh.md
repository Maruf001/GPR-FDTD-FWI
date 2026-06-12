# Experiment 256: Commit/PR Summary Current Archive Coverage Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 722
recorded current archive coverage without rebuilding the archive.

## 723: Commit/PR Summary Current Archive Coverage Refresh

Output:

```text
outputs/experiments/723_commit_pr_summary_current_archive_coverage_refresh
```

Command:

```text
Update the commit/PR summary from run 719 so it records run 722 as the current
archive coverage audit while keeping run 633 as the checksum-valid but stale
external handoff archive.
```

Artifacts:

```text
README.md
commit_pr_summary_current_archive_coverage_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 723
```

## Interpretation

The current commit-preparation artifact is now run 723. It supersedes run 719
for commit planning while preserving run 714 as local validation, run 718 as
code self-review, run 721 as state audit, run 722 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so archive coverage points to run 722 and commit
preparation points to run 723.
