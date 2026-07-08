# Field Experiment 538: Measured-DZT Live Collection Manifest Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `537` validator.

The sensitivity cases check whether the validator rejects damaged manifest
shape, family-count damage, false live-DZT promotion, placeholder creation,
false family completion, false live receipt, false parser readiness, false
field FWI, false field 3D/HPC, damaged figures, and missing script snapshots.

This is CPU-only validation sensitivity. It does not ingest DZT files, run a
parser, accept provenance, launch field FWI, launch GPU work, or promote field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/538_gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_collection_manifest_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              15
expected pass cases:                 1
expected fail cases:                14
actual pass cases:                   1
actual fail cases:                  14
unexpected cases:                    0
damaged cases:                      14
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Interpretation

The validator accepts only the exact no-live-DZT manifest state. It rejects
placeholders and false measured-evidence promotion.

## Decision

Use runs `536-538` as the guarded measured-DZT collection manifest block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_collection_manifest_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x855, dynamic range=255
```
