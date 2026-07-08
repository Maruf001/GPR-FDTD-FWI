# Field Experiment 151: Recovered-Session Collection Scaffold

Date: 2026-06-18

## Purpose

Apply the session metadata recovered in run `150` to the controlled collection
scaffold from run `147`, producing a better worksheet for a future controlled
2D field collection.

This is CPU-only packet synthesis and validation. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/151_gssi51600s_recovered_session_collection_scaffold
```

Key artifacts:

```text
packet_scaffold_recovered_session/
data/recovered_session_collection_scaffold_summary.json
data/recovered_session_collection_scaffold_evidence.csv
data/recovered_session_collection_scaffold_table_delta.csv
data/controlled_2d_packet_validation_findings.csv
data/controlled_2d_packet_table_status.csv
data/controlled_2d_packet_acceptance_status.csv
figures/gssi51600s_recovered_session_collection_scaffold.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_recovered_session_collection_scaffold
source scaffold run:                   147_gssi51600s_controlled_collection_scaffold
source recovery run:                   150_gssi51600s_current_archive_metadata_recovery
candidate session prefill fields:      4
applied session prefill fields:        4
before missing required values:        60
after missing required values:         56
missing-required delta:                -4
before session missing required:       6
after session missing required:        2
session missing-required delta:        -4
after dtype failures:                  0
after cross-table failures:            0
ready for collection:                  true
ready for packet acceptance:           false
ready for current archive field FWI:   false
ready for heavy field work:            false
ready for field 3D/HPC:                false
gpu priority:                          none
```

Recovered session fields applied to the scaffold:

```text
antenna_serial  = 3385
software_version = 1.4.35
gain_setting = 0
time_range_ns = 5.0
```

Validation delta:

```text
session_log:            missing required 6 -> 2
target_truth:           missing required 9 -> 9
profile_geometry:       missing required 6 -> 6
acquisition_run:        missing required 9 -> 9
reference_measurement:  missing required 30 -> 30
```

## Interpretation

Run `151` improves the field worksheet, not the inversion state. The future
controlled collection can start from the same-system recovered session
metadata, with a note to verify or update those fields on collection day.

The remaining blockers are still the substantive ones: collection date and
operator verification, measured target truth, surveyed profile geometry,
controlled Tx/Rx offset, coupling condition, measured time-zero references,
and amplitude references. The packet is not accepted, and field FWI/heavy
field work/3D remain blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_recovered_session_collection_scaffold.py
4 passed
```

Figure validation:

```text
gssi51600s_recovered_session_collection_scaffold.png: 2569x937,
nonwhite=0.3524, dynamic range=255
```
