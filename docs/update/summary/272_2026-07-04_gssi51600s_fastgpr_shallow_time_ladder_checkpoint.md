# GSSI 51600S Fast-GPR Shallow Time Ladder Checkpoint

## What changed

- Added `run_gssi51600s_fastgpr_shallow_time_ladder.py`.
- The ladder uses the GSSI predictor stack, the GSSI detector top x seed, GSSI dt/dx metadata, and a shallow Fast-GPR window within `0-5 ns`.
- Ran the Fast-GPR time/polarity ladder around the GSSI detector top candidate.

## Key numbers

- Ladder artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/006_gssi51600s_fastgpr_shallow_time_ladder`
- GSSI detector top x: `0.703263 m`
- detector top time: `1.051081 ns`
- detector top depth under epsr metadata: `0.105035 m`
- observed field window shape: `4 x 41 x 8`
- Fast-GPR result shape: `4 x 41 x 8`
- GSSI epsr metadata: `2.25`
- GSSI field dt: `0.009823 ns`
- Fast-GPR dt: `0.1 ns`
- shallow target window: `0.098232-4.098232 ns`
- trace stride: `15`
- effective dx: `0.049995 m`
- trace window: `159-264`
- best shift: `0` samples = `0.0 ns`
- best polarity: `-1`
- best loss: `0.666402`
- positive-polarity zero-shift baseline loss: `0.720122`
- improvement vs baseline: `0.053720`
- relative improvement vs baseline: `0.074599`
- fixed overlap: `21` time samples

## Current decision

The GSSI shallow Fast-GPR objective now has a fitted nuisance alignment: polarity `-1`, shift `0`. This is the correct input to the first GSSI-specific shallow geometry/material optimizer.

## What remains blocked

- Prediction amplitude is very small before standardization (`prediction_abs_max ~= 8.33e-5`), so optimizer claims should stay normalized-objective scoped.
- No GSSI-specific geometry/material optimizer has been run yet.
- No final GSSI x/z/radius/epsr/conductivity product report exists yet.
- The current GSSI path still uses a cropped common aperture; full long-profile tails remain unscanned.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_fastgpr_shallow_time_ladder.py tests/test_gssi51600s_fastgpr_shallow_time_ladder.py`
- `python -m pytest tests/test_gssi51600s_fastgpr_shallow_time_ladder.py -q` -> `2 passed`
- Ladder plus shallow-detector tests -> `7 passed`
- Ladder figure is nonblank, `1481 x 835`, RGBA, full channel extrema.
- `git diff --check` on ladder/detector files was clean.
- Script snapshots were frozen under `006_gssi51600s_fastgpr_shallow_time_ladder/scripts/`.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/006_gssi51600s_fastgpr_shallow_time_ladder/data/gssi51600s_fastgpr_shallow_time_ladder_summary.json`
- Rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/006_gssi51600s_fastgpr_shallow_time_ladder/data/gssi51600s_fastgpr_shallow_time_ladder_rows.csv`
- Arrays: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/006_gssi51600s_fastgpr_shallow_time_ladder/data/gssi51600s_fastgpr_shallow_time_ladder_arrays.npz`
- Figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/006_gssi51600s_fastgpr_shallow_time_ladder/figures/gssi51600s_fastgpr_shallow_time_ladder.png`

## Next defensible task

Run a GSSI-specific shallow geometry/material optimizer using:

- x window from detector top: `0.703263 m`
- observed window from ladder: profile `0-3`, trace `159-264`, time `0.098-4.098 ns`
- epsr seed: `2.25`
- alignment: polarity `-1`, shift `0`
- shallow depth bounds around the detector depth instead of the 0701 deep bounds

## Marathon status

The requested 20-hour local marathon is still active. Continue with the GSSI shallow optimizer rather than stopping at this checkpoint.
