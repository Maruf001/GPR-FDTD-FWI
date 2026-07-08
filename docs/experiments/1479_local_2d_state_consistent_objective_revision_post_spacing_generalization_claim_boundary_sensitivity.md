# Experiment 1479: Post Spacing Generalization Claim Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1478` claim-boundary validator with controlled damaged
variants.

This confirms that the updated post-spacing claim boundary is sensitive to
count drift, spacing-result drift, boundary flag drift, blocked-claim
promotion, downstream promotion, figure problems, and missing script snapshots.

This uses saved artifacts only. It does not run new FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1479_local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_spacing_generalization_claim_boundary_sensitivity.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_SPACING_GENERALIZATION_CLAIM_BOUNDARY_SENSITIVITY.md
```

## Result

```text
scenarios:                  11
expected pass:              1
observed pass:              1
expected failures:          10
observed failures:          10
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1477:     true
rejects damaged variants:   true
broad radius promoted:      false
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
```

## Interpretation

The validator accepts the exact run `1477` boundary and rejects controlled
damage to claim counts, spacing counts, boundary flags, blocked claims,
downstream states, figure validation, and script snapshots.

## Decision

Use runs `1477-1479` as the guarded current 2D near/far generalization
claim-boundary block. Broad-radius, physical, GPU, field-transfer, field-FWI,
and 3D/HPC claims remain blocked.
