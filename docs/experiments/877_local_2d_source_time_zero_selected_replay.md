# Experiment 877: Local 2D Source/Time-Zero Selected Replay

Date: 2026-06-25

## Purpose

Execute the run `145` CPU replay contract over five selected cached
coordinate-objective diagnostics.

This is a cached replay analysis. It does not run FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/146_local_2d_source_time_zero_selected_replay
```

Key artifacts:

```text
data/local_2d_source_time_zero_selected_replay.csv
data/local_2d_source_time_zero_selected_replay_summary.json
figures/local_2d_source_time_zero_selected_replay.png
docs/LOCAL_2D_SOURCE_TIME_ZERO_SELECTED_REPLAY.md
scripts/run_local_2d_source_time_zero_selected_replay.py
scripts/test_local_2d_source_time_zero_selected_replay.py
scripts/script_snapshot_manifest.json
```

## Result

```text
selected cases:                  5
selected rows:                   42
decision-sensitive cases:        2
geometry-stable cases:           3
max geometry span mm:            126.12394697280925
max time-shift span ps:          50.0
max amplitude span percent:      56.284751892158646
CPU replay complete:             true
new FDTD run ready:              false
GPU work ready:                  false
field transfer ready:            false
```

Replay result:

| Rank | Category | Run | Geometry span mm | Time span ps | Amplitude span % | Decision sensitive |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 1 | max_amplitude_stress | 233_coordinate_optimizer_variable_radius_location_only_seed21 | 120.41594578792295 | 50.0 | 56.284751892158646 | true |
| 2 | max_geometry_instability | 221_coordinate_optimizer_variable_radius_target_order_210_seed13 | 126.12394697280925 | 50.0 | 22.857024460539577 | true |
| 3 | stable_high_time_shift | 1251_coordinate_optimizer_close10_seed13_sources4_txrx50_objectives | 0.0 | 50.0 | 14.022071571129334 | false |
| 4 | fixed_radius_like_close14 | 410_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p642333984375_objectives | 0.0 | 50.0 | 13.89773278875104 | false |
| 5 | low_source_effect_control | 105_coordinate_optimizer_diagnostic_objective_cpu_smoke | 0.0 | 0.0 | 0.0 | false |

## Interpretation

The source/time-zero effect is decision-sensitive in the broad variable-radius
cached cases, with geometry spans above 120 mm. It is stable in the selected
close10, close14, and low-effect control cases.

This means future local 2D claims need source/time-zero robustness language.
The result still does not justify new FDTD/GPU work by itself because the
selected cached diagnostics already answer the immediate replay question.

## Decision

Use this selected replay result to scope source/time-zero robustness metrics.
Keep new FDTD, GPU work, detector-FWI, field transfer, field FWI, and 3D/HPC
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_selected_replay.py
3 passed
```

Figure check:

```text
2464x778, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_selected_replay.py
sha256=0ebbf1c10171082deeaea21ba52de65e4c9791c4ab40f330a092e9196ec96756

test_local_2d_source_time_zero_selected_replay.py
sha256=ce45551fbdf12b39fb365e95a26d5933bedec906d4479dfcc3939c32b8f37f22
```
