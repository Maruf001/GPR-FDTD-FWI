# Experiment 1726: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1725` validator for the run `1724` observed-by-case
materialization result JSON template pack.

This run asks whether the validator only accepts the exact output-local result
template pack and rejects damaged schema, payload, result-file, execution,
downstream, figure, and script-snapshot states.

This run does not create cache arrays, materialize observed arrays, execute
commands, run FDTD, start GPU work, transfer to field work, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1726_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                         22
expected pass cases:             1
expected fail cases:            21
actual pass cases:               1
actual fail cases:              21
unexpected cases:                0
exact source passes:          true
damaged cases rejected:       true
observed-by-case materialized: false
new FDTD executed:             false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
validation sensitivity ready:  true
```

The sensitivity cases cover source-readiness damage, row removal, payload and
case count damage, schema damage, placeholder damage, template-written damage,
hash damage, missing payload files, false external-result promotion, path
overlap, false result acceptance, materialization promotion, FDTD promotion,
GPU/field/3D promotion, figure damage, and script-snapshot damage.

## Interpretation

The result-template validator now rejects all tested damaged states. The
template pack remains preparation-only evidence: it defines output-local result
JSON placeholders for a future approved executor path, but it does not produce
measured or simulated observed arrays.

## Decision

Keep run `1724` as a result-template preparation artifact only. Do not treat
it as observed-by-case materialization evidence, FDTD execution evidence, or a
downstream GPU/field/3D readiness signal.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2500x868, dynamic range=255
```
