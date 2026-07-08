# Experiment 1431: Local 2D Post Far-Radius Refinement Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the local 2D claim boundary after runs `1427`-`1430`.

This run consolidates the design-gap audit, expanded-window radius bracket,
objective-failure diagnosis, and far-radius refinement into the current
decision boundary.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1431_local_2d_state_consistent_post_far_radius_refinement_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_post_far_radius_refinement_claim_boundary_rows.csv
data/local_2d_state_consistent_post_far_radius_refinement_claim_boundary_summary.json
figures/local_2d_state_consistent_post_far_radius_refinement_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_POST_FAR_RADIUS_REFINEMENT_CLAIM_BOUNDARY.md
scripts/run_local_2d_state_consistent_post_far_radius_refinement_claim_boundary.py
scripts/test_local_2d_state_consistent_post_far_radius_refinement_claim_boundary.py
scripts/script_snapshot_manifest.json
```

## Result

```text
boundary rows:                       6
promoted claims:                     2
bounded observations:                2
blocked claims:                      2
near radius last pass:               1.75 mm
far radius last pass:                0.75 mm
far radius first fail:               0.80 mm
minimum wrong-minus-truth misfit:    -0.0035579159181040702
claim boundary ready:                true
broad radius tolerance promoted:     false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The local 2D branch now supports:

| Claim | Decision |
| --- | --- |
| Corrected-state local mechanism | promoted |
| Objective-failure isolation to `veryhigh` | promoted |
| Near-radius expanded-window observation through +1.75 mm | bounded observation |
| Far-radius `veryhigh` boundary from -0.75 mm pass to -0.80 mm fail | bounded observation |
| Broad radius tolerance | blocked |
| Physical/GPU/field/3D escalation | blocked |

## Decision

Use run `1431` as the current local 2D claim boundary. Broad radius, physical,
GPU, field-transfer, field-FWI, and 3D/HPC claims remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_post_far_radius_refinement_claim_boundary.py
3 passed
```

Figure validation:

```text
3077x863, dynamic range=255
```
