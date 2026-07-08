# BEM Experiment 372: Post Intake Worksheet Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `371` BEM post-intake claim boundary from artifacts.

This run checks that the new intake-worksheet claim, claim counts, blocked
claim rows, downstream guardrails, figure output, and script snapshots remain
internally consistent.

## Output

```text
outputs/bem_experiments/372_project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validator_checks.csv
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validator_summary.json
figures/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
claim count:                    13
guarded claims:                 10
blocked claims:                 3
intake worksheet ready:         true
accepts exact run 368:          true
rejects damaged variants:       true
missing packet items:           34
real packet files present:      false
real comparison ready:          false
threshold calibration ready:    false
broad BEM replacement ready:    false
field transfer ready:           false
GPU work ready:                 false
3D validation ready:            false
field FWI ready:                false
```

## Interpretation

The saved run `371` boundary is internally consistent. The intake worksheet is
guarded as a non-evidence handoff artifact, and all real-packet dependent BEM
claims remain blocked.

## Decision

Use run `372` as the validator for the run `371` BEM post-intake claim
boundary. Sensitivity hardening remains required before treating the boundary
block as guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_intake_worksheet_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3581x929, dynamic range=255
```
