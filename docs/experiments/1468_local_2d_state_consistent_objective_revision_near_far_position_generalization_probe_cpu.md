# Experiment 1468: Near/Far Position Generalization Probe

Date: 2026-06-28

## Purpose

Execute the first CPU generalization case from the guarded near/far interaction
design block. Runs `1461-1463` showed a local near/far radius-error interaction
at the original target position. This run asks whether that same failure pattern
survives when the whole three-target family is translated left and right across
the fixed acquisition aperture.

This is a CPU-only synthetic 2D FDTD probe. It does not run GPU work, field FWI,
field transfer, neural-network training, or 3D/HPC work.

## Output

```text
outputs/experiments/1468_local_2d_state_consistent_objective_revision_near_far_position_generalization_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_position_generalization_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_position_generalization_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_position_generalization_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_position_generalization_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_POSITION_GENERALIZATION_PROBE.md
```

The exact run script and focused test were frozen in:

```text
outputs/experiments/1468_local_2d_state_consistent_objective_revision_near_far_position_generalization_probe_cpu/scripts
```

## Result

```text
position shifts:                  [-20.0, 0.0, 20.0] mm
near-radius deltas:               5
far-radius deltas:                3
grid models:                      45
objective selection rows:         270
candidate rows:                   1080
all-objectives-truth models:      25
any-failure models:               20
all-objective failure models:     6
elapsed time:                     1666.873 s
physical claim ready:             false
GPU work ready:                   false
field transfer ready:             false
field FWI ready:                  false
3D/HPC ready:                     false
```

First partial-failure threshold by target position and far-radius error:

| Target shift | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| -20 mm | none | near +1.5 mm | near +1.5 mm |
| 0 mm | near +1.5 mm | near +0.5 mm | near +0.5 mm |
| +20 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |

First all-objective failure threshold by target position and far-radius error:

| Target shift | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| -20 mm | none | none | none |
| 0 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |
| +20 mm | none | none | none |

## Interpretation

The zero-shift slice reproduces the run `1461` local behavior: far-neighbor
radius error can make partial failures start earlier, while severe
all-objective wrong-lock failure starts at near +1.5 mm.

The translated target-family slices do not preserve that severe all-objective
failure. At -20 mm and +20 mm, the same near/far error grid produces partial
failures, but no all-objective failure models. This means the earlier
near-dominated all-objective failure boundary is not a broad position-invariant
rule under the fixed aperture. It is a local mechanism at the original target
position.

## Decision

Use this run as the first executed target-position generalization check. The
result strengthens the guardrails: the mechanism is real locally, but its
severity depends on target position relative to the fixed acquisition aperture.
Do not promote a broad radius-tolerance rule, physical-transfer claim, GPU
queue, field-FWI branch, or 3D/HPC branch from this result.

Next defensible synthetic 2D work is to validate run `1468`, then decide whether
the next executed generalization should vary target depth, neighbor spacing,
source timing, or acquisition offset.

## Validation

Setup tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_position_generalization_probe_cpu.py
5 passed
```

Figure validation:

```text
3184x1495, dynamic range=255
```
