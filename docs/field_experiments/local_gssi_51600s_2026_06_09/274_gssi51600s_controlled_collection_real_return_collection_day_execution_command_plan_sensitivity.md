# Field Experiment 274: Controlled Collection-Day Execution Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `273` validator for the saved run `272` controlled
collection-day execution command plan.

This is an artifact-only sensitivity run. It mutates saved command-plan rows,
summary values, figure metadata, script snapshots, and command-script text in
memory. It does not ingest real field data, run field FWI, launch 3D/HPC work,
or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/274_gssi51600s_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_EXECUTION_COMMAND_PLAN_SENSITIVITY.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        15
observed failure scenarios:        15
unexpected outcomes:               0
sensitivity ready:                 true
exact run 272 accepted:            true
damaged variants rejected:         true
real files present:                false
metadata values present:           false
checksums present:                 false
provenance acceptance ready:       false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The damaged variants cover source-count drift, phase drift, accidental command
execution, command-script drift, downstream promotion, figure drift, and
script-snapshot drift.

## Interpretation

The controlled collection-day execution plan is now guarded as a non-executed
field work plan. The exact run `272` artifact passes, while every damaged
variant fails as expected.

This strengthens the operational gate. It still does not create measured field
evidence because the archive has not yet received the nine required real DZT
files, 32 measured metadata values, or nine checksums.

## Decision

Use runs `272-274` as the guarded non-executed field collection-day command-plan
block. Real files, measured metadata, and checksums remain required before any
field evidence, field FWI, 3D/HPC, or GPU escalation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan_sensitivity.py
3 passed
```

Figure validation:

```text
3473x895, dynamic range=255
```
