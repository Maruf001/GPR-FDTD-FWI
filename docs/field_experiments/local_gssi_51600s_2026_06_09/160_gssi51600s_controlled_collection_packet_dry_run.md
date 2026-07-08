# Field Experiment 160: Controlled Collection Packet Dry Run

Date: 2026-06-22

## Purpose

Test whether the run `158` controlled-collection execution packet can pass the
existing packet validator when all required values are filled. This is a
workflow dry run with deliberately artificial placeholder values. It is not
measured field data and must not be used for scientific field claims.

This is CPU-only validation. It does not run DZT preprocessing,
finite-difference time-domain simulation, full-waveform inversion, GPU kernels,
field full-waveform inversion, three-dimensional/high-performance-computing
work, or neural-network training.

Run `159` was a same-turn draft with a reporting bug in the delta JSON. Run
`160` is the corrected dry-run output for this checkpoint.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/160_gssi51600s_controlled_collection_packet_dry_run
```

Key artifacts:

```text
dry_run_packet/session_log.csv
dry_run_packet/target_truth.csv
dry_run_packet/profile_geometry.csv
dry_run_packet/acquisition_run.csv
dry_run_packet/reference_measurement.csv
data/field_controlled_collection_packet_dry_run_acceptance_status.csv
data/field_controlled_collection_packet_dry_run_delta.json
data/field_controlled_collection_packet_dry_run_findings.csv
data/field_controlled_collection_packet_dry_run_summary.json
docs/FIELD_COLLECTION_PACKET_DRY_RUN.md
```

## Result

```text
source execution packet:              158_gssi51600s_controlled_collection_execution_packet
dry-run packet rows:                  12
dry-run filled rows:                  12
blocking findings:                    0
missing required values:              0
data-type failures:                   0
cross-table failures:                 0
ready acceptance gates:               7 / 7
dry-run packet acceptance:            true
source packet acceptance:             false
scientific field claim ready:         false
current-archive field FWI ready:      false
heavy field work ready:               false
field 3D/HPC ready:                   false
gpu priority:                         none
```

The source packet in run `158` had 51 missing required values and zero
cross-table failures. The dry-run fill reduces missing values to zero and keeps
cross-table failures at zero. This verifies that the packet identifiers,
links, required-field rules, and validator can accept a fully filled packet.

## Interpretation

This is an engineering validation of the field collection workflow. It proves
that the packet structure is usable. It does not prove field geometry, timing,
amplitude calibration, radius, cover depth, or inversion readiness.

The next real field action remains unchanged: collect measured values into the
run `158` packet and rerun the validator.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_packet_dry_run.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_packet_dry_run.py: pass
tests/test_gssi_field_controlled_collection_packet_dry_run.py: pass
```
