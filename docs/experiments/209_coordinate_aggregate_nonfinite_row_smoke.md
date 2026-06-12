# Experiment 209: Coordinate Aggregate Non-Finite Row Smoke

## Purpose

Validate the coordinate aggregate row-sanitization hardening through the real
coordinate confidence aggregate CLI.

## 676: Coordinate Aggregate Non-Finite Row Smoke

Output:

```text
outputs/experiments/676_coordinate_aggregate_nonfinite_row_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_confidence_aggregate.py outputs/experiments/676_coordinate_aggregate_nonfinite_row_smoke/input_summary_nonfinite_rows.json --outdir outputs/experiments/676_coordinate_aggregate_nonfinite_row_smoke --run-name coordinate_aggregate_nonfinite_row_smoke
```

Artifacts:

```text
README.md
input_summary_nonfinite_rows.json
data/coordinate_confidence_aggregate.csv
data/coordinate_confidence_aggregate.json
data/nonfinite_row_smoke_validation.json
figures/coordinate_confidence_aggregate.png
figures/coordinate_ambiguity_widths.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Validation:

```text
status: pass
invalid JSON/CSV/manifest tokens: 0
output non-finite numeric values: 0
CSV rows: 2
confidence labels: missing=1, strong=1
truth-geometry rows: 1
source summary: {}
acquisition summary: {}
non-finite row optional numeric CSV cells: blank
plots nonblank: true
git diff --check: clean after run 676
```

## Interpretation

Run 676 confirms the real aggregate CLI serializes malformed optional numeric
row values as JSON nulls and blank CSV cells. The valid row remains usable for
truth-geometry counting, while non-finite source/acquisition metadata is not
included in grouped aggregate summaries.

## Next Decision

Refresh the commit-preparation and next-action queue pointers so aggregate CLI
smokes include run 676, then run a small state audit over runs 675-678.

