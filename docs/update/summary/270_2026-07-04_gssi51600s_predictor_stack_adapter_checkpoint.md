# GSSI 51600S Predictor Stack Adapter Checkpoint

## What changed

- Added `run_gssi51600s_predictor_stack_adapter.py`.
- The adapter reads the GSSI DZT profiles with `readgssi`, removes median background per time sample, robust-normalizes signed amplitudes, saves absolute amplitudes, and crops all profiles to a common trace aperture.
- Generated a predictor-ready GSSI stack/manifest artifact.

## Key numbers

- Stack adapter artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter`
- Stack NPZ: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/data/gssi51600s_predictor_stack.npz`
- Manifest rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/data/gssi51600s_predictor_stack_manifest_rows.csv`
- Stack shape: `4 x 510 x 274` as profile x sample x trace
- Saved arrays: `signed_stack`, `abs_stack`
- dt: `0.0098231827 ns`
- scan spacing dx: `0.003333 m`
- common cropped profile length: `0.909909 m`
- time range: `5.0 ns`
- depth range from metadata: `0.499654 m`
- dielectric metadata: `2.25`
- original trace counts: `807`, `274`, `814`, `274`
- cropped common trace count: `274`
- signed amplitude range: `[-1, 1]`
- abs-stack p99: `1.0`

## Current decision

The GSSI 51600S data is now in a predictor-compatible stack format for shallow-window detection. The stack is intentionally cropped to the shortest profile aperture so all four profiles share one regular x grid.

## What remains blocked

- Cropping to the shortest aperture discards the long-profile tail from files `013` and `015`; a later full-aperture detector should handle variable-length profiles or padding/masking.
- No GSSI-specific shallow event detector has been run yet.
- No GSSI-specific time/polarity ladder or Fast-GPR optimizer has been run yet.
- This adapter does not infer rebar geometry; it only prepares the data.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_predictor_stack_adapter.py tests/test_gssi51600s_predictor_stack_adapter.py`
- `python -m pytest tests/test_gssi51600s_predictor_stack_adapter.py -q` -> `4 passed`
- Stack plus compatibility tests -> `7 passed`
- `conda run -n gpr-fdtd-fwi python run_gssi51600s_predictor_stack_adapter.py ...` completed with four decoded DZT records.
- Stack preview figure is nonblank, `1889 x 1311`, RGBA, full channel extrema.
- `git diff --check` on GSSI adapter/compatibility files was clean.
- Script snapshots were frozen under `004_gssi51600s_predictor_stack_adapter/scripts/`.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/data/gssi51600s_predictor_stack_adapter_summary.json`
- Stack NPZ: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/data/gssi51600s_predictor_stack.npz`
- Manifest rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/data/gssi51600s_predictor_stack_manifest_rows.csv`
- Preview figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/004_gssi51600s_predictor_stack_adapter/figures/gssi51600s_predictor_stack_preview.png`

## Next defensible task

Run a shallow event/candidate detector on the GSSI stack to propose x/time windows inside `0-5 ns`. This should produce candidate x positions, time/depth estimates under epsr metadata, profile support, and target windows for a GSSI-specific Fast-GPR ladder/optimizer.

## Marathon status

The requested 20-hour local marathon is still active. Continue with GSSI shallow candidate detection rather than stopping at this checkpoint.
