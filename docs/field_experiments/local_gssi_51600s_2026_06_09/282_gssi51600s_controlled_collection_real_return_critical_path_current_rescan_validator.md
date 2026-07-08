# Field Experiment 282: Critical-Path Current Rescan Validator

Date: 2026-06-28

## Purpose

Validate the saved run `281` current rescan from artifacts.

This run confirms the file, metadata, checksum, critical-path, downstream
guard, figure, and script-snapshot state recorded by the current rescan.

This is an artifact validator. It does not ingest real field data, run field
preprocessing, run FDTD, run field FWI, launch GPU/HPC work, or claim field
evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/282_gssi51600s_controlled_collection_real_return_critical_path_current_rescan_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_critical_path_current_rescan_validator_checks.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_validator_summary.json
figures/field_controlled_collection_real_return_critical_path_current_rescan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                       7
passed checks:                           7
failed checks:                           0
validation ready:                        true
required real files:                     9
real files present:                      0
metadata values required:                32
metadata values present:                 0
checksums required:                      9
checksums present:                       0
critical-path measured requirements:     50
critical-path measured complete:         0
acceptance gates:                        7
acceptance gates ready:                  0
provenance acceptance ready:             false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

## Interpretation

The saved run `281` current rescan is internally consistent: all measured
requirement counts remain zero, no unexpected files or placeholders are
present, and downstream field states remain blocked.

## Decision

Use runs `281-282` as the guarded current field inbox state. Real measured
files, metadata, and checksums remain required before provenance acceptance or
any field FWI, 3D/HPC, or GPU escalation.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_critical_path_current_rescan_validator.py
3 passed
```

Figure validation:

```text
3329x895, dynamic range=255
```
