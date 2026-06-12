# Experiment 213: Commit/PR Summary Coordinate Aggregate Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 679
state audit of the coordinate aggregate row-sanitization chain.

## 680: Commit/PR Summary Coordinate Aggregate Audit Refresh

Output:

```text
outputs/experiments/680_commit_pr_summary_coordinate_aggregate_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 677 so it records run 679 as the current
state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_coordinate_aggregate_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 680
```

## Interpretation

The current commit-preparation artifact is now run 680. It supersedes run 677
for review/commit planning while preserving run 675 as local validation, run
676 as aggregate non-finite row CLI smoke, run 679 as state audit, run 654 as
archive coverage audit, and run 648 as restart.

## Next Decision

Refresh the next-action queue so state audit points to run 679 and commit
preparation points to run 680.

