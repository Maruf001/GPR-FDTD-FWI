# External 2025 GGAE Profile Outcome Runtime Checkpoint

Date: 2026-07-03

## Scope

This checkpoint updates the external 2025 GGAE profile outcome synthesis to include runtime and objective-evaluation speed. The goal is to keep accuracy and speed in the same field-method artifact.

## Updated Artifact

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/223_external_2025_ggae_profile_outcome_synthesis`

Decision:

- `external_2025_ggae_profile_outcomes_three_provisional_one_failed_diameter_not_claimed`

## Runtime Summary

- Total paired-profile runtime: `67.64161482779309 s`
- Total objective evaluations: `160`
- Median provisional holdout: `0.7661208808422089`

Profile speed rows:

- `190424AA_LID10002_rank2_right_shift`: holdout `0.6064098179340363`, runtime `16.53725339192897 s`, eval/s `2.418781344882945`
- `LS1_LID10001_rank2`: holdout `0.7661208808422089`, runtime `16.34898333181627 s`, eval/s `2.4466353159806085`
- `LS1_LID10002`: holdout `0.8706095814704895`, runtime `18.925224913051352 s`, eval/s `2.1135812220870838`
- `LDH1_LID10001_rank2`: holdout `1.6379399299621582`, runtime `15.830153190996498 s`, eval/s `2.5268233047011988`

## Claim Boundary

Runtime evidence does not change the claim boundary: three profiles are provisional event-window location/cover only; LDH1 is failed; diameter and material properties are not claimed.

## Verification

- `python -m py_compile run_ggae2025_external_2025_profile_outcome_synthesis.py`
- `python -m pytest tests/test_ggae2025_external_2025_profile_outcome_synthesis.py -q`
- `python run_ggae2025_external_2025_profile_outcome_synthesis.py`
- `git diff --check`

## Next Step

Use the speed-normalized outcome table for the next method decision: either test one new independent external profile/candidate or focus on reducing the runtime per profile while keeping the same holdout split and claim boundary.
