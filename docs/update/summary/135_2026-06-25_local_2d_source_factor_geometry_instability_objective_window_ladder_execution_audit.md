# Local 2D Source-Factor Geometry-Instability Objective-Window Ladder Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records run `234`, which executes the six-objective ladder
command from run `232`.

This was a bounded CPU-only optimizer execution. It did not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/234_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit
outputs/experiments/1370_local_2d_source_factor_geomxdisc_objective_window_ladder_cpu
```

Tracked note:

```text
docs/experiments/911_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.md
```

## Result

```text
commands executed:                  true
timed out:                          false
exit code:                          0
elapsed seconds:                    471.871
complete optimizer output:          true
usable evidence ready:              true
artifact presence:                  6 / 6
confidence best x:                  188.0 mm
confidence truth x selected:        false
objective row count:                6
truth-x objective count:            0
lower-x objective count:            6
all objectives select lower x:      true
full batch ready:                   false
GPU work ready:                     false
field transfer ready:               false
```

Best x by objective:

```text
base:       188.0 mm
highband:   188.0 mm
late:       188.0 mm
late_high:  188.0 mm
veryhigh:   188.0 mm
early_high: 188.0 mm
```

## Decision

Objective-window selection does not repair the geometry-instability branch.
All six objective windows select the lower x candidate, not truth x.

Do not promote objective-window weighting as a fix. Broad source-factor batch
execution, GPU work, field transfer, and claims remain blocked.

The next useful branch is a geometry/state interaction audit that checks
whether the lower-x preference is caused by neighbor rebar state, initial-state
offsets, rasterization/material discretization, or the observable definition.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
sha256: fee41868503f1d29f203d6e04f0b58a4fe05fefe716c9eaca4d88a10b2bc5159

test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
sha256: cd0f64f3414e46468734401ede5dbd7fed3efd73f0c46748a74fc384ac746e1e
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py tests/test_local_2d_source_factor_geometry_instability_objective_window_ladder_execution_audit.py
pass
```

Figure check:

```text
1671x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then design the next bounded
geometry/state interaction audit.
