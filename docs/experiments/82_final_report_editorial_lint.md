# Experiment 82: Final Report Editorial Lint

## Purpose

Lint the final report markdown for missing run references, broken embedded
image paths, and unresolved editing markers.

## 549: Final Report Editorial Lint

Output:

```text
outputs/experiments/549_final_report_editorial_lint
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Parse final_report.md, verify run references against outputs/experiments,
verify embedded image paths, and search for TODO/FIXME/TBD/XXX markers.
PY
```

Artifacts:

```text
final_report_editorial_lint.md
data/final_report_editorial_lint.json
run_manifest.json
```

Result:

```text
status=pass
referenced runs=42
missing runs=0
embedded images=7
broken embedded images=0
unresolved markers=0
```

## Interpretation

The final report markdown passes the lightweight editorial/reproducibility
lint. All run references resolve to existing output folders, all embedded
figures resolve through the run 547 bundle, and no unresolved editing markers
remain.

## Next Decision

Proceed to manuscript editing/formatting or archive-status review. No GPU
experiment is queued.
