# Experiment 1665: 84-Grid Pilot Revised Real-Result Command Plan

Date: 2026-06-30

## Purpose

Convert the revised five-row pilot checklist from run `1664` into a concrete
set of validation commands for future real-result JSON files.

Run `1664` refreshed the producer checklist around payload rows
`1;23;46;68;72`. This run builds the matching command plan while keeping every
command non-executed because the real-result JSON files do not exist yet.

This run does not execute FDTD, fill result files, accept pilot evidence,
launch GPU work, transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1665_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan_command_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source revised checklist ready:        true
command count:                         5
required field count:                  50
required payload IDs:                  1;23;46;68;72
contains payload 68:                   true
contains stale payload 86:             false
contains retained_blend:               false
commands executed:                     0
JSON file checks ready:                0
command actions:                       3
ready command actions:                 0
fillable templates refreshed:          false
real executor script available:        false
new FDTD executions:                   false
GPU work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
command plan ready:                    true
```

The five planned commands target the revised pilot payload rows:

| Command order | Payload row | Objective profile | Transition bin |
| ---: | ---: | --- | ---: |
| 1 | 1 | highband | 0 |
| 2 | 23 | late | 4 |
| 3 | 46 | late_high | 9 |
| 4 | 68 | veryhigh | 13 |
| 5 | 72 | veryhigh | 17 |

Each command checks that the staged JSON file exists, can be parsed by
`python -m json.tool`, and can be checksummed.

## Interpretation

The revised execution-preparation path is internally consistent through the
command-plan layer. It now includes payload row `68` and excludes stale payload
row `86` and the unsupported `retained_blend` label.

The plan is intentionally not a real execution result. None of the five staged
JSON files exists yet, no command has been run, and the fillable templates still
need to be refreshed from the same revised payload set.

## Decision

Use run `1665` as the revised command-plan source. The next defensible step is
to refresh the fillable template pack around payload rows `1;23;46;68;72`;
after that, validate the revised checklist, commands, and templates as one
coherent intake package before any real FDTD executor work.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_command_plan.py
5 passed
```

Figure check:

```text
2213x847, dynamic range=255
```
