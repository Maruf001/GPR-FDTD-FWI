# Experiment 175: Objective Diagnostic No-Confidence Manifest Smoke

## Purpose

Smoke-test the real coordinate objective diagnostic CLI on a summary that has
diagnostic ratio rows but no saved `objective_results`, verifying that the
manifest does not advertise a missing confidence CSV artifact.

## 642: Objective Diagnostic No-Confidence Manifest Smoke

Output:

```text
outputs/experiments/642_objective_diagnostic_no_confidence_manifest_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py \
  outputs/experiments/642_objective_diagnostic_no_confidence_manifest_smoke/input_summary_no_confidence.json \
  --outdir outputs/experiments/642_objective_diagnostic_no_confidence_manifest_smoke \
  --run-name objective_diagnostic_no_confidence_manifest_smoke
```

Artifacts:

```text
README.md
input_summary_no_confidence.json
data/coordinate_objective_diagnostic_ratios.csv
data/coordinate_objective_diagnostic_report.json
data/no_confidence_manifest_smoke_validation.json
figures/coordinate_objective_diagnostic_ratios.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Validation:

```text
manifest has confidence_csv: false
confidence CSV exists: false
objective_confidence is null: true
objective confidence rows: 0
ratio rows: 1
report non-finite numeric count: 0
figure notes exist: true
plot size: 2059 x 1005
plot nonblank: true
git diff --check: clean after run 642
```

## Interpretation

The run 639 manifest hardening works in the real CLI path. A report with no
objective confidence rows still emits the ratio CSV, JSON, plot, and figure
notes, but it does not declare or create a confidence CSV.

## Next Decision

Refresh commit-preparation and next-action queue pointers so the manifest smoke
is available alongside the run 639 full-suite validation.
