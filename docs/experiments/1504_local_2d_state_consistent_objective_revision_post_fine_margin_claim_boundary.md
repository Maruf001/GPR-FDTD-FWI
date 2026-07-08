# Experiment 1504: Post Fine Margin Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded fine-transition margin audit into the local 2D claim
boundary.

Runs `1501-1503` showed that the 45 mm acquisition-layout clearing is visible
in saved misfit margins, not only in binary pass/fail labels. This run adds
that result as a separate guarded claim.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer claims to field evidence, run field FWI, or start
3D/HPC work.

## Output

```text
outputs/experiments/1504_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                         15
guarded claims:                 12
blocked claims:                 3
boundary ready:                 true
margin sensitivity ready:       true
margin sign flip:               true
max min-margin before 45:       -0.000374885
min margin at 45:               0.00022905
transition stress models:       24
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
figure size:                    3761x964
figure dynamic range:           255
```

## Interpretation

The local 2D near/far claim boundary now includes the guarded margin
observation: the tested far-error stress cases have negative margins before
45 mm and positive margins at 45 mm.

The added claim strengthens the local mechanism story, but it does not promote
a broad physical rule or justify GPU/field/3D escalation.

## Decision

Use run `1504` as the current local 2D near/far claim boundary after margin
integration. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC
claims blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary.py
3 passed
```
