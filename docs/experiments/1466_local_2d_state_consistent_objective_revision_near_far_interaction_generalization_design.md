# Experiment 1466: Near/Far Interaction Generalization Design

Date: 2026-06-28

## Purpose

Define the next independent CPU checks required before the local near/far
interaction mechanism can be considered for broader promotion.

This is a design packet. It does not run new FDTD simulations, launch GPU work,
transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1466_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_cases.csv
data/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_acceptance_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_INTERACTION_GENERALIZATION_DESIGN.md
scripts/run_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design.py
scripts/test_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
design cases:                  8
design axes:                   5
acceptance checks:             7
passed acceptance checks:      7
requires new CPU sweep cases:  8
execute now cases:             0
generalization design ready:   true
broad radius promoted:         false
physical claim ready:          false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
```

Design axes:

| Design case | Axis | Purpose |
| --- | --- | --- |
| target x shift left | target position | Check whether near-dominated all-objective failure persists away from the current x location. |
| target x shift right | target position | Check symmetry across the receiver aperture. |
| target depth shallower | target depth | Test whether near/far interaction changes with travel-time separation. |
| target depth deeper | target depth | Test whether the wrong-lock threshold changes with weaker returns. |
| neighbor spacing narrower | neighbor spacing | Test whether stronger coupling makes partial failures start earlier. |
| neighbor spacing wider | neighbor spacing | Test whether weaker coupling delays partial failures. |
| source time-shift positive | source model | Separate geometry mechanism from source-timing sensitivity. |
| receiver offset variant | acquisition | Test whether acquisition layout changes the ambiguity plateau. |

## Interpretation

The guarded local mechanism needs independent geometry, depth, neighbor-spacing,
source, and acquisition variants before any broad-radius or physical-transfer
claim can be promoted.

## Decision

Use run `1466` as the next-design packet. Do not execute GPU, field FWI, or
3D/HPC work from the current local mechanism evidence.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design.py
3 passed
```

Figure validation:

```text
3365x900, dynamic range=255
```
