# Field Experiment 071: Time-Zero Perturbation Sensitivity

Date: 2026-06-18

## Purpose

Test whether the short 014/016 B-scan QC remains supported when the relative
time-zero correction is perturbed across the uncertainty envelope from run 075.
This is a CPU-only field-QC stress test; it does not launch FDTD, FWI, GPU
kernels, 3D inversion, radius recovery, or cover-depth recovery.

## Outputs

```text
078_gssi51600s_field_time_zero_perturbation_sensitivity
079_gssi51600s_field_publication_claim_bundle_post_time_zero_perturbation
080_gssi51600s_field_dataset_policy_synthesis_post_time_zero_perturbation
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/078_gssi51600s_field_time_zero_perturbation_sensitivity/data/field_time_zero_perturbation_windows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/078_gssi51600s_field_time_zero_perturbation_sensitivity/data/field_time_zero_perturbation_sensitivity_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/078_gssi51600s_field_time_zero_perturbation_sensitivity/figures/field_time_zero_perturbation_sensitivity.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/079_gssi51600s_field_publication_claim_bundle_post_time_zero_perturbation/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/080_gssi51600s_field_dataset_policy_synthesis_post_time_zero_perturbation/data/field_dataset_policy_summary.json
```

## Result

Run 078 evaluates seven offsets across three shallow B-scan windows:

```text
policy label:                         field_time_zero_ci_perturbation_stack_robust
offset count:                         7
window count:                         3
window rows:                          21
supported rows:                       18
raw/no-correction supported rows:     0
nominal supported rows:               3 / 3
bootstrap-CI supported rows:          9 / 9
conservative-envelope supported rows: 6 / 6
minimum nonraw matrix improvement:    0.125152
minimum nonraw corrected abs corr:    0.661316
minimum nonraw improved-column frac:  0.570281
field GPU/FWI priority:               none
```

Tested offsets:

```text
no correction:             0.000000 ns
conservative lower:        0.068762 ns
bootstrap CI lower:        0.108055 ns
bootstrap median:          0.117878 ns
nominal relative anchor:   0.127701 ns
bootstrap CI upper:        0.147348 ns
conservative upper:        0.186640 ns
```

Run 079 folds the perturbation sensitivity into the paper-facing bundle:

```text
policy label:                         field_publication_claim_bundle_2d_qc_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          12
claim boundaries:                     11
time-zero perturbation included:       true
bootstrap-CI support:                 9 / 9
conservative support:                 6 / 6
ready for manuscript supplement:      true
gpu priority:                         none
```

Run 080 refreshes the dataset-level policy:

```text
policy label:                         field_2d_qc_not_3d_or_fwi
publication bundle figure rows:       12
publication bundle claim boundaries:  11
publication perturbation policy:      field_time_zero_ci_perturbation_stack_robust
publication perturbation support:     9 / 9 bootstrap-CI rows, 6 / 6 conservative rows
survey classification:                independent_2d_line_profiles
```

## Interpretation

The short 014/016 relative time-zero correction is not only supported at the
single nominal offset. It remains B-scan-QC supported across all tested
bootstrap-CI and conservative-envelope perturbations in the three shallow stack
windows. This strengthens the manuscript uncertainty argument for the short
field pair.

The result remains a measured-field QC stress test. It does not create an
absolute time-zero calibration, field FWI target, 3D survey, radius estimate, or
cover-depth estimate.

## Validation

Focused tests:

```text
tests/test_gssi_field_time_zero_perturbation_sensitivity.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
15 passed
```

Figure validation:

```text
078 field_time_zero_perturbation_sensitivity.png: 2773x869, dynamic range=255
079 field_publication_claim_bundle.png: 2569x869, dynamic range=255
080 field_dataset_policy.png: 12259x835, dynamic range=255
```
