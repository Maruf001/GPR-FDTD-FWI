# External 2025 Field-Facing 3D Policy Checkpoint

## What changed
- Added a field-facing 3D inversion policy artifact.
- Synthesized current evidence from:
  - real 190424AA radius/epsr candidate artifact `260`;
  - Fast-GPR true-3D blocked smoke artifact `267`;
  - JAX scalar fixed-material recovery artifact `273`.
- Added the policy to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/274_external_2025_field_facing_3d_inversion_policy`
- Policy rows: `10`
- Current real-field top diameter candidate: `16.0 mm`
- Current real-field diameter range: `7.999999523162842 to 24.0 mm`
- Current real-field top concrete/background epsr candidate: `3.9855180978775024`
- Current epsr range: `3.9718658924102783 to 3.9855180978775024`
- Fast-GPR full-3D status: `forward_smoke_not_full_3d`
- Leaderboard evidence score: `1` policy/candidate-range only

## What remains blocked
- This does not create a new field prediction.
- Full 3D field inversion remains blocked until the forward engine is true-z-coupled and Maxwell-complete enough for the claim.
- Diameter remains a bounded candidate range, not a unique field-identified value.

## Current decision
`external_2025_field_facing_3d_policy_ready_no_3d_field_claim`

Use this policy for the next real-data implementation:
- fit/refine x and cover depth from field windows;
- keep diameter as a bounded candidate range;
- fix or tightly bound rebar material/radius first;
- invert/report concrete epsr as best plus range;
- do not use current Fast-GPR code as full 3D.

## Next defensible task
Build the first field-window adapter that applies this policy to the 190424AA/LID10002 event: fixed/tightly bounded rebar material, diameter candidate range, concrete epsr candidate/range, and source timing as nuisance.

## Validation/resource checks
- `python -m py_compile run_external_2025_field_facing_3d_inversion_policy.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_field_facing_3d_inversion_policy.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `33 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/274_external_2025_field_facing_3d_inversion_policy/data/external_2025_field_facing_3d_inversion_policy_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/274_external_2025_field_facing_3d_inversion_policy/data/external_2025_field_facing_3d_inversion_policy_rows.csv`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue with the field-window adapter that applies this policy.
