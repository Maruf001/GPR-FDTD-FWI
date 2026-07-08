# BEM Experiment 493: Post Real Return-File Acceptance-Gate Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `492` validator against controlled damage to the run `491`
BEM claim boundary.

## Output

```text
outputs/bem_experiments/493_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       34
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  33
observed failure scenarios:                  33
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 491:             true
validator rejects damaged variants:          true
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The validator accepts the exact run `491` boundary and rejects damaged variants
for claim-count drift, acceptance-gate readiness drift, acceptance-gate metric
drift, premature packet acceptance, downstream promotion, figure drift, and
script-snapshot drift.

## Decision

Use runs `491-493` as the current guarded BEM post-real-return-file-acceptance
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3725x883, dynamic range=255
```
