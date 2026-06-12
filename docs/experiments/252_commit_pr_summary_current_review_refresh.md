# Experiment 252: Commit/PR Summary Current Review Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after run 718 made
code self-review current.

## 719: Commit/PR Summary Current Review Refresh

Output:

```text
outputs/experiments/719_commit_pr_summary_current_review_refresh
```

Command:

```text
Update the commit/PR summary from run 715 so it records run 718 as the current
focused code self-review checkpoint.
```

Artifacts:

```text
README.md
commit_pr_summary_current_review_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 719
```

## Interpretation

The current commit-preparation artifact is now run 719. It supersedes run 715
for commit planning while preserving run 714 as local validation, run 718 as
code self-review, run 717 as state audit, run 710 as archive coverage audit,
run 685 as manuscript validation, run 648 as restart, and run 633 as the
checksum-valid but stale archive.

## Next Decision

Refresh the next-action queue so code self-review points to run 718 and commit
preparation points to run 719.
