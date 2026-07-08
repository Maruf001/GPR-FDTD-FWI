# Experiment 1500: Post Fine Offset-Transition Claim Boundary Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1499` fine-refined claim-boundary validator with
controlled damaged variants.

Run `1499` validates the saved run `1498` claim boundary. This run checks that
the validator is selective: it should accept the exact saved boundary and reject
controlled drift in claim counts, fine-transition metrics, threshold flags,
blocked downstream states, figure validation, and script snapshots.

This is an artifact-only sensitivity run. It does not run new FDTD simulations,
launch GPU work, transfer claims to field evidence, run field FWI, or start
3D/HPC work.

## Output

```text
outputs/experiments/1500_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  21
expected pass:              1
observed pass:              1
expected failures:          20
observed failures:          20
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1498:     true
rejects damaged variants:   true
broad radius promoted:      false
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
figure size:                3671x925
figure dynamic range:       255
```

## Interpretation

The fine-refined claim-boundary validator accepts the exact run `1498` boundary
and rejects controlled damage to policy labels, claim counts, base boundary
counts, design-axis readiness, fine validation state, fine offset lists, fine
row counts, fine taxonomy, fine threshold flags, fine claim-row support,
blocked claims, downstream states, figure validation, and script snapshots.

This hardens the run `1498` claim boundary. The fine 45 mm acquisition-layout
transition is guarded, while broad-radius, physical-transfer, GPU, field-FWI,
and 3D/HPC claims remain blocked.

## Decision

Use runs `1498-1500` as the guarded fine-refined local 2D near/far
offset-transition claim-boundary block.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_sensitivity.py
3 passed
```
