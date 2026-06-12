# Experiment 222: Commit/PR Summary Current Manuscript/Archive Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 688
state audit of the manuscript/archive refresh chain.

## 689: Commit/PR Summary Current Manuscript/Archive Audit Refresh

Output:

```text
outputs/experiments/689_commit_pr_summary_current_manuscript_archive_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 686 so it records run 688 as the current
state audit.
```

Artifacts:

```text
README.md
commit_pr_summary_current_manuscript_archive_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 689
```

## Interpretation

The current commit-preparation artifact is now run 689. It supersedes run 686
for review/commit planning while preserving run 675 as local validation, run
676 as aggregate non-finite row CLI smoke, run 682 as archive coverage audit,
run 685 as manuscript validation, run 688 as state audit, and run 648 as
restart.

## Next Decision

Refresh the next-action queue so state audit points to run 688 and commit
preparation points to run 689.

