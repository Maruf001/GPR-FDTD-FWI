# BEM Experiment 358: Real-Pair Trace Export Packet Filesystem Gap Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `357` filesystem gap-audit validator with controlled
damaged variants.

Run `357` validates the saved run `356` gap audit. This run checks that the
validator accepts the exact saved audit and rejects controlled drift in source
identity, packet counts, action rows, derived row expectations, downstream
states, figure validation, and script snapshots.

This run does not stage files, execute FDTD, run BEM/FDTD comparison, calibrate
thresholds, launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/bem_experiments/358_project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_validation_sensitivity_scenarios.csv
data/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  15
expected pass:              1
observed pass:              1
expected failures:          14
observed failures:          14
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 356:      true
rejects damaged variants:   true
real packet files present:  false
comparison ready:           false
GPU work ready:             false
field transfer ready:       false
3D validation ready:        false
figure size:                3491x909
figure dynamic range:       255
```

## Interpretation

The run `357` validator accepts the exact run `356` gap audit and rejects
controlled damaged variants for source identity drift, contract-guard drift,
packet-count drift, false file presence, missing-file group drift, action-row
drift, derived row-count drift, downstream promotion, figure validation drift,
and script-snapshot drift.

## Decision

Use runs `356-358` as the guarded BEM real-pair packet filesystem gap-audit
block. Real BEM/FDTD comparison remains blocked until the required packet files
are staged.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_validation_sensitivity.py
3 passed
```
