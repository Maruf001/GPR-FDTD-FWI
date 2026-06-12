# Experiment 260: Commit/PR Summary Current Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 726 made
local validation current.

## 727: Commit/PR Summary Current Validation Refresh

Output:

```text
outputs/experiments/727_commit_pr_summary_current_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 723 so it records run 726 as the current
local validation checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 727
```

## Interpretation

The current commit-preparation artifact is now run 727. It supersedes run 723
for commit planning while preserving run 726 as local validation, run 718 as
code self-review, run 725 as state audit, run 722 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so local validation points to run 726 and commit
preparation points to run 727.
