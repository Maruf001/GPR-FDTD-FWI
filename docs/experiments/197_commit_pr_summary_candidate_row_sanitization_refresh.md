# Experiment 197: Commit/PR Summary Candidate Row-Sanitization Refresh

## Purpose

Refresh the commit/PR summary and dirty-worktree inventory after the run 663
candidate confidence row-sanitization hardening.

## 664: Commit/PR Summary Candidate Row-Sanitization Refresh

Output:

```text
outputs/experiments/664_commit_pr_summary_candidate_row_sanitization_refresh
```

Command:

```text
Update the commit/PR summary from run 661 so it records run 663 as the current
local validation checkpoint and docs/experiments/55-197.
```

Artifacts:

```text
README.md
commit_pr_summary_candidate_row_sanitization_refresh.md
data/current_commit_inventory.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_commit_inventory.json parses as JSON
git diff --check: clean after run 664
```

## Interpretation

The current commit-preparation artifact is now run 664. It supersedes run 661
for review/commit planning while preserving run 633 as the current
checksum-valid but stale packaged archive, run 648 as restart, run 636 as
manuscript validation, run 663 as local validation, run 660 as state audit, and
run 654 as archive coverage audit.

## Next Decision

Refresh the next-action queue so local validation points to run 663 and commit
preparation points to run 664.

