# Field Experiment 301: Real-Return Packet Filesystem Gap Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `300` filesystem gap-audit validator with controlled
damaged variants.

Run `300` validates the saved run `299` gap audit. This run checks that the
validator accepts the exact saved audit and rejects controlled drift in source
identity, packet counts, requirement counts, action rows, downstream states,
GPU priority, figure validation, and script snapshots.

This run does not stage measured files, run DZT preprocessing, run FDTD, run
field FWI, launch GPU/HPC work, or claim field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/301_gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_filesystem_gap_audit_validation_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_packet_filesystem_gap_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_packet_filesystem_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  16
expected pass:              1
observed pass:              1
expected failures:          15
observed failures:          15
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 299:      true
rejects damaged variants:   true
real packet files present:  false
field evidence ready:       false
field FWI ready:            false
field 3D/HPC ready:         false
gpu priority:               none
figure size:                3491x904
figure dynamic range:       255
```

## Interpretation

The run `300` validator accepts the exact run `299` gap audit and rejects
controlled damaged variants for source identity drift, contract-guard drift,
packet-count drift, false file presence, missing requirement-count drift,
action-row drift, downstream promotion, GPU-priority drift, figure validation
drift, and script-snapshot drift.

## Decision

Use runs `299-301` as the guarded field real-return packet filesystem gap-audit
block. Field evidence remains blocked until the required measured packet items
are staged.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_filesystem_gap_audit_validation_sensitivity.py
3 passed
```
