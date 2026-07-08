# Field Experiment 466: Live Receipt Verifier Current-State Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `465` live receipt verifier current-state validator.

Run `465` validated the current-state receipt report from run `464`. This run
checks that the validator rejects damaged source readiness, report shape, live
file promotion, missing-count drift, receipt-readiness promotion, downstream
promotion, figure damage, and script-snapshot damage.

This run does not copy measured files, accept field evidence, rerun the parser,
rerun provenance, rerun archive acceptance, launch field FWI, launch GPU work,
or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/466_gssi51600s_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
sensitivity cases:                     9
expected pass cases:                   1
expected fail cases:                   8
actual pass cases:                     1
actual fail cases:                     8
unexpected cases:                      0
damaged cases:                         8
parser ready:                          false
provenance ready:                      false
archive ready:                         false
field FWI ready:                       false
field 3D/HPC ready:                    false
sensitivity ready:                     true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| source_ready_false | source audit readiness false |
| receipt_shape_damage | one receipt report row removed |
| live_file_promotion | receipt report marks one live file present |
| missing_count_drift | missing file count drifts from 33 |
| receipt_ready_promotion | receipt ready count promoted |
| downstream_promotion | field FWI readiness promoted |
| figure_damage | figure path missing |
| script_snapshot_damage | script snapshot count missing |

## Interpretation

The live receipt verifier block is now sensitivity-hardened. The validator
accepts only the exact current-state report and rejects damaged receipt-shape,
file-presence, readiness, downstream, figure, and script-snapshot states.

## Decision

Use runs `464`-`466` as the guarded live receipt verifier block. Do not rerun
parser, provenance, archive acceptance, field FWI, GPU work, or field 3D/HPC
until all 33 receipt rows pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity.py
3 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
