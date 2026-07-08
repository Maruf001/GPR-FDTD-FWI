# Experiment 1470: Near/Far Depth Generalization Probe

Date: 2026-06-28

## Purpose

Execute the target-depth generalization case from the guarded near/far
interaction design block. Run `1468` showed that the severe near/far failure
pattern depends on target x-position relative to the fixed acquisition aperture.
This run asks whether the same near/far radius-error interaction changes when
the whole three-target family is moved 10 mm shallower or 10 mm deeper.

This is a CPU-only synthetic 2D FDTD probe. It does not run GPU work, field FWI,
field transfer, neural-network training, or 3D/HPC work.

## Output

```text
outputs/experiments/1470_local_2d_state_consistent_objective_revision_near_far_depth_generalization_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_depth_generalization_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_depth_generalization_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_depth_generalization_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_depth_generalization_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_DEPTH_GENERALIZATION_PROBE.md
```

## Result

```text
depth shifts:                    [-10.0, 0.0, 10.0] mm
depth count:                     3
near-radius deltas:              5
far-radius deltas:               3
grid models:                     45
objective selection rows:        270
candidate rows:                  1080
all-objectives-truth models:     29
any-failure models:              16
all-objective failure models:    10
elapsed time:                    1693.303 s
physical claim ready:            false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

First partial-failure threshold by depth and far-radius error:

| Depth shift | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| -10 mm shallower | none | none | none |
| 0 mm | near +1.5 mm | near +0.5 mm | near +0.5 mm |
| +10 mm deeper | near +1.5 mm | near +1.5 mm | near +1.5 mm |

First all-objective failure threshold by depth and far-radius error:

| Depth shift | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| -10 mm shallower | none | none | none |
| 0 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |
| +10 mm deeper | none | near +1.5 mm | near +1.5 mm |

## Interpretation

The zero-depth slice reproduces the run `1461` local behavior: far-neighbor
radius error shifts partial failures earlier, and all-objective failures start
at near +1.5 mm.

The shallower target-family slice has no failures in this tested grid. The
deeper slice keeps severe failures in the far-error cases, but not for the
no-far-error case. Depth therefore changes the severity and threshold pattern:
the mechanism is not depth-invariant.

## Decision

Use run `1470` as the first executed target-depth generalization check. The
result further narrows the claim boundary: the near/far mechanism is real in
the local tested setup, but its severity depends on target position and depth.
Do not promote broad-radius tolerance, physical-transfer, GPU, field-FWI, or
3D/HPC claims from this result.

Next defensible 2D work is to validate run `1470`, then decide whether the next
generalization axis should be neighbor spacing, source timing, or acquisition
offset.

## Validation

Setup tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_depth_generalization_probe_cpu.py
5 passed
```

Figure validation:

```text
3185x1495, dynamic range=255
```
