# Experiment 1727: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template-Pack External Result Path Guard

Date: 2026-06-30

## Purpose

Audit the locked external result paths after the run `1724` result JSON
template pack and the run `1725-1726` validator/sensitivity block.

This guard checks that the ten result JSON templates remain output-local
preparation files and did not become external result files, overlap external
result paths, or sit under the external result root.

This run does not materialize observed arrays, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1727_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_guard_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard.png
scripts/
```

## Result

```text
guard rows:                         10
payloads:                            5
cases:                               2
template files exist:               10
output-local templates:             10
external result files exist:         0
manifest external-result rows:       0
manifest overlap rows:               0
computed template/external equals:   0
templates under external root:       0
external paths under external root: 10
templates accepting as result:       0
row FDTD executed count:             0
observed-by-case materialized:   false
result written:                  false
new FDTD executed:               false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
guard ready:                      true
```

## Interpretation

The result JSON templates remain preparation inventory only. They exist in the
synthetic 2D output archive, while the locked external result paths remain
empty. No observed arrays, result files, FDTD execution, or downstream evidence
state is promoted.

## Decision

Keep the result JSON templates as preparation inventory only. Observed-by-case
materialization and FDTD execution remain blocked until real approved result
files exist.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard.py

3 passed
```

Figure validation:

```text
2285x846, dynamic range=255
```
