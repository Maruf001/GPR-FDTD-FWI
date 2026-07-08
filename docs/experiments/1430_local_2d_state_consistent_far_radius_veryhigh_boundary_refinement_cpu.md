# Experiment 1430: Local 2D Far-Radius Veryhigh Boundary Refinement

Date: 2026-06-28

## Purpose

Refine the far-neighbor radius-decrease boundary isolated by runs `1428` and
`1429`, using the same expanded target x-window and six-objective audit.

This run does not launch GPU work, transfer to field data, run field FWI, or
promote 3D/HPC work.

## Output

```text
outputs/experiments/1430_local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_results.csv
data/local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_candidates.csv
data/local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_summary.json
figures/local_2d_state_consistent_far_radius_veryhigh_boundary_refinement.png
docs/LOCAL_2D_STATE_CONSISTENT_FAR_RADIUS_VERYHIGH_BOUNDARY_REFINEMENT.md
scripts/run_local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_cpu.py
scripts/test_local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations:                       7
objectives:                          6
result rows:                         42
candidate rows:                      756
correct state all objectives truth:  true
perturbed truth rows:                31
perturbed failure rows:              5
minimum wrong-minus-truth misfit:    -0.0035579159181040702
boundary detected:                   true
far -radius last all-objectives pass: 0.75 mm
far -radius first any-objective fail: 0.80 mm
elapsed:                             357.109 seconds
```

All five failures occur under the `veryhigh` objective:

| Perturbation | Objective | Selected x | Wrong-minus-truth misfit |
| --- | --- | ---: | ---: |
| far neighbor radius -0.80 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |
| far neighbor radius -0.85 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |
| far neighbor radius -0.90 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |
| far neighbor radius -0.95 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |
| far neighbor radius -1.00 mm | veryhigh | 187.0 mm | -0.0035579159181040702 |

## Interpretation

The far-neighbor `veryhigh` boundary is now sharply localized: -0.75 mm passes
all six objectives, while -0.80 mm fails under `veryhigh`. The failure plateau
continues through -1.00 mm with the same selected wrong x and same negative
margin.

## Decision

Use run `1430` as the refined local 2D far-radius boundary. Do not promote
broad radius, physical, GPU, field-transfer, field-FWI, or 3D/HPC claims from
this branch.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_far_radius_veryhigh_boundary_refinement_cpu.py
2 passed
```

Figure validation:

```text
2460x1459, dynamic range=255
```
