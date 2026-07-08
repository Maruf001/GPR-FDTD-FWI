# Field Experiment 319: Real-Return Packet Staging Dependency Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `318` controlled field staging-plan validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `317` staging plan and
rejects changes that would alter the stage order, dependency graph,
missing-item counts, field decision states, GPU priority, figure validation, or
script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/319_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                     16
expected pass:                 1
observed pass:                 1
expected failures:             15
observed failures:             15
unexpected outcomes:           0
sensitivity ready:             true
accepts exact run 317:         true
rejects damaged variants:      true
controlled evidence ready:     false
field FWI ready:               false
field 3D/HPC ready:            false
gpu priority:                  none
```

## Interpretation

The run `318` validator accepts the exact run `317` staging plan and rejects
controlled damaged variants for stage-count drift, stage-order drift,
missing-count drift, dependency-graph drift, readiness promotion, field-state
promotion, GPU-priority drift, figure drift, and script-snapshot drift.

## Decision

Use runs `317-319` as the guarded controlled-field return-packet staging
dependency block. Keep provenance acceptance, archive acceptance, field
evidence, field FWI, GPU work, and field 3D/HPC blocked until real measured
packet items pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3653x922, dynamic range=255
```
