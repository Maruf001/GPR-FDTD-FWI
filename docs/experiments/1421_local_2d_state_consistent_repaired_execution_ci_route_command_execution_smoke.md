# Local 2D Experiment 1421: Repaired Execution CI Route Command Execution Smoke

Date: 2026-06-28

## Purpose

Execute the four runnable CPU pytest command rows from run `1418` and confirm
that the two blocked routes remain unexecuted.

Run `1418` created a non-executed command plan. Runs `1419-1420` validated and
stress-tested that plan. This run executes only the CPU commands that the plan
marked runnable.

It does not run new FDTD/FWI inversions, launch GPU/HPC work, compare against
field data, or promote physical, field, or 3D claims.

## Output

```text
outputs/experiments/1421_local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_rows.csv
data/local_2d_state_consistent_repaired_execution_ci_route_command_execution_summary.json
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CI_ROUTE_COMMAND_EXECUTION_SMOKE.md
scripts/run_local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke.py
scripts/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke.py
```

## Result

```text
execution rows:                     6
executable commands:                4
executed commands:                  4
passed executable commands:         4
failed executable commands:         0
blocked routes not executed:        2
unexpected blocked executions:      0
fast-smoke commands executed:       2
full-core commands executed:        2
execution smoke ready:              true
full pack remains authoritative:    true
sentinel replaces full pack:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Command outcomes:

| Route | Command group | Outcome |
| ---: | --- | --- |
| 1 | reduced_sentinel_fast_smoke | 9 tests passed |
| 2 | reduced_sentinel_fast_smoke | 9 tests passed |
| 3 | repaired_full_core_gate | 26 tests passed |
| 4 | repaired_full_core_gate | 26 tests passed |
| 5 | blocked_design_review_required | not executed |
| 6 | blocked_current_evidence | not executed |

## Interpretation

The runnable repaired 2D CI command rows execute successfully on CPU. The two
blocked routes remain unexecuted, the full 88-row pack remains authoritative
for boundary-sensitive routes, and the reduced sentinel remains fast-smoke
only.

## Decision

Use run `1421` as the executed CPU smoke for the repaired 2D CI route plan. Do
not promote physical, GPU, field-transfer, field-FWI, or 3D/HPC claims from
this smoke.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke.py
5 passed
```

Executed command rows:

```text
reduced sentinel command, route 1: 9 passed
reduced sentinel command, route 2: 9 passed
full core command, route 3:       26 passed
full core command, route 4:       26 passed
```

Figure validation:

```text
figures/local_2d_state_consistent_repaired_execution_ci_route_command_execution_smoke.png
3112x837, dynamic range=255
```
