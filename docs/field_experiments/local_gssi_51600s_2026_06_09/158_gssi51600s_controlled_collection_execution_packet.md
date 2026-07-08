# Field Experiment 158: Controlled Collection Execution Packet

Date: 2026-06-22

## Purpose

Convert the run `156` critical path into an execution-grade controlled
two-dimensional field packet. The goal is to prefill the minimum row IDs and
cross-table links before a real field session, so the collection team can enter
measurements without inventing identifiers or breaking packet joins.

This is CPU-only planning and validation. It does not run DZT preprocessing,
finite-difference time-domain simulation, full-waveform inversion, GPU kernels,
field full-waveform inversion, three-dimensional/high-performance-computing
work, or neural-network training.

Run `157` was a same-turn draft of the same packet before reference-gap labels
were separated by blocker type. Run `158` is the final output for this
checkpoint.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/158_gssi51600s_controlled_collection_execution_packet
```

Key artifacts:

```text
packet/session_log.csv
packet/target_truth.csv
packet/profile_geometry.csv
packet/acquisition_run.csv
packet/reference_measurement.csv
data/field_controlled_collection_execution_packet_row_index.csv
data/field_controlled_collection_execution_steps.csv
data/field_controlled_collection_remaining_required_fields.csv
data/field_controlled_collection_execution_table_status.csv
data/field_controlled_collection_execution_acceptance_status.csv
data/field_controlled_collection_execution_packet_summary.json
docs/FIELD_COLLECTION_EXECUTION_PACKET.md
```

## Result

```text
policy label:                         gssi51600s_controlled_collection_execution_packet
source critical path:                 gssi51600s_controlled_collection_critical_path
packet tables:                        5
planned packet rows:                  12
planned sessions:                     1
planned target-truth rows:            1
planned profiles:                     1
planned controlled repeat profiles:   3
planned time-zero references:         3
planned amplitude references:         3
missing required values:              51
data-type failures:                   0
cross-table failures:                 0
cross-table links prefilled:          true
acceptance gates:                     7
ready acceptance gates:               0
ready for collection execution:       true
ready for packet acceptance:          false
ready for current-archive field FWI:  false
ready for heavy field work:           false
ready for field 3D/HPC:               false
gpu priority:                         none
```

The planned packet fixes the following minimum structure:

```text
1 session row
1 target-truth row
1 surveyed profile row
3 controlled acquisition-repeat rows
3 time-zero reference rows
3 amplitude-reference rows
```

The acquisition rows already link to the target, profile, and reference IDs.
The validator reports zero cross-table failures, so the packet structure is
internally coherent before collection.

## Remaining Required Values

The packet is intentionally not accepted yet. The remaining blockers are real
measurements and metadata that must be collected or verified:

```text
session_log:           9 missing required values
target_truth:          9 missing required values
profile_geometry:      6 missing required values
acquisition_run:       9 missing required values
reference_measurement: 18 missing required values
```

Reference gaps are now split by blocker type:

```text
reference_registry:    reference file names
time_zero_reference:   measured time zero and uncertainty
amplitude_reference:   amplitude metric and repeatability
```

## Interpretation

This is the right field-side next checkpoint after run `156`. The project now
has a concrete controlled-collection packet rather than only a critical-path
description. A future field session can fill the packet and rerun the validator
without changing IDs or redesigning the table structure.

The result does not change the scientific boundary:

- Supported: the next controlled two-dimensional field collection has an
  execution packet with prefilled IDs and valid joins.
- Not supported: packet acceptance before real measurements are entered.
- Not supported: current-archive field full-waveform inversion.
- Not supported: heavy field GPU work.
- Not supported: field three-dimensional/high-performance-computing work.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_execution_packet.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_execution_packet.py: pass
tests/test_gssi_field_controlled_collection_execution_packet.py: pass
```
