# 2026-07-03 190424AA GGAE Aperture Robustness Checkpoint

## What changed

- Promoted the `190424AA_LID10002` rank2 +1 cm right-shift aperture from a one-iteration screen to the same full staged GGAE/IFWI recipe used by the central narrow-aperture run.
- Added `run_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py` and focused tests to summarize central, -1 cm left-shift, and +1 cm right-shift aperture evidence.
- Refreshed the 190424AA GGAE evidence pack and method-validation leaderboard so the aperture-robustness result is visible and source-linked.

## Key numbers

- Central full staged aperture:
  - mean holdout loss: `0.6834719777107239`
  - mean x: `0.13368532061576843 m`
  - mean cover: `0.09367473050951958 m`
- +1 cm right-shift full staged aperture:
  - mean holdout loss: `0.6398650705814362`
  - mean full loss: `0.6401719152927399`
  - mean x: `0.13380017131567 m`
  - mean cover: `0.09385191649198532 m`
- Central vs right-shift validated full span:
  - x span: `0.00011485069990158081 m`
  - cover span: `0.00017718598246574402 m`
- -1 cm left-shift screen:
  - mean holdout loss: `0.9642074108123779`, borderline above the `0.95` provisional threshold.

## Current decision

- Decision label: `external_2025_190424aa_lid10002_ggae_aperture_shift_right_confirmed_left_borderline`.
- Claim boundary: provisional location/cover support for `190424AA_LID10002` rank2 only.
- Do not claim diameter, material/permittivity validation, adjacent-profile transfer, or global-profile prediction.

## Artifacts

- Full +1 cm right-shift even run: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/170_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift`
- Full +1 cm right-shift odd run: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/171_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift`
- Aperture synthesis: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/172_external_2025_190424aa_lid10002_ggae_aperture_robustness_synthesis`
- Final evidence pack: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/174_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_aperture_robustness_final`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Validation and hygiene

- `python -m py_compile run_field_method_validation_leaderboard.py run_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py run_ggae2025_external_2025_190424aa_evidence_pack.py`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py -q` -> `10 passed`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py tests/test_ggae2025_external_2025_190424aa_confirmation_synthesis.py tests/test_ggae2025_external_2025_190424aa_candidate_diagnostic_matrix.py -q` -> `12 passed`
- `git diff --check` -> clean.

## Next defensible task

- Continue the active marathon with a deeper GGAE2025/Fast-GPR-FWI method upgrade on field data, not synthetic:
  - inspect the GGAE/Fast-GPR-FWI implementation against the paper/repo notes;
  - test optimizer/acceleration variants separately from the Jazayeri LBFGS branch;
  - keep the same real-data claim boundary discipline on `190424AA` and other available `data/2025-01-13_GPR_Dataset` profiles.

## Marathon status

- The user-requested marathon remains active. This checkpoint is not a stop condition.
