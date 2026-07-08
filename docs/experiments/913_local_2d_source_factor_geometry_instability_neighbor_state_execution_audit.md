# Experiment 913: Local 2D Source-Factor Geometry-Instability Neighbor-State Execution Audit

Date: 2026-06-25

## Purpose

Execute the three neighbor-state commands designed in run `236`.

Run `234` showed that objective-window selection was not the cause of the
lower-x preference: all six objective windows selected `x=188 mm`. This run
tests whether correcting the non-target neighbor rebar state restores the truth
target coordinate.

This is a bounded CPU-only optimizer execution. It does not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/238_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit
outputs/experiments/1371_local_2d_source_factor_geomx_neighbor_positions_base_cpu
outputs/experiments/1372_local_2d_source_factor_geomx_neighbor_radii_base_cpu
outputs/experiments/1373_local_2d_source_factor_geomx_neighbor_full_base_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_geometry_instability_neighbor_state_execution_summary.json
data/local_2d_source_factor_geometry_instability_neighbor_state_execution_results.csv
data/local_2d_source_factor_geometry_instability_neighbor_state_execution_confidence.csv
data/local_2d_source_factor_geometry_instability_neighbor_state_execution_required_artifacts.csv
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_NEIGHBOR_STATE_EXECUTION_AUDIT.md
figures/local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.png
scripts/run_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
scripts/test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands executed:                 3 / 3
timed out:                         0
nonzero exits:                     0
complete optimizer outputs:        3
usable evidence ready:             3
truth-x design count:              1
lower-x design count:              2
neighbor-state repair found:       true
total elapsed seconds:             1235.083
full batch ready:                  false
GPU work ready:                    false
field transfer ready:              false
```

Design results:

| Design | Best x mm | Best z mm | Best radius mm | Best misfit | Truth x | Truth xyz |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `truth_neighbor_positions_base` | 189.0 | 90.0 | 5.0 | 0.16869103277938238 | false | false |
| `truth_neighbor_radii_base` | 188.0 | 90.0 | 5.0 | 0.42822235203536657 | false | false |
| `truth_neighbor_full_base` | 190.0 | 90.0 | 5.0 | 0.09154466861337839 | true | true |

## Interpretation

The lower-x preference is explained by neighbor-state error, not by objective
window choice alone.

Correcting neighbor positions helps but is incomplete: the best x moves from
`188 mm` to `189 mm`. Correcting neighbor radii alone does not fix the branch.
Correcting both neighbor positions and neighbor radii restores the truth target
geometry and gives the lowest misfit.

## Decision

Do not promote broad source-factor batch execution, GPU work, field transfer,
or claims from the earlier lower-x branch.

The next useful local 2D branch is a state-consistency guard: before optimizing
a target, neighbor states used as fixed context must be either truth/accepted
states or explicitly marked as uncertain. The current evidence supports a
mechanism claim that wrong fixed neighbor state can bias target x.

## Milestone Snapshot

This is a result-driven local 2D execution milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
sha256: 565d47ce82231ed7bb4eee5ed050fdc997afac07555b8e739a3e075cb7e0a434

test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
sha256: 2c4e7f93691d3ad65a23dca520b65539b0a3103add67ae3e72065442fd0baa5f
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py
2 passed
```

Compile check:

```text
run_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py: pass
tests/test_local_2d_source_factor_geometry_instability_neighbor_state_execution_audit.py: pass
```

Figure check:

```text
1816x738, dynamic range=255
```
