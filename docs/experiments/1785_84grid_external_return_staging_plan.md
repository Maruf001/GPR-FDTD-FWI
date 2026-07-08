# Experiment 1785: 84-Grid External Return Staging Plan

Date: 2026-07-01

## Purpose

Create a non-executed staging plan for the 84-grid external returns identified
by runs `1782-1784`.

This run does not create a real approval token, does not create cache arrays,
does not create result JSON files, does not stage files into the live external
return area, does not execute copy commands, does not materialize observed-by-
case data, and does not execute FDTD.

## Output

```text
outputs/experiments/1785_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_item_staging_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:       true
source validation ready:           true
source sensitivity ready:          true
staging items:                     21
stages:                            5
approval token required:           1
cache arrays required:             10
result JSON files required:        10
artifact jobs required:            10
template copy allowed:             0
real approval token present:       0
real cache arrays present:         0
real result JSON files present:    0
live files present:                0
ready to stage items:              0
copy commands:                     21
executed commands:                 0
action groups:                     6
ready action groups:               0
ready for materialization:         false
new FDTD executed:                 false
gpu priority:                      none
```

Action groups:

| Order | Action | Required items | Required jobs | Ready now |
| ---: | --- | ---: | ---: | --- |
| 1 | produce real approval token | 1 | 0 | false |
| 2 | produce real cache arrays | 10 | 10 | false |
| 3 | produce real result JSON files | 10 | 10 | false |
| 4 | preflight approval and paired artifact jobs | 21 | 10 | false |
| 5 | stage only real external files into live paths | 21 | 10 | false |
| 6 | rerun live intake and materialization gates | 21 | 10 | false |

## Interpretation

The 84-grid external-return handoff is now reduced to one approval token, ten
cache arrays, ten result JSON files, twenty-one exact live-path copy commands,
and six guarded action groups.

The commands are intentionally non-executed. Output-local templates are
non-evidence, and cache arrays are not templated because they must come from
real FDTD execution.

## Decision

Use run `1785` as the non-executed staging plan for future 84-grid
external-return files. Keep materialization and FDTD execution blocked until
the real approval token, ten real cache arrays, and ten real result JSON files
pass guarded live intake.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
