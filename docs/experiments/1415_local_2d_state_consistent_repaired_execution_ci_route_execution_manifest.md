# Local 2D Experiment 1415: Repaired Execution CI Route Execution Manifest

Date: 2026-06-28

## Purpose

Turn the guarded CI adoption checklist into an explicit route execution
manifest.

Runs `1412-1414` define and guard the adoption checklist. This run makes the
next operational split explicit:

```text
Which route can run reduced-sentinel fast smoke, which route requires the full
88-row core gate, and which routes remain blocked or require a new design?
```

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1415_local_2d_state_consistent_repaired_execution_ci_route_execution_manifest
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_execution_manifest_rows.csv
data/local_2d_state_consistent_repaired_execution_ci_route_execution_manifest_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_manifest.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_EXECUTION_MANIFEST.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_execution_manifest.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_execution_manifest.py
```

## Result

```text
CI routes:                                6
runnable CI jobs:                         4
blocked CI routes:                        2
fast-smoke jobs:                          2
full-core gate jobs:                      2
new-design-required jobs:                 1
blocked-current-evidence jobs:            1
reduced-sentinel total rows if run:        22
full-core total rows if run:               176
CI route execution manifest ready:         true
full pack remains authoritative:           true
sentinel replaces full pack:               false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
field FWI ready:                           false
ready for 3D/HPC:                          false
```

## Interpretation

The repaired local 2D guard now has an explicit CI route execution manifest.
Two routes are runnable reduced-sentinel fast smoke, two routes require the
repaired 88-row full core gate, one route requires a new design, and one route
remains blocked by current evidence.

## Decision

Use run `1415` as the route-level CI execution manifest. The 11-row sentinel
remains fast-smoke-only, the 88-row core table remains authoritative for
boundary-sensitive changes, and physical/GPU/field/3D claims remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_execution_manifest.py
5 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_execution_manifest.png
2608x835, dynamic range=255
```
