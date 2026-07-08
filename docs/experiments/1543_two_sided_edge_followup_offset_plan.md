# Experiment 1543: Two-Sided Edge Follow-Up Offset Plan

Date: 2026-06-29

## Purpose

Define a small follow-up offset plan for shrinking the sampled 45.0 mm
suppression bracket if a future FDTD run is worth the compute cost.

This run is a plan only. It does not run FDTD simulations, launch GPU work,
transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1543_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_plan_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan.png
scripts/
```

## Result

```text
source claims:                       21
source guarded claims:               18
source blocked claims:               3
source lower gap:                    0.007812 mm
source upper gap:                    0.015625 mm
source bracket span:                 0.023437 mm
proposed offsets:                    5
below-45 offsets:                    2
above-45 offsets:                    3
planned far-radius deltas:           -0.8, -1.6 mm
planned near-radius deltas:          1.5, 1.9 mm
planned cases:                       20
plan ready:                          true
follow-up FDTD executed:             false
new physical claim ready:            false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Proposed offsets:

| Priority | Offset (mm) | Side | Purpose |
| ---: | ---: | --- | --- |
| 1 | 44.996094 | below 45 | bisect lower failure-to-suppression gap |
| 2 | 45.007812 | above 45 | bisect upper suppression-to-reappearance gap |
| 3 | 44.998047 | below 45 | test near-suppression side of lower gap |
| 4 | 45.003906 | above 45 | test near-suppression side of upper gap |
| 5 | 45.011719 | above 45 | test near-reappearance side of upper gap |

## Interpretation

This run defines a small follow-up offset plan only. It does not change the
current claim boundary.

## Decision

Use run `1543` as the candidate offset plan if a future bracket-shrink FDTD run
is worth the compute cost.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan.py
3 passed
```

Figure validation:

```text
3005x880, dynamic range=255
```
