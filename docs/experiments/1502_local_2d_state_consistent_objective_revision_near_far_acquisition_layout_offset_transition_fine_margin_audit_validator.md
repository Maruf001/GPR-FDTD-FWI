# Experiment 1502: Fine Offset-Transition Margin Audit Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1501` fine offset-transition margin audit from
artifacts.

Run `1501` showed that the far-error stress cases have negative saved margins
before 45 mm and positive saved margins at 45 mm. This run validates that
artifact without rerunning FDTD.

This run does not run new FDTD simulations, launch GPU work, transfer claims to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1502_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
models audited:                     90
objective rows audited:             540
transition stress models:           24
pre-45 stress models all fail any:  true
45 mm stress models all clear:      true
max min-margin before 45:           -0.000374885
min margin at 45:                   0.00022905
margin sign flip:                   true
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
figure size:                        3581x929
figure dynamic range:               255
```

## Interpretation

The saved margin audit validates from artifacts. It preserves the 90-model
margin table, 24 stress transition rows, negative pre-45 margin, positive
45 mm margin, and blocked downstream states.

## Decision

Use run `1502` as the validator for the fine acquisition-layout margin audit.
Sensitivity hardening remains required before treating the margin audit as
guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_margin_audit_validator.py
3 passed
```
