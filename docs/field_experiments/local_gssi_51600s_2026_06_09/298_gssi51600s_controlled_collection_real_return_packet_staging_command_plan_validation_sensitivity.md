# Field Experiment 298: Real Return Packet Staging Command Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `297` field staging-plan validator with controlled damaged
variants.

The exact run `296` plan should pass. Damaged variants should fail when they
change plan counts, phase order, dependencies, expected output counts,
non-execution semantics, source links, measured-completion state, field
readiness state, GPU priority, figure validation, or script snapshots.

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/298_gssi51600s_controlled_collection_real_return_packet_staging_command_plan_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_staging_command_plan_validation_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_packet_staging_command_plan_validation_sensitivity_summary.json
figures/field_controlled_collection_real_return_packet_staging_command_plan_validation_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_STAGING_COMMAND_PLAN_VALIDATION_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    16
expected pass:                1
observed pass:                1
expected failures:            15
observed failures:            15
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 296:        true
rejects damaged variants:     true
real packet files present:    false
real return execution ready:  false
provenance acceptance ready:  false
real archive acceptance ready: false
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
GPU priority:                 none
figure size:                  3473x913
figure dynamic range:         255
```

The validator rejects all damaged variants:

| Scenario | Expected | Observed |
| --- | --- | --- |
| exact run 296 inputs | pass | pass |
| policy label drift | fail | fail |
| phase count drift | fail | fail |
| phase order drift | fail | fail |
| dependency drift | fail | fail |
| output count drift | fail | fail |
| command execution promotion | fail | fail |
| command uncommented | fail | fail |
| source contract link drift | fail | fail |
| measured completion promotion | fail | fail |
| real packet promotion | fail | fail |
| provenance promotion | fail | fail |
| downstream promotion | fail | fail |
| GPU priority drift | fail | fail |
| figure validation drift | fail | fail |
| script snapshot drift | fail | fail |

## Interpretation

The run `297` validator accepts the exact run `296` field packet staging plan
and rejects controlled damaged variants for plan-count drift, phase-order drift,
dependency drift, output-count drift, command execution promotion, uncommented
command text, source-link drift, false measured completion, false field-state
promotion, GPU-priority drift, figure drift, and script-snapshot drift.

## Decision

Use runs `296-298` as the guarded field real-return packet staging command-plan
block. Keep provenance acceptance, real archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, and GPU work blocked until the measured
packet is staged and validators pass.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_command_plan_validation_sensitivity.py
3 passed
```
