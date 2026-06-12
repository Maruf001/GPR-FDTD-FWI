# Experiment 200: Commit/PR Summary Candidate Row-Sanitization Audit Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 666
current candidate row-sanitization state audit.

## 667: Commit/PR Summary Candidate Row-Sanitization Audit Refresh

Output:

```text
outputs/experiments/667_commit_pr_summary_candidate_row_sanitization_audit_refresh
```

Command:

```text
Update the commit/PR summary from run 664 so it records run 666 as the current
state audit and docs/experiments/55-200.
```

Artifacts:

```text
README.md
commit_pr_summary_candidate_row_sanitization_audit_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 667
```

## Interpretation

The current commit-preparation artifact is now run 667. It supersedes run 664
for review/commit planning while preserving run 633 as the current
checksum-valid but stale packaged archive, run 648 as restart, run 636 as
manuscript validation, run 663 as local validation, run 666 as state audit, and
run 654 as archive coverage audit.

## Next Decision

Refresh the next-action queue so state audit points to run 666 and commit
preparation points to run 667.

