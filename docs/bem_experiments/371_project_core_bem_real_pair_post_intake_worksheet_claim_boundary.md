# BEM Experiment 371: Post Intake Worksheet Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded non-evidence return-packet intake worksheet block into
the BEM claim boundary.

This run uses saved artifacts only. It does not stage real FDTD packet files,
run BEM/FDTD comparison, calibrate thresholds, launch GPU work, transfer to
field evidence, run field FWI, or start 3D validation.

## Output

```text
outputs/bem_experiments/371_project_core_bem_real_pair_post_intake_worksheet_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_claim_rows.csv
data/project_core_bem_real_pair_post_intake_worksheet_claim_boundary_summary.json
figures/project_core_bem_real_pair_post_intake_worksheet_claim_boundary.png
scripts/
```

## Result

```text
claims:                         13
guarded claims:                 10
blocked claims:                 3
intake worksheet sensitivity:   true
real packet files present:      false
missing packet items:           34
real comparison ready:          false
threshold calibration ready:    false
broad BEM replacement ready:    false
field transfer ready:           false
GPU work ready:                 false
3D validation ready:            false
field FWI ready:                false
claim boundary ready:           true
```

## Interpretation

The BEM claim boundary now includes the guarded non-evidence intake worksheet,
while real packet files, real comparison, threshold calibration, field
transfer, GPU work, and 3D validation remain blocked.

## Decision

Use run `371` as the current BEM claim boundary after the intake worksheet
block. Do not run real comparison or threshold calibration until the real
packet passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_intake_worksheet_claim_boundary.py
3 passed
```

Figure validation:

```text
3401x962, dynamic range=255
```
