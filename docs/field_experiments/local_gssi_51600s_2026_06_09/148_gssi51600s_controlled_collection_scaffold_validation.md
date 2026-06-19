# Field Experiment 148: Controlled Collection Scaffold Validation

Date: 2026-06-18

## Purpose

Validate the run `147` controlled-collection scaffold with the existing
controlled-2D packet validator. This confirms whether the planned IDs and
cross-table links are coherent, while preserving the fact that measured values
are still blank.

This is CPU-only packet validation. It does not run FDTD, FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/148_gssi51600s_controlled_collection_scaffold_validation
```

Key artifacts:

```text
data/controlled_2d_packet_validation_summary.json
data/controlled_2d_packet_table_status.csv
data/controlled_2d_packet_acceptance_status.csv
data/controlled_2d_packet_validation_findings.csv
```

## Result

```text
policy label:                         gssi51600s_controlled_2d_packet_validator
packet rows:                          12
filled rows:                          12
required-field evaluations:           119
blocking findings:                    60
missing required values:              60
dtype failures:                       0
cross-table failures:                 0
acceptance gates ready:               0 / 7
ready for packet acceptance:          false
ready for current archive field FWI:  false
ready for heavy field work:           false
ready for field 3D/HPC:               false
gpu priority:                         none
```

Table-level blockers:

```text
session_log:            6 missing required fields
target_truth:           9 missing required fields
profile_geometry:       6 missing required fields
acquisition_run:        9 missing required fields
reference_measurement: 30 missing required fields
```

## Interpretation

The scaffold has coherent planned row IDs and cross-table links: all scaffold
rows are filled enough to be recognized, and there are no dtype or cross-table
failures. It is still not an accepted packet because measured target geometry,
survey fields, Tx/Rx/coupling fields, time-zero values, amplitude metrics, and
session details remain blank.

Current-archive field FWI, heavy field GPU work, and field 3D/HPC remain
blocked.

## Validation

Executed:

```text
conda run -n gpr-fdtd-fwi python run_gssi_field_controlled_2d_packet_validator.py \
  --packet-dir outputs/field_experiments/local_gssi_51600s_2026_06_09/147_gssi51600s_controlled_collection_scaffold/packet_scaffold \
  --run-name gssi51600s_controlled_collection_scaffold_validation
```
