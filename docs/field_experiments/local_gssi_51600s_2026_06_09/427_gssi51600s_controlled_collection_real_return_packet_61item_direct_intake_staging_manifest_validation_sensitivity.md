# Field Experiment 427: Direct Intake Staging Manifest Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `426` validator for the run `425` direct-intake staging
manifest.

Run `426` validated the staging manifest. This run verifies that the validator
rejects damaged counts, template or synthetic substitution, staged-file
promotion, action-order drift, downstream evidence promotion, figure damage,
and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/427_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                          9
expected pass scenarios:                        1
expected failure scenarios:                     8
unexpected scenarios:                           0
direct-intake validation sensitivity ready:     true
exact source artifacts pass:                    true
template substitution rejected:                 true
downstream promotion rejected:                  true
real packet files present:                      false
controlled field evidence ready:                false
field FWI ready:                                false
field 3D/HPC ready:                             false
GPU priority:                                   none
```

The exact run `425` artifacts pass. Damaged variants fail as expected for slot
count drift, DZT group-count drift, template substitution, staged-file
promotion, action-order drift, downstream evidence promotion, figure damage,
and script-snapshot damage.

## Decision

Use runs `425-427` as the guarded direct-intake staging-manifest block. The
field stream still requires real files to be staged and accepted before
provenance, archive, evidence, field FWI, GPU work, or 3D/HPC can proceed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validation_sensitivity.py
12 passed
```

Figure check:

```text
2393x854, dynamic range=255
```
