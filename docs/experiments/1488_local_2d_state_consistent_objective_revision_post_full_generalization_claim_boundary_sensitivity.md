# Experiment 1488: Post Full Generalization Claim Boundary Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1487` full-generalization claim-boundary validator with
controlled damaged variants.

This uses saved artifacts only. It does not run new FDTD simulations, launch GPU
work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1488_local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_full_generalization_claim_boundary_sensitivity.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_FULL_GENERALIZATION_CLAIM_BOUNDARY_SENSITIVITY.md
```

## Result

```text
scenarios:                  13
expected pass:              1
observed pass:              1
expected failures:          12
observed failures:          12
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1486:     true
rejects damaged variants:   true
broad radius promoted:      false
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
```

## Interpretation

The full claim-boundary validator accepts the exact run `1486` boundary and
rejects controlled damage to policy labels, claim counts, axis readiness,
spacing counts, source thresholds, acquisition suppression, blocked claims,
downstream states, figure validation, and script snapshots.

## Decision

Use runs `1486-1488` as the guarded full 2D near/far generalization
claim-boundary block. Broad-radius, physical, GPU, field-transfer, field-FWI,
and 3D/HPC claims remain blocked.
