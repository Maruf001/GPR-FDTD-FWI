# Experiment 228: Coordinate Aggregate Invalid Default Smoke

## Purpose

Validate run 694 through the real aggregate CLI by checking invalid default
Tx/Rx offsets and a finite valid-default control.

## 695: Coordinate Aggregate Invalid Default Smoke

Output:

```text
outputs/experiments/695_coordinate_aggregate_invalid_default_smoke
```

Commands:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_confidence_aggregate.py outputs/experiments/695_coordinate_aggregate_invalid_default_smoke/input_summary_missing_offset.json --outdir <invalid_outdir> --run-name invalid_default_<value> --default-missing-tx-rx-offset-mm <nan|inf|-1>
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_confidence_aggregate.py outputs/experiments/695_coordinate_aggregate_invalid_default_smoke/input_summary_missing_offset.json --outdir outputs/experiments/695_coordinate_aggregate_invalid_default_smoke/valid_default_control --run-name valid_default_control --default-missing-tx-rx-offset-mm 20.0
```

Artifacts:

```text
README.md
input_summary_missing_offset.json
data/invalid_default_smoke_validation.json
valid_default_control/data/coordinate_confidence_aggregate.csv
valid_default_control/data/coordinate_confidence_aggregate.json
valid_default_control/figures/coordinate_confidence_aggregate.png
valid_default_control/figures/coordinate_ambiguity_widths.png
valid_default_control/figures/FIGURE_NOTES.md
valid_default_control/run_manifest.json
run_manifest.json
```

Validation:

```text
status: pass
invalid defaults rejected: 3/3
invalid output directories created: 0
valid control return code: 0
valid control invalid JSON/CSV/manifest tokens: 0
valid control non-finite output numerics: 0
valid control Tx/Rx offset: 20.0
valid control Tx/Rx source: default_missing
valid control plots nonblank: 2/2
figure notes: true
git diff --check: clean after run 695
```

## Interpretation

The aggregate CLI rejects non-finite or negative default Tx/Rx offsets before
output allocation. A finite default remains usable and is marked as an
inferred `default_missing` value in output rows.

## Next Decision

Refresh commit-preparation and next-action queue pointers so aggregate CLI
smokes include run 695.

