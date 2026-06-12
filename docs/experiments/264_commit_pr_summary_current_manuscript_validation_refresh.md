# Experiment 264: Commit/PR Summary Current Manuscript Validation Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 730 made
manuscript validation current.

## 731: Commit/PR Summary Current Manuscript Validation Refresh

Output:

```text
outputs/experiments/731_commit_pr_summary_current_manuscript_validation_refresh
```

Command:

```text
Update the commit/PR summary from run 727 so it records run 730 as the current
manuscript validation checkpoint and run 729 as the current state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_manuscript_validation_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
inventory status: inventory_ready
manuscript validation pointer: run 730
git diff --check: clean after run 731
```

## Interpretation

The current commit-preparation artifact is now run 731. It supersedes run 727
for commit planning while preserving run 726 as local validation, run 718 as
code self-review, run 729 as state audit, run 722 as archive coverage audit,
run 730 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so manuscript validation points to run 730 and
commit preparation points to run 731.
