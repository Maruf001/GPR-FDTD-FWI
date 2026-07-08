# Field Experiment 337: Antenna-Aware Filesystem Gap Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `336` artifact validator with controlled damaged variants.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/337_gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          16
expected pass:                      1
observed pass:                      1
expected failures:                  15
observed failures:                  15
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 335:              true
rejects damaged variants:           true
packet items required:              61
metadata requirements:              36
antenna metadata addendum items:    4
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The validator accepts exact run `335` artifacts and rejects damaged variants
for contract drift, packet-count drift, present-item drift, metadata-count
drift, antenna-metadata drift, action-row drift, downstream promotion,
GPU-priority drift, figure-validation drift, and script-snapshot drift.

## Decision

Use runs `335-337` as the guarded antenna-aware filesystem gap audit block.
Field evidence remains blocked until the 61-item measured packet exists and
passes the refreshed acceptance gate.

## Validation

Focused sensitivity test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3527x904, dynamic range=255
```
