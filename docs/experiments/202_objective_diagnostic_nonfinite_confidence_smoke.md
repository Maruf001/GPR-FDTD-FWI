# Experiment 202: Objective Diagnostic Non-Finite Confidence Smoke

## Purpose

Validate the candidate-confidence row-sanitization hardening through the real
objective diagnostic report CLI.

## 669: Objective Diagnostic Non-Finite Confidence Smoke

Output:

```text
outputs/experiments/669_objective_diagnostic_nonfinite_confidence_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py outputs/experiments/669_objective_diagnostic_nonfinite_confidence_smoke/input_summary_nonfinite_confidence.json --outdir outputs/experiments/669_objective_diagnostic_nonfinite_confidence_smoke --run-name objective_diagnostic_nonfinite_confidence_smoke
```

Artifacts:

```text
README.md
input_summary_nonfinite_confidence.json
data/coordinate_objective_diagnostic_ratios.csv
data/coordinate_objective_confidence_rows.csv
data/coordinate_objective_diagnostic_report.json
data/nonfinite_confidence_smoke_validation.json
figures/coordinate_objective_diagnostic_ratios.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Validation:

```text
status: pass
report invalid JSON tokens: 0
report non-finite numeric values: 0
confidence CSV exists: true
manifest has confidence_csv: true
objective confidence rows: 2
ratio rows: 1
non-finite variant confidence label: missing
plot nonblank: true
git diff --check: clean after run 669
```

## Interpretation

Run 669 confirms the real objective diagnostic CLI writes JSON-safe nulls and
blank CSV cells for non-finite objective confidence values. The plot and figure
notes are present, and the CLI manifest correctly declares `confidence_csv`.

## Next Decision

Refresh commit-preparation and next-action queue pointers so objective CLI
smokes include run 669.

