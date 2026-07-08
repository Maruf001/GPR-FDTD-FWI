# Local 2D Source-Factor Geometry-Instability Neighbor-State Execution Audit

Date: 2026-06-25

## Scope

This checkpoint records run `238`, which executes the three neighbor-state
commands from run `236`.

This was a bounded CPU-only optimizer execution. It did not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/238_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit
outputs/experiments/1371_local_2d_source_factor_geomx_neighbor_positions_base_cpu
outputs/experiments/1372_local_2d_source_factor_geomx_neighbor_radii_base_cpu
outputs/experiments/1373_local_2d_source_factor_geomx_neighbor_full_base_cpu
```

Tracked note:

```text
docs/experiments/913_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.md
```

## Result

```text
commands executed:                 3 / 3
complete optimizer outputs:        3
truth-x design count:              1
lower-x design count:              2
neighbor-state repair found:       true
total elapsed seconds:             1235.083
full batch ready:                  false
GPU work ready:                    false
field transfer ready:              false
```

Best x by design:

```text
truth_neighbor_positions_base: 189.0 mm
truth_neighbor_radii_base:     188.0 mm
truth_neighbor_full_base:      190.0 mm
```

## Decision

The geometry-instability branch now has a concrete mechanism: wrong fixed
neighbor state can bias target x. Correcting both neighbor positions and
neighbor radii restores truth x and gives the lowest misfit.

Do not promote broad source-factor batch execution, GPU work, field transfer,
or claims from the earlier lower-x branch. The next useful branch is a
state-consistency guard for target optimization.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
sha256: 565d47ce82231ed7bb4eee5ed050fdc997afac07555b8e739a3e075cb7e0a434

test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
sha256: 2c4e7f93691d3ad65a23dca520b65539b0a3103add67ae3e72065442fd0baa5f
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py tests/test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
pass
```

Figure check:

```text
1816x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then design a state-consistency
guard for target optimization.
