# Experiment 1506: Post Fine Margin Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1505` claim-boundary validator with controlled damaged
variants.

Run `1505` validates the saved run `1504` post-margin claim boundary. This run
checks that the validator accepts the exact boundary and rejects controlled
drift in claim counts, base counts, the margin claim, margin metrics, blocked
claims, downstream states, figure validation, and script snapshots.

This run does not run new FDTD simulations, launch GPU work, transfer claims to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1506_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  14
expected pass:              1
observed pass:              1
expected failures:          13
observed failures:          13
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1504:     true
rejects damaged variants:   true
GPU work ready:             false
field transfer ready:       false
3D/HPC ready:               false
figure size:                3401x909
figure dynamic range:       255
```

## Interpretation

The run `1505` validator accepts the exact run `1504` claim boundary and
rejects controlled damaged variants for claim-count drift, base-count drift,
margin-claim drift, margin metric drift, blocked claim promotion, downstream
promotion, figure-validation drift, and script-snapshot drift.

## Decision

Use runs `1504-1506` as the guarded post-margin local 2D claim-boundary block.
Broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validation_sensitivity.py
3 passed
```
