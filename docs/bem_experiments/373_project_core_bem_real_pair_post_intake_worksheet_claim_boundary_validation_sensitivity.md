# BEM Experiment 373: Post Intake Worksheet Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `372` BEM post-intake claim-boundary validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `371` boundary and
rejects damaged variants covering source identity drift, claim-count drift,
intake-worksheet claim drift, worksheet-metric drift, blocked-row drift,
downstream promotion, figure drift, and script-snapshot drift.

## Output

```text
outputs/bem_experiments/373_project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                    10
expected pass:                1
observed pass:                1
expected failures:            9
observed failures:            9
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 371:        true
rejects damaged variants:     true
real packet files present:    false
real comparison ready:        false
threshold calibration ready:  false
GPU work ready:               false
field transfer ready:         false
3D validation ready:          false
```

## Interpretation

The run `372` validator accepts the exact run `371` BEM boundary and rejects
controlled damaged variants. This protects the post-intake boundary from claim
count drift, worksheet promotion, downstream promotion, and missing validation
artifacts.

## Decision

Use runs `371-373` as the guarded BEM post-intake claim-boundary block. Real
comparison and threshold calibration remain blocked until real packet files
pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3365x909, dynamic range=255
```
