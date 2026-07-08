# Local 2D Experiment 1418: Repaired Execution CI Route Command Plan

Date: 2026-06-28

## Purpose

Turn the guarded CI route manifest into a concrete, non-executed command plan.

Runs `1415-1417` defined, validated, and stress-tested the route-level CI
policy. This run adds command templates for the four runnable CPU routes and
keeps the two blocked routes non-executable.

It does not run new FDTD/FWI inversions, execute the generated commands, launch
GPU/HPC work, compare against field data, or promote physical, field, or 3D
claims.

## Output

```text
outputs/experiments/1418_local_2d_state_consistent_repaired_execution_ci_route_command_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_rows.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_plan_summary.json
commands/local_2d_state_consistent_repaired_execution_ci_route_commands.sh
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_PLAN.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_plan.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan.py
```

## Result

```text
command rows:                      6
executable commands:               4
blocked commands:                  2
fast-smoke commands:               2
full-core gate commands:           2
commands executed:                 false
command plan ready:                true
full pack remains authoritative:   true
sentinel replaces full pack:       false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
ready for 3D/HPC:                  false
```

The generated command script contains:

| Route class | Commands | Role |
| --- | ---: | --- |
| reduced sentinel fast smoke | 2 | CPU fast smoke for consumer/schema/parsing/plotting changes |
| repaired full core gate | 2 | CPU full-core guard for row-key, digest, boundary, objective, margin, or token changes |
| blocked design review required | 1 | non-executable |
| blocked current evidence | 1 | non-executable |

## Interpretation

The route manifest now has concrete test-level command templates: two
reduced-sentinel fast-smoke commands, two repaired full-core gate commands, and
two blocked routes that remain non-executable.

The generated shell script is an execution aid, not an executed result. It
preserves the existing authority boundary: the 11-row sentinel is fast-smoke
only, and the 88-row full core table remains authoritative for boundary-
sensitive changes.

## Decision

Use run `1418` as the non-executed CI command plan. Execute only the four
runnable CPU test commands when CI validation is needed. Keep physical, GPU,
field, field FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_plan.py
5 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_plan.png
2572x837, dynamic range=255
```
