# Local 2D Source/Time-Zero Replay Audit

Date: 2026-06-25

## Scope

Start the source-amplitude/time-zero branch identified by run `143` using saved
coordinate-objective diagnostics rather than new simulation.

This is a CPU-only cached replay audit. It does not launch FDTD, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/144_local_2d_source_time_zero_perturbation_replay_audit
```

Tracked experiment note:

```text
docs/experiments/875_local_2d_source_time_zero_perturbation_replay_audit.md
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

## Interpretation

The source/time-zero issue is not hypothetical. Existing saved diagnostics
already show fitted 50 ps shifts, amplitude-scale deviations above 5% in 628
files, and geometry instability across objectives in 40 files.

This supports a focused CPU replay/design branch and reinforces the field run
`176` requirement for real time-zero and amplitude references.

## Decision

Continue source-amplitude/time-zero work as CPU replay/design. Do not launch
new FDTD, GPU work, detector-FWI, field transfer, field FWI, or 3D/HPC from
this audit alone.

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

## Next Marathon Branch

The marathon remains active. The next useful branch is to turn this broad audit
into a smaller replay contract: select representative cached diagnostics,
define source/time-zero acceptance metrics, and decide whether the replay can
close the design question without new FDTD.
