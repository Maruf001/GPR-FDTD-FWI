# Field Experiment 281: Critical-Path Current Rescan

Date: 2026-06-28

## Purpose

Rescan the controlled collection return inbox against the guarded run
`278-280` critical-path block.

This run answers a current-state question:

```text
Have any real measured DZT files, measured metadata values, checksums, or
acceptance gates appeared since the guarded critical-path block was created?
```

This is a current-state scan. It does not ingest real field data, run field
preprocessing, run FDTD, run field FWI, launch GPU/HPC work, or claim field
evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/281_gssi51600s_controlled_collection_real_return_critical_path_current_rescan
```

Key artifacts:

```text
data/field_controlled_collection_real_return_critical_path_current_rescan_file_rows.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_metadata_rows.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_checksum_rows.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_unexpected_rows.csv
data/field_controlled_collection_real_return_critical_path_current_rescan_summary.json
figures/field_controlled_collection_real_return_critical_path_current_rescan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source critical path guarded:             true
required real files:                      9
real files present:                       0
metadata values required:                 32
metadata values present:                  0
checksums required:                       9
checksums present:                        0
unexpected files:                         0
critical-path measured requirements:      50
critical-path measured complete:          0
critical-path acceptance gates:           7
critical-path acceptance gates ready:     0
current rescan ready:                     true
provenance acceptance ready:              false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

## Interpretation

The current return inbox still has zero of nine real DZT files, zero of 32
measured metadata values, and zero of nine checksums. The guarded critical path
therefore remains at zero of 50 measured requirements and zero of seven
acceptance gates complete.

## Decision

Keep provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, 3D/HPC, and GPU work blocked until real measured files, metadata,
and checksums are staged.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_critical_path_current_rescan.py
3 passed
```

Figure validation:

```text
2789x883, dynamic range=255
```
