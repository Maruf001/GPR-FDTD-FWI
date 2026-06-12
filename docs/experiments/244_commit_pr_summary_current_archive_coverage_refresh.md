# Experiment 244: Commit/PR Summary Current Archive Coverage Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 710
recorded current archive coverage without rebuilding the archive.

## 711: Commit/PR Summary Current Archive Coverage Refresh

Output:

```text
outputs/experiments/711_commit_pr_summary_current_archive_coverage_refresh
```

Command:

```text
Update the commit/PR summary from run 707 so it records run 710 as the current
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
git diff --check: clean after run 711
```

## Interpretation

The current commit-preparation artifact is now run 711. It supersedes run 707
for commit planning while preserving run 702 as local validation, run 706 as
code self-review, run 709 as state audit, run 710 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so archive coverage points to run 710 and commit
preparation points to run 711.
