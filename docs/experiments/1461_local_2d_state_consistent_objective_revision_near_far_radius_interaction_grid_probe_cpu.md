# Experiment 1461: Near/Far Radius-Error Interaction Grid Probe

Date: 2026-06-28

## Purpose

Extend the guarded run `1458-1460` near-neighbor radius-error threshold block
by testing whether the threshold changes when the far-neighbor radius error is
also varied.

This is a bounded CPU probe using the same dense scan and objective family as
the earlier threshold run. It does not launch GPU work, transfer to field
evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1461_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_RADIUS_INTERACTION_GRID_PROBE.md
scripts/run_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_probe_cpu.py
scripts/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_probe_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
near-radius deltas:                 5
far-radius deltas:                  3
grid models:                        15
objective selection rows:           90
candidate rows:                     360
scan positions:                     8
all-objectives-truth models:        5
any-failure models:                 10
all-objective failure models:       6
first any-failure by far delta:     {0.0: 1.5, -0.8: 0.5, -1.6: 0.5}
first all-failure by far delta:     {0.0: 1.5, -0.8: 1.5, -1.6: 1.5}
elapsed seconds:                    551.405
promote revised objective now:      false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Failure counts by near/far radius error:

| Far radius error | Near +0.0 mm | Near +0.5 mm | Near +1.0 mm | Near +1.5 mm | Near +1.9 mm |
| ---: | ---: | ---: | ---: | ---: | ---: |
| +0.0 mm | 0 | 0 | 0 | 6 | 6 |
| -0.8 mm | 0 | 4 | 4 | 6 | 6 |
| -1.6 mm | 0 | 4 | 4 | 6 | 6 |

## Interpretation

The interaction grid shows two useful facts:

1. Far-neighbor radius error makes the partial-failure boundary more fragile.
   With no far-neighbor radius error, the first failure appears at near
   +1.5 mm. With far-neighbor errors of -0.8 mm or -1.6 mm, partial failures
   begin at near +0.5 mm.
2. The severe all-objective wrong-lock boundary is stable across the tested
   far-neighbor settings. In all three far-radius conditions, all six
   objectives fail first at near +1.5 mm.

This supports the local mechanism interpretation: near-neighbor radius error is
the main driver of the hard wrong-x lock, while far-neighbor radius error
increases sensitivity in the intermediate partial-failure region.

## Decision

Use run `1461` as a bounded local near/far interaction probe. The result
improves the mechanism story but still does not promote broad-radius,
physical-transfer, GPU, field-FWI, or 3D/HPC claims.

## Validation

Focused setup test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_probe_cpu.py
3 passed
```

Figure validation:

```text
2834x1815, dynamic range=255
```
