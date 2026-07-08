# Local 2D Source-Factor Geometry-Instability Highband/Base Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records run `230`, which executes the corrected base-plus-
highband command from run `228`.

This was a bounded CPU-only optimizer execution. It did not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/230_local_2d_source_factor_geometry_instability_highband_base_execution_audit
outputs/experiments/1369_local_2d_source_factor_geomxdisc_shifted_source_base_highband_cpu
```

Tracked note:

```text
docs/experiments/909_local_2d_source_factor_geometry_instability_highband_base_execution_audit.md
```

## Result

```text
commands executed:               true
timed out:                       false
exit code:                       0
elapsed seconds:                 454.508
complete optimizer output:       true
usable evidence ready:           true
artifact presence:               6 / 6
confidence best x:               188.0 mm
confidence truth x selected:     false
base best x:                     188.0 mm
highband best x:                 188.0 mm
highband truth x selected:       false
full batch ready:                false
GPU work ready:                  false
field transfer ready:            false
```

## Decision

The corrected highband diagnostic does not reverse the geometry-instability
lower-x preference. Both `base` and `highband` select `x=188 mm`, while truth is
`x=190 mm`.

Do not promote highband weighting as a fix for this branch. The next useful
local 2D branch is an objective/observable discriminant for why the
geometry-instability case prefers lower x even with truth z and radius.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
sha256: e82b9c6a58eb92c4adbb05f63c259c17f3dde4f0f5eff39959335b2f5da5a12a

test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
sha256: 3b6b12345bfd185a3db6103a8bfe00d51210fb60056992079003f6471d584186
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py -q
3 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py tests/test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
pass
```

Figure check:

```text
1672x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with a snapshot refresh, then pursue the next bounded
objective/observable discriminant branch.
