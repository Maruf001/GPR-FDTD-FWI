# Experiment 1724: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template Pack

Date: 2026-06-30

## Purpose

Create output-local result JSON templates for the ten future observed-by-case
materialization jobs.

The templates are based on the run `1691-1693` execution contract. Each
template pre-fills stable job identity fields and leaves future solver,
runtime, shape, and hash fields blank. The templates are not written to the
external result paths and they do not count as materialized observed arrays or
accepted FDTD outputs.

This run does not create cache arrays, execute commands, run FDTD, start GPU
work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1724_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack
```

Key artifacts:

```text
templates/result_json/payload_*/ff_max_geometry_instability_*_observed_by_case.result.template.json
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_template_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack.png
scripts/
```

## Result

```text
source execution contract ready:       true
source validation ready:               true
source sensitivity ready:              true
templates:                              10
payloads:                                5
cases:                                   2
schema fields per template:             16
total schema fields:                   160
stable prefilled fields:                60
future-value placeholders:             100
template files written:                 10
template JSON key count min:            16
template JSON key count max:            16
output-local templates:                 10
external result files present:           0
template/external path overlaps:         0
templates accepted as results:           0
observed-by-case materialized:        false
result written:                       false
commands executed:                    false
new FDTD executed:                    false
execution permitted:                  false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
template pack ready:                  true
```

## Interpretation

The future result writer now has ten output-local JSON templates: one for each
payload/case job. The stable identity fields are filled, while the actual
solver output fields remain blank.

These templates are not evidence. They become useful only after an approved
materialization run creates real observed arrays and real result JSON files.

## Decision

Use these templates for result-writer preparation only. Keep observed-by-case
materialization and FDTD execution blocked until approval is completed and real
external outputs exist.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack.py

3 passed
```

Figure validation:

```text
2429x848, dynamic range=255
```
