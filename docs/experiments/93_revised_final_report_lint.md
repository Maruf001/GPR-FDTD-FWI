# Experiment 93: Revised Final Report Lint

## Purpose

Verify the run 559 revised final report after refreshing the reproducibility
section.

## 560: Revised Final Report Lint

Output:

```text
outputs/experiments/560_revised_final_report_lint
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Parse final_report_revised.md, verify run references against outputs/experiments,
verify embedded image paths, and search for TODO/FIXME/TBD/XXX markers.
PY
```

Artifacts:

```text
README.md
data/revised_final_report_lint.json
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

The run 559 revised report is the current manuscript artifact. It preserves the
same claims as run 548 while citing the current validation and archive state.

## Next Decision

Continue manuscript editing, code/docs review, or user-directed handoff.
