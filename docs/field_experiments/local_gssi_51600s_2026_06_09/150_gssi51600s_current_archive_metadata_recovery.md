# Field Experiment 150: Current Archive Metadata Recovery

Date: 2026-06-18

## Purpose

Recover any defensible current-archive packet metadata that exists in the raw
GSSI DZX sidecars but was not mapped into the run `143` current-archive packet
prefill. This tests the run `146` note that only session metadata may be
recoverable from the existing archive.

This is CPU-only packet recovery and validation. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/150_gssi51600s_current_archive_metadata_recovery
```

Key artifacts:

```text
packet_recovered/
data/current_archive_metadata_recovery_summary.json
data/current_archive_metadata_recovery_evidence.csv
data/current_archive_dzx_recovery_metadata.csv
data/current_archive_metadata_recovery_table_delta.csv
data/controlled_2d_packet_validation_findings.csv
data/controlled_2d_packet_table_status.csv
data/controlled_2d_packet_acceptance_status.csv
figures/gssi51600s_current_archive_metadata_recovery.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_current_archive_metadata_recovery
DZX sidecars scanned:                 4
recoverable fields found:             2
applied recovered fields:             2
before missing required values:       67
after missing required values:        65
missing-required delta:               -2
before session missing required:      3
after session missing required:       1
session missing-required delta:       -2
after dtype failures:                 0
after cross-table failures:           0
acceptance gates:                     7
ready for packet acceptance:          false
ready for current archive field FWI:  false
ready for heavy field work:           false
ready for field 3D/HPC:               false
gpu priority:                         none
```

Recovered evidence:

```text
session_log.antenna_serial <- DZX antSerialNumber = 3385
session_log.gain_setting   <- DZX displayGain     = 0
session_log.operator       <- not present in DZX/DZT strings
```

Validation delta:

```text
session_log:            missing required 3 -> 1
target_truth:           missing required 10 -> 10
profile_geometry:       missing required 24 -> 24
acquisition_run:        missing required 20 -> 20
reference_measurement:  missing required 10 -> 10
```

## Interpretation

The raw DZX sidecars add real, defensible provenance: antenna serial `3385`
and display gain `0`, both consistent across all four profiles. The recovered
packet copy is therefore a better current-archive packet than run `143`.

This does not change the field-inversion decision. The packet still lacks
operator, known target truth, surveyed profile endpoints, target crossings,
controlled Tx/Rx offset, coupling condition, external time-zero references,
and amplitude references. Field FWI, heavy field compute, and field 3D/HPC
remain blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_current_archive_metadata_recovery.py
4 passed
```

Figure validation:

```text
gssi51600s_current_archive_metadata_recovery.png: 2569x937,
nonwhite=0.3265, dynamic range=255
```
