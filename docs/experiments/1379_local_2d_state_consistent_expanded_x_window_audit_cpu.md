# Experiment 1379: Local 2D State-Consistent Expanded X-Window Audit

Date: 2026-06-27

## Purpose

Check whether the state-consistent target recovery is an artifact of the prior
candidate x-window.

Runs `1375`-`1378` used a local target window ending at the truth coordinate
x=190 mm. This run expands the candidate x-window to:

```text
186, 187, 188, 189, 190, 191, 192, 193, 194 mm
```

and evaluates the corrected state plus selected radius-boundary states across
all six objective windows.

This is a bounded CPU-only local 2D experiment. It does not launch broad
batches, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/experiments/1379_local_2d_state_consistent_expanded_x_window_audit_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_expanded_x_window_results.csv
data/local_2d_state_consistent_expanded_x_window_candidates.csv
data/local_2d_state_consistent_expanded_x_window_summary.json
figures/local_2d_state_consistent_expanded_x_window_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_EXPANDED_X_WINDOW_AUDIT.md
scripts/run_local_2d_state_consistent_expanded_x_window_audit.py
scripts/test_local_2d_state_consistent_expanded_x_window_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
neighbor states tested:              5
objective windows tested:            6
result rows:                         30
correct-state truth rows:            6 of 6
perturbed truth rows:                13 of 24
perturbed failure rows:              11
minimum wrong-minus-truth misfit:    -0.013784677258736597
expanded x-window all passed:        false
tolerance boundary detected:         true
broad batch ready:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
elapsed seconds:                     255.865
```

Correct-state outcomes:

| Objective | Selected x mm | Wrong minus truth misfit | Truth geometry |
| --- | ---: | ---: | --- |
| base | 190.0 | 0.022485563942480497 | true |
| highband | 190.0 | 0.01994705692712514 | true |
| late | 190.0 | 0.03116866327859709 | true |
| late_high | 190.0 | 0.04212689628171617 | true |
| veryhigh | 190.0 | 0.01994273760685534 | true |
| early_high | 190.0 | 0.00799252117380315 | true |

Failure rows:

| Perturbation | Objective | Selected x mm | Wrong minus truth misfit |
| --- | --- | ---: | ---: |
| near_neighbor_radius_plus_2p00mm | veryhigh | 187.0 | -0.004660070912023737 |
| near_neighbor_radius_plus_2p25mm | base | 187.0 | -0.00027061154662177955 |
| near_neighbor_radius_plus_2p25mm | late | 187.0 | -0.0014443119831138995 |
| near_neighbor_radius_plus_2p25mm | veryhigh | 187.0 | -0.009942253207946672 |
| far_neighbor_radius_minus_1p50mm | veryhigh | 187.0 | -0.0035579159181040702 |
| far_neighbor_radius_minus_1p75mm | base | 187.0 | -0.0000372744339579012 |
| far_neighbor_radius_minus_1p75mm | highband | 187.0 | -0.0022434737551220996 |
| far_neighbor_radius_minus_1p75mm | late | 187.0 | -0.0018612266970207403 |
| far_neighbor_radius_minus_1p75mm | late_high | 187.0 | -0.007048809546210455 |
| far_neighbor_radius_minus_1p75mm | veryhigh | 187.0 | -0.013784677258736597 |
| far_neighbor_radius_minus_1p75mm | early_high | 187.0 | -0.001968748078119531 |

## Interpretation

The main corrected-state mechanism survives the expanded x-window. With
candidates above and below the truth coordinate, all six objectives still pick:

```text
x = 190 mm
z = 90 mm
radius = 5 mm
```

That means the corrected-state success is not simply because x=190 mm was the
upper edge of the earlier search window.

The tolerance boundary is stricter than run `1378` suggested. Once x=187 mm is
available, the very-high objective flips at near-neighbor radius +2.0 mm and
far-neighbor radius -1.5 mm. The failures all move toward x=187 mm, not toward
candidate values above the truth coordinate.

## Decision

Use the corrected-state result as the stable local 2D mechanism claim:

```text
With consistent neighbor geometry, the target recovery remains x=190 mm even
when the target x-window is expanded from 186 mm to 194 mm.
```

Do not overstate the radius tolerance. The broader tolerance claim should be:

```text
Small radius-state perturbations can remain stable under narrow target windows,
but under a wider x-window and stricter objective set, selected radius
perturbations can flip the target to x=187 mm.
```

This supports a bounded local mechanism result, not broad local 2D batches, GPU
work, field transfer, or field FWI.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_expanded_x_window_audit.py
sha256: bbbc519fc3907f5be1684cd9fb6016e5570d2da4f1a44f3da7eaba2dea985f0b

test_local_2d_state_consistent_expanded_x_window_audit.py
sha256: b29ec131345c439a9a423657605352ff0f7d3f3386909ca5992c5d48634e7057
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_expanded_x_window_audit.py
2 passed
```

Figure check:

```text
local_2d_state_consistent_expanded_x_window_audit.png
2356x1421, dynamic range=255
```
