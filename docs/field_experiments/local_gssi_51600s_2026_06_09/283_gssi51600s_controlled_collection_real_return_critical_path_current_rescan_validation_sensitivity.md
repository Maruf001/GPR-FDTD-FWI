# Field Experiment 283: Critical-Path Current Rescan Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `282` current-rescan validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `281` rescan and
rejects damaged versions with file-count drift, metadata-count drift, false
file presence, checksum-count drift, unexpected files, false downstream
promotion, invalid figure metadata, and missing script snapshots.

This is an artifact sensitivity test. It does not ingest real field data, run
field preprocessing, run FDTD, run field FWI, launch GPU/HPC work, or claim
field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/283_gssi51600s_controlled_collection_real_return_critical_path_current_rescan_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_critical_path_current_rescan_validation_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_validation_sensitivity_summary.json
figures/field_controlled_collection_real_return_critical_path_current_rescan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    9
expected pass:                1
observed pass:                1
expected failures:            8
observed failures:            8
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 281:        true
rejects damaged variants:     true
provenance acceptance ready:  false
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
gpu priority:                 none
```

## Interpretation

The current-rescan validator accepts the exact run `281` rescan and rejects
damaged variants covering count drift, false file or checksum presence,
unexpected files, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `281-283` as the guarded current field inbox state. Real measured
files, metadata values, and checksums remain required before provenance
acceptance, field evidence, field FWI, 3D/HPC, or GPU work.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_critical_path_current_rescan_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3257x891, dynamic range=255
```
