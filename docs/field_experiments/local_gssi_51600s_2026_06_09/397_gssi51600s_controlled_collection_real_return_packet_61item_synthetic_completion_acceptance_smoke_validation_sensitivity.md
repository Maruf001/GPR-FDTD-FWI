# Field Experiment 397: Synthetic Completion Acceptance Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `396` validator against controlled damage to the run `395`
synthetic completion-smoke artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/397_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validation_sensitivity.png
```

## Result

```text
sensitivity scenarios:                  31
expected pass scenarios:                 1
observed pass scenarios:                 1
expected failure scenarios:              30
observed failure scenarios:              30
unexpected outcomes:                     0
validation sensitivity ready:            true
validator accepts exact run 395:         true
validator rejects damaged variants:      true
synthetic only:                          true
real packet files present:               false
provenance acceptance ready:             false
archive acceptance ready:                false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The damaged variants cover count drift, source-readiness drift, completion
syntax drift, evidence-state drift, downstream promotion, figure drift, and
missing script snapshots. The exact run `395` passes and all damaged variants
fail as expected.

## Decision

Use runs `395-397` as the guarded synthetic field intake acceptance-path smoke
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x883, dynamic range=255
```
