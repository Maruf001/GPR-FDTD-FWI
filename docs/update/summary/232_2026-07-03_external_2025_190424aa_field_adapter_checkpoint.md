# External 2025 190424AA Field Adapter Checkpoint

## What changed
- Added a run-ready 190424AA/LID10002 field-window adapter config.
- The adapter packages:
  - real-field x/cover seeds;
  - radius candidates and diameter range;
  - concrete epsr seed/range;
  - fixed/tightly bounded rebar material policy;
  - timing nuisance bounds;
  - explicit guard against using current Fast-GPR as full 3D.
- Added the adapter row to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/275_external_2025_190424aa_field_window_policy_adapter`
- Field profile: `190424AA_LID10002_rank2`
- x seed: `0.13384640216827393 m`
- cover depth seed: `0.093923419713974 m`
- radius candidates: `[0.004, 0.008, 0.012] m`
- diameter range: `8.00-24.00 mm`
- concrete epsr seed: `3.9855180978775024`
- concrete epsr bounds: `3.9718658924102783-3.9855180978775024`
- source delay bounds: `0.15-0.30 ns`
- time shift bounds: `-0.45--0.15 ns`
- Leaderboard evidence score: `1` config-only

## What remains blocked
- This is a config/adapter only.
- It does not run a new field fit.
- It does not produce a new field prediction.

## Current decision
`external_2025_190424aa_field_window_policy_adapter_ready_no_new_fit`

This is the concrete starting packet for the next real field-window optimizer run.

## Next defensible task
Run the first policy-constrained 190424AA field-window optimizer using this config:
- x and cover trainable;
- radius as candidate grid/range, not free unbounded;
- concrete epsr bounded;
- rebar material fixed/tightly bounded;
- source timing as nuisance.

## Validation/resource checks
- `python -m py_compile run_external_2025_190424aa_field_window_policy_adapter.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_190424aa_field_window_policy_adapter.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `34 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Adapter rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/275_external_2025_190424aa_field_window_policy_adapter/data/external_2025_190424aa_field_window_policy_adapter_rows.csv`
- Adapter config: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/275_external_2025_190424aa_field_window_policy_adapter/data/external_2025_190424aa_field_window_policy_adapter_config.json`
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/275_external_2025_190424aa_field_window_policy_adapter/data/external_2025_190424aa_field_window_policy_adapter_summary.json`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue with the policy-constrained field-window optimizer run.
