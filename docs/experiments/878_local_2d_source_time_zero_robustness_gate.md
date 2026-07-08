# Experiment 878: Local 2D Source/Time-Zero Robustness Gate

Date: 2026-06-25

## Purpose

Convert the selected source/time-zero replay from run `146` into pass/block
claim rows.

This is a CPU-only gate artifact. It does not run FDTD, GPU kernels, field FWI,
3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/147_local_2d_source_time_zero_robustness_gate
```

Key artifacts:

```text
data/local_2d_source_time_zero_robustness_gate.csv
data/local_2d_source_time_zero_robustness_gate_summary.json
figures/local_2d_source_time_zero_robustness_gate.png
docs/LOCAL_2D_SOURCE_TIME_ZERO_ROBUSTNESS_GATE.md
scripts/run_local_2d_source_time_zero_robustness_gate.py
scripts/test_local_2d_source_time_zero_robustness_gate.py
scripts/script_snapshot_manifest.json
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

Gate rows:

| Rank | Category | Geometry span mm | Gate pass | Claim level |
| ---: | --- | ---: | --- | --- |
| 1 | max_amplitude_stress | 120.41594578792295 | false | source_time_zero_sensitive_do_not_generalize |
| 2 | max_geometry_instability | 126.12394697280925 | false | source_time_zero_sensitive_do_not_generalize |
| 3 | stable_high_time_shift | 0.0 | true | source_time_zero_robust_for_selected_case |
| 4 | fixed_radius_like_close14 | 0.0 | true | source_time_zero_robust_for_selected_case |
| 5 | low_source_effect_control | 0.0 | true | source_time_zero_robust_for_selected_case |

## Interpretation

Source/time-zero robustness is mixed. The close14-like and stable/control cases
pass under the selected replay, but broad variable-radius cases are sensitive
and cannot support a general source/time-zero robustness claim.

## Decision

Use this gate in local 2D claim language. Keep broad source/time-zero
robustness, new FDTD, GPU work, detector-FWI, field transfer, field FWI, and
3D/HPC blocked.

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
