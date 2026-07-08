# Local 2D Source/Time-Zero Robustness Gate

Date: 2026-06-25

## Scope

Convert the run `146` selected source/time-zero replay into pass/block claim
rows.

This is a CPU-only gate artifact. It does not launch FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/147_local_2d_source_time_zero_robustness_gate
```

Tracked experiment note:

```text
docs/experiments/878_local_2d_source_time_zero_robustness_gate.md
```

## Result

```text
cases gated:                         5
robust cases:                        3
blocked sensitive cases:             2
general source/time-zero claim ready: false
close14-like gate pass:              true
broad variable-radius claim ready:   false
new FDTD run ready:                  false
GPU work ready:                      false
field transfer ready:                false
```

## Interpretation

The source/time-zero robustness result is not globally positive. It supports
scoped language for the selected close10, close14, and control cases, but broad
variable-radius cases remain sensitive.

## Decision

Use run `147` as the source/time-zero robustness gate. Do not make a general
source/time-zero robustness claim. Keep new FDTD, GPU work, detector-FWI, field
transfer, field FWI, and 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_robustness_gate.py
2 passed
```

Figure check:

```text
1925x770, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_robustness_gate.py
sha256=88c4a98802af9b8f48f7758ee8edd0959dc0bb36e2e62a7a0c2d0b2d3b2497e0

test_local_2d_source_time_zero_robustness_gate.py
sha256=64e239ae1a794a593e13187b0a0ff6c8a6c35a1aa70c0c9e9edce352a6d4fa05
```

## Next Marathon Branch

The marathon remains active. The next useful work is to refresh the
presentation/evidence pack or milestone snapshot audit so it includes the new
source/time-zero robustness gate.
