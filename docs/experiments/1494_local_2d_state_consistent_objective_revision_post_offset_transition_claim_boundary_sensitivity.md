# Experiment 1494: Post Offset-Transition Claim Boundary Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1493` refined claim-boundary validator with controlled
damaged variants.

The exact run `1492` boundary should pass. Damaged variants should fail when
they change policy labels, claim counts, axis readiness, spacing counts, source
thresholds, acquisition suppression, acquisition transition thresholds, blocked
claims, downstream states, figure validation, or script snapshots.

This is CPU-only validation hardening. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1494_local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  16
expected pass:              1
observed pass:              1
expected failures:          15
observed failures:          15
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1492:     true
rejects damaged variants:   true
broad radius promoted:      false
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
figure size:                3401x911
figure dynamic range:       255
```

## Interpretation

The refined claim-boundary validator accepts the exact run `1492` boundary and
rejects all controlled corruptions. This guards the refined two-threshold
acquisition-layout result without promoting broader physical, field, GPU, or
3D claims.

## Decision

Use runs `1492-1494` as the guarded refined 2D near/far offset-transition
claim-boundary block. Broad-radius, physical, GPU, field-transfer, field-FWI,
and 3D/HPC claims remain blocked.
