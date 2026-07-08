# Local 2D Experiment 1417: Repaired Execution CI Route Execution Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1416` CI route execution validator against controlled
damage cases.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1417_local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity_scenarios.csv
data/local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_EXECUTION_SENSITIVITY.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity.py
```

## Result

```text
scenarios:                                  22
expected pass scenarios:                    1
expected failure scenarios:                 21
observed pass scenarios:                    1
observed failure scenarios:                 21
unexpected outcomes:                        0
CI route execution sensitivity ready:        true
full pack remains authoritative:             true
sentinel replaces full pack:                 false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
ready for 3D/HPC:                            false
```

The exact run `1415` manifest passes. The 21 damaged variants fail as expected
for source-readiness drift, route-count drift, job-class drift, fast/full
authority drift, blocked-route drift, row-count mismatch, sentinel/full-pack
authority drift, and physical/GPU/field/FWI/3D readiness drift.

## Interpretation

The route execution validator has guarded sensitivity coverage. It accepts the
exact manifest and rejects controlled corruption of route structure, authority
rules, blocked-route behavior, row-count consistency, and claim-boundary flags.

## Decision

Use runs `1415-1417` as the guarded 2D CI route execution package. The
sentinel remains fast-smoke-only, the full core pack remains authoritative, and
physical/GPU/field/3D claims remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity.py
6 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_sensitivity.png
3257x890, dynamic range=255
```
