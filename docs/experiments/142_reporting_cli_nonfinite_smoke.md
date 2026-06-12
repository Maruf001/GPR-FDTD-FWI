# Experiment 142: Reporting CLI Non-Finite Smoke

## Purpose

Exercise the hardened coordinate confidence aggregate CLI end-to-end on
malformed and non-finite optional numeric fields.

## 609: Reporting CLI Non-Finite Smoke

Output:

```text
outputs/experiments/609_reporting_cli_nonfinite_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_confidence_aggregate.py outputs/experiments/609_reporting_cli_nonfinite_smoke/data/nonfinite_confidence_input.json --outdir outputs/experiments/609_reporting_cli_nonfinite_smoke
```

Artifacts:

```text
README.md
data/nonfinite_confidence_input.json
data/coordinate_confidence_aggregate.csv
data/coordinate_confidence_aggregate.json
data/reporting_cli_nonfinite_smoke_validation.json
figures/coordinate_confidence_aggregate.png
figures/coordinate_ambiguity_widths.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Validation:

```text
CLI exit code: 0
generated run_manifest.json parses as JSON
generated coordinate_confidence_aggregate.json parses as JSON
aggregate non-finite numeric count: 0
PNG dimensions: 1719 x 971 for both figures
PNG extrema span 0-255 for RGB channels
git diff --check: clean after run 609
```

## Interpretation

The aggregate CLI now survives malformed optional values through CSV, JSON,
plot generation, and figure-note writing. Raw rows preserve input strings, but
aggregate statistics and acquisition labels use sanitized missing-value
behavior.

## Next Decision

Optionally smoke the objective diagnostic CLI with sparse/non-finite inputs, or
refresh the current state audit after the new smoke run.
