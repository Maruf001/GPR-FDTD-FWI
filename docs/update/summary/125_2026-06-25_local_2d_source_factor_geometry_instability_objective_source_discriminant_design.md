# Local 2D Source-Factor Geometry-Instability Objective/Source Discriminant Design

Date: 2026-06-25

## Scope

This checkpoint records run `224`, which designs three bounded CPU commands to
separate source-timing and objective-weighting effects in the
geometry-instability lower-x preference.

This was command design only. It did not run FDTD, optimizer commands, GPU work,
field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/224_local_2d_source_factor_geometry_instability_objective_source_discriminant_design
```

Tracked note:

```text
docs/experiments/906_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.md
```

## Result

```text
commands generated:                   3
predicted runner experiment start:    1367
predicted runner experiment end:      1369
command design passes:                3
command design failures:              0
estimated candidate/profile/objective evaluations: 12
output collisions:                    0
geometry discriminant execution ready: true
full batch ready:                     false
GPU work ready:                       false
field transfer ready:                 false
```

Designed commands:

| Expected output | Discriminant | Estimated evals |
| --- | --- | ---: |
| `1367_local_2d_source_factor_geomxdisc_matched_nominal_source_base_cpu` | matched nominal source/base objective | 3 |
| `1368_local_2d_source_factor_geomxdisc_shifted_source_highband_cpu` | shifted source/highband objective | 3 |
| `1369_local_2d_source_factor_geomxdisc_time_grid_base_cpu` | two-source-time grid/base objective | 6 |

## Decision

Run `224` is the next executable local 2D geometry-instability branch. It is
bounded and CPU-only. Full source-factor batch execution, GPU work, field
transfer, and claims remain blocked.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
sha256: afe5d2822d53558561a1f48281fa01e40287cc30b556d4f53671a70873e60a1f

test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
sha256: 92c15c43a01785603647e0615db290a0f7b13b37219e2440499740dce867b67a
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py tests/test_local_2d_source_factor_geometry_instability_objective_source_discriminant_design.py
pass
```

Figure check:

```text
2032x770, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then execute the bounded
geometry-instability discriminants if resources remain safe.
