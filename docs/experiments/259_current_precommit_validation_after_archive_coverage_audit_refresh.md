# Experiment 259: Current Precommit Validation After Archive Coverage Audit Refresh

## Purpose

Refresh local validation after the archive-coverage refresh audit/commit/queue
chain through run 725.

## 726: Current Precommit Validation After Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/726_current_precommit_validation_after_archive_coverage_audit_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_archive_coverage_audit_refresh.json
data/git_diff_check.log
data/gpu_snapshot.csv
data/memory_snapshot.txt
data/pytest_q.log
run_manifest.json
```

Validation:

```text
full pytest: 268 passed in 24.43 s
git diff --check: clean
GPU utilization: 1%
RAM available: 101 GiB
```

## Interpretation

Run 726 supersedes run 714 as the current local validation checkpoint. The code
and docs remain clean after the run722-725 archive-coverage audit refresh
chain.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 726.
