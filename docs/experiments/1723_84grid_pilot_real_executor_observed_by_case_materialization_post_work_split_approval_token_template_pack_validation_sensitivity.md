# Experiment 1723: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split Approval-Token Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1722` approval-token template-pack validator.

The sensitivity run mutates the validated artifacts in memory and checks
whether the validator rejects damaged states. The damage cases cover source
readiness, template rows, schema shape, placeholder count, template placement,
missing payloads, false external approval, false materialization readiness,
FDTD execution promotion, downstream promotion, figure damage, and missing
script snapshots.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1723_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                         20
expected pass cases:            1
expected fail cases:           19
actual pass cases:              1
actual fail cases:             19
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:        true
ready for materialization:     false
new FDTD executed:             false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
sensitivity ready:             true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact source | pass | pass |
| source readiness false | fail | fail |
| template row removed | fail | fail |
| schema field count damaged | fail | fail |
| placeholder count damaged | fail | fail |
| template written damaged | fail | fail |
| output-local placement damaged | fail | fail |
| template payload missing | fail | fail |
| external approval promoted | fail | fail |
| template overlaps external path | fail | fail |
| template accepted as external approval | fail | fail |
| external item present | fail | fail |
| materialization promoted | fail | fail |
| FDTD execution promoted | fail | fail |
| GPU promoted | fail | fail |
| field transfer promoted | fail | fail |
| field FWI promoted | fail | fail |
| 3D/HPC promoted | fail | fail |
| figure dynamic range removed | fail | fail |
| script snapshots removed | fail | fail |

## Interpretation

The validator is sensitive to the failure modes that would make a planning
template look like approval or evidence. It accepts only the exact output-local
template pack and rejects false external approval, false materialization,
FDTD/downstream promotion, damaged figures, and missing script snapshots.

## Decision

Keep the template as preparation only. Do not treat it as approval or FDTD
evidence. Observed-by-case materialization remains blocked until the completed
external approval token and all planned materialization artifacts pass their
gates.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_approval_token_template_pack_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2428x871, dynamic range=255
```
