# Experiment 247: Current Precommit Validation After Archive Coverage Refresh

## Purpose

Refresh local validation after the archive-coverage refresh audit/commit/queue
chain through run 713.

## 714: Current Precommit Validation After Archive Coverage Refresh

Output:

```text
outputs/experiments/714_current_precommit_validation_after_archive_coverage_refresh
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
git diff --check
```

Artifacts:

```text
README.md
data/current_precommit_validation_after_archive_coverage_refresh.json
data/git_diff_check.log
data/gpu_snapshot.csv
data/memory_snapshot.txt
data/pytest_q.log
run_manifest.json
```

Validation:

```text
full pytest: 268 passed in 24.41 s
git diff --check: clean
GPU utilization: 1%
RAM available: 101 GiB
```

## Interpretation

Run 714 supersedes run 702 as the current local validation checkpoint. The code
and docs remain clean after the run710-713 archive-coverage audit refresh
chain.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 714.
