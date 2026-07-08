# GSSI 51600S Predictor Compatibility Checkpoint

## What changed

- Ran fresh GSSI DZT QC under the `gpr-fdtd-fwi` conda environment because `readgssi` is not available in the base environment.
- Added `run_gssi51600s_predictor_compatibility_report.py`.
- The compatibility report compares the current GSSI 51600S DZT data against the promoted 0701 predictor product report and refined optimizer window.

## Key numbers

- Fresh GSSI QC artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/002_gssi51600s_current_dzt_qc_for_predictor_compatibility`
- Compatibility report artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/003_gssi51600s_predictor_compatibility_report`
- DZT files decoded: `4`
- profile/channel records: `4`
- antenna: `51600S`
- readgssi version: `0.0.22`
- samples per profile: `510`
- trace count range: `274-814`
- time range: `5.0 ns`
- dielectric metadata value: `2.25`
- depth range from metadata/time: `0.499654 m`
- scan spacing: `0.003333 m`
- profile length range: `0.909909-2.709729 m`
- sidecar warnings: none

Compatibility against current 0701 predictor:

- 0701 candidate z/depth: `1.507637 m`
- 0701 local target window: `15.625-21.625 ns`
- GSSI max depth: `0.499654 m`
- GSSI max time: `5.0 ns`
- direct 0701 candidate reuse: `False`

## Current decision

The GSSI files are decoded and QC-ready, but the current 0701 predictor candidate cannot be reused directly. A GSSI-specific shallow-window adapter is required before fitting geometry/material predictions on this data.

## What remains blocked

- No normalized predictor stack exists yet for the GSSI DZT records.
- No GSSI-specific candidate x-window detector has been run.
- No GSSI-specific time/polarity ladder or Fast-GPR shallow-window optimizer has been run.
- The current GSSI data has only `0-5 ns` acquisition range; the 0701 late/deep window is out of range.

## Validation/resource checks

- `conda run -n gpr-fdtd-fwi python run_gssi_dzt_qc.py ...` decoded all four DZT records and wrote QC figures.
- GSSI QC figures are nonblank:
  - four B-scan QC figures: `2312 x 903`, RGBA
  - field context figure: `2144 x 937`, RGBA
  - inventory figure: `2059 x 835`, RGBA
- `python -m py_compile run_gssi51600s_predictor_compatibility_report.py tests/test_gssi51600s_predictor_compatibility_report.py`
- `python -m pytest tests/test_gssi51600s_predictor_compatibility_report.py -q` -> `3 passed`
- Product-report plus compatibility tests -> `5 passed`
- Compatibility figure is nonblank, `1923 x 767`, RGBA, full channel extrema.
- `git diff --check` on compatibility/report files was clean.

## Artifact paths

- GSSI QC summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/002_gssi51600s_current_dzt_qc_for_predictor_compatibility/data/gssi_dzt_qc_summary.json`
- GSSI QC inventory: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/002_gssi51600s_current_dzt_qc_for_predictor_compatibility/data/gssi_dzt_inventory.csv`
- Compatibility summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/003_gssi51600s_predictor_compatibility_report/data/gssi51600s_predictor_compatibility_report_summary.json`
- Compatibility rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/003_gssi51600s_predictor_compatibility_report/data/gssi51600s_predictor_compatibility_rows.csv`
- Compatibility figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/003_gssi51600s_predictor_compatibility_report/figures/gssi51600s_predictor_compatibility_report.png`

## Next defensible task

Build the GSSI normalized predictor stack/manifest adapter:

- read each DZT profile with `readgssi`
- background-remove and normalize amplitudes
- crop/pad/resample profiles to a consistent stack
- save `.npz` stack plus manifest rows with `dt_ns`, `scan_spacing_m`, profile length, trace count, and source file
- then run a shallow candidate detector/time-window selection on that stack

## Marathon status

The requested 20-hour local marathon is still active. Continue with the GSSI stack adapter and shallow-window path rather than stopping at this checkpoint.
