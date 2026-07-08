# Experiment 875: Local 2D Source/Time-Zero Perturbation Replay Audit

Date: 2026-06-25

## Purpose

Scan saved local 2D coordinate-objective diagnostics for source-amplitude and
time-zero sensitivity before launching any new FDTD/GPU work.

This is a CPU-only replay audit over cached diagnostics. It does not run FDTD,
GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/144_local_2d_source_time_zero_perturbation_replay_audit
```

Key artifacts:

```text
data/local_2d_source_time_zero_perturbation_replay_audit.csv
data/local_2d_source_time_zero_perturbation_replay_audit_summary.json
figures/local_2d_source_time_zero_perturbation_replay_audit.png
docs/LOCAL_2D_SOURCE_TIME_ZERO_PERTURBATION_REPLAY_AUDIT.md
scripts/run_local_2d_source_time_zero_perturbation_replay_audit.py
scripts/test_local_2d_source_time_zero_perturbation_replay_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
diagnostic files audited:              648
diagnostic rows audited:               3807
replay-relevant files:                 645
nonzero time-shift files:              645
amplitude deviation >=5% files:        628
geometry-unstable files:               40
max absolute time shift ps:            50.0
max amplitude deviation percent:       48.64359318220286
field time-zero refs required:         3
field amplitude refs required:         3
CPU replay recommended:                true
new FDTD ready:                        false
GPU work ready:                        false
field transfer ready:                  false
```

Top replay-relevant diagnostics:

| Run | Max abs time shift ps | Max amplitude deviation % | Unique best geometries |
| --- | ---: | ---: | ---: |
| 233_coordinate_optimizer_variable_radius_location_only_seed21 | 50.0 | 48.64359318220286 | 4 |
| 242_coordinate_optimizer_variable_radius_location_only_seed34 | 50.0 | 44.47191242436864 | 4 |
| 225_coordinate_optimizer_variable_radius_location_only_seed13 | 50.0 | 44.23625628086831 | 6 |
| 219_coordinate_optimizer_variable_radius_close_spacing_from_assignment_seed13 | 50.0 | 41.807659838540175 | 10 |
| 221_coordinate_optimizer_variable_radius_target_order_210_seed13 | 50.0 | 24.69154222744757 | 11 |

## Interpretation

Saved local 2D diagnostics already contain large enough source/time-zero
effects to justify a focused CPU replay/design branch:

```text
time-zero: 645 diagnostic files have nonzero fitted source time shift
amplitude: 628 files have >=5% fitted amplitude deviation
geometry: 40 files choose different best geometry across objectives
```

This aligns with the field run `176` requirement for three time-zero reference
files and three amplitude-reference files.

## Decision

Use this audit to seed a focused CPU replay around source amplitude and
time-zero uncertainty. Do not launch new FDTD, GPU work, detector-FWI, field
transfer, field FWI, or 3D/HPC from this audit alone.

## Validation

Focused tests:

```text
tests/test_local_2d_source_time_zero_perturbation_replay_audit.py
2 passed
```

Figure check:

```text
2536x1280, dynamic range=255
```

Script snapshots:

```text
run_local_2d_source_time_zero_perturbation_replay_audit.py
sha256=d5a199a909e13cbb9e810c60c7eaf8dad315d6b70a92e01878a6b83e35ffab9f

test_local_2d_source_time_zero_perturbation_replay_audit.py
sha256=ea9d9616aea584066961e755a0f703b636e21eadeba9040e4402a05775d14dbf
```
