# Field Experiment 621: External Return Hygiene Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `620` validator using damaged or prematurely promoted
states.

The sensitivity set checks readiness damage, missing leaf directories,
unexpected directories, false file presence, false symlink presence, slot-count
damage, writable-count damage, field-evidence promotion, field FWI promotion,
field 3D promotion, GPU-priority promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/621_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validation_sensitivity.png
scripts/
```

## Result

```text
sensitivity scenarios:                   16
expected pass scenarios:                 1
expected fail scenarios:                 15
observed pass scenarios:                 1
observed fail scenarios:                 15
unexpected outcomes:                     0
damaged scenarios:                       15
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
```

## Decision

The validator accepts only the exact clean empty tree and rejects damaged or
prematurely promoted states. Use runs `619-621` as the guarded no-data
external-return hygiene block.

## Validation

Figure check:

```text
2825x851, dynamic range=255
```

Script snapshots:

```text
2
```
