# Experiment 876: Local 2D Source/Time-Zero Replay Contract

Date: 2026-06-25

## Purpose

Narrow the broad run `144` source/time-zero audit into a representative cached
CPU replay set.

This is a CPU-only replay contract. It does not run FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/145_local_2d_source_time_zero_replay_contract
```

Key artifacts:

```text
data/local_2d_source_time_zero_replay_contract_cases.csv
data/local_2d_source_time_zero_replay_contract_metrics.csv
data/local_2d_source_time_zero_replay_contract_summary.json
figures/local_2d_source_time_zero_replay_contract.png
docs/LOCAL_2D_SOURCE_TIME_ZERO_REPLAY_CONTRACT.md
scripts/run_local_2d_source_time_zero_replay_contract.py
scripts/test_local_2d_source_time_zero_replay_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source diagnostic files:             648
selected cases:                      5
contract metrics:                    4
contract metrics passed:             4
selected max abs time shift ps:      50.0
selected max amplitude deviation %:  48.64359318220286
selected max unique geometries:      11
CPU replay contract ready:           true
new FDTD run ready:                  false
GPU work ready:                      false
field transfer ready:                false
```

Selected replay cases:

| Rank | Category | Run | Max abs time shift ps | Max amplitude deviation % | Unique geometries |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | max_amplitude_stress | 233_coordinate_optimizer_variable_radius_location_only_seed21 | 50.0 | 48.64359318220286 | 4 |
| 2 | max_geometry_instability | 221_coordinate_optimizer_variable_radius_target_order_210_seed13 | 50.0 | 24.69154222744757 | 11 |
| 3 | stable_high_time_shift | 1251_coordinate_optimizer_close10_seed13_sources4_txrx50_objectives | 50.0 | 14.947674361202367 | 1 |
| 4 | fixed_radius_like_close14 | 410_coordinate_optimizer_close14_seed13_sources4_txrx50_noise19p642333984375_objectives | 50.0 | 14.78981943685016 | 1 |
| 5 | low_source_effect_control | 105_coordinate_optimizer_diagnostic_objective_cpu_smoke | 0.0 | 0.0 | 1 |

Contract metrics:

| Metric | Observed | Pass |
| --- | ---: | --- |
| time_shift_coverage | 50.0 | true |
| amplitude_scale_coverage | 48.64359318220286 | true |
| geometry_stability_contrast | 2 | true |
| field_reference_alignment | 6.0 | true |

## Interpretation

A focused CPU replay can start from five cached diagnostics that cover maximum
amplitude stress, maximum geometry instability, stable high time shift, a
close14 fixed-radius-like case, and a low-source-effect control.

The contract maps directly to the field run `176` boundary: time-zero and
amplitude references matter, but this cached replay does not itself create
field evidence.

## Decision

Use this contract for the next CPU replay. Do not launch new FDTD/GPU work
until the selected cached cases show a decision-changing gap that cannot be
answered by saved diagnostics.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_replay_contract.py
3 passed
```

Figure check:

```text
2428x778, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_replay_contract.py
sha256=b9b4eb93357f9a243bc988014aef8c620ae0eb7e1fd22fec84d0c9ae8237a5c0

test_local_2d_source_time_zero_replay_contract.py
sha256=44c6310d8c154157a2baff111c11d58b346131ff22726a5b553552eb9f55e8b5
```
