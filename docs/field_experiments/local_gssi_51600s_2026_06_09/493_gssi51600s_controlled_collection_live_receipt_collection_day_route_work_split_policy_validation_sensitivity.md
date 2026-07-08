# Field Experiment 493: Controlled Collection Live Receipt Collection-Day Route Work-Split Policy Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `492` validator by mutating the run `491` work-split
policy artifacts.

The sensitivity audit checks that the validator accepts the exact policy and
rejects damaged readiness, stage-count, file-count, receipt-check, timing,
promotion, figure, and script-snapshot states.

This is a CPU-only artifact sensitivity audit. It does not create live files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/493_gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                    16
expected pass cases:       1
expected fail cases:      15
actual pass cases:         1
actual fail cases:        15
unexpected cases:          0
exact source passes:       true
damaged cases rejected:    true
field FWI ready:           false
field 3D/HPC ready:        false
gpu priority:              none
sensitivity ready:         true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact_source | pass | pass |
| policy_ready_false | fail | fail |
| source_validation_false | fail | fail |
| stage_removed | fail | fail |
| prefill_file_count_damage | fail | fail |
| prefill_check_count_damage | fail | fail |
| measurement_dependent_count_damage | fail | fail |
| prefill_timing_flag_damage | fail | fail |
| measured_dzt_dependency_damage | fail | fail |
| stage_unlocks_promotion | fail | fail |
| partial_delivery_promotes_parser | fail | fail |
| all_files_gate_removed | fail | fail |
| field_fwi_promotion | fail | fail |
| field_3d_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator is sensitive to the failure modes that matter for the collection
route. It rejects attempts to treat partial delivery as parser-ready, rejects
field FWI or field 3D/HPC promotion, and rejects damaged file and receipt-check
counts.

## Decision

Keep the work-split policy as a guarded field collection planning artifact. It
does not authorize field FWI, GPU work, or field 3D/HPC from the current dry
field packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_work_split_policy_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_work_split_policy_validation_sensitivity.py

6 passed
```

Figure validation:

```text
2284x857, dynamic range=255
```
