# BEM Experiment 540: Matched FDTD Return Real-Export Implementation Gap Audit

Date: 2026-06-30

## Purpose

Audit the remaining implementation gap after the matched-FDTD real-export
schema block.

Runs `537-539` define and guard the required FDTD return schema. This run
probes the current real-export and accepted-file writer interfaces in real mode
to answer:

```text
Is there an executable real FDTD export or accepted comparison writer available
behind the guarded schema?
```

This is a CPU-only interface audit. It does not run FDTD, run BEM solves, write
accepted evidence, run FWI, use GPU kernels, run field FWI, run 3D/HPC work, or
train neural networks.

## Output

```text
outputs/bem_experiments/540_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_fdtd_exporter_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_writer_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_blocker_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source schema ready:                       true
source validator ready:                    true
source sensitivity ready:                  true
FDTD exporter probes:                      2
FDTD exporter refusals:                    2
FDTD real export enabled:                  0
FDTD return values exported:               0
writer probes:                             4
writer refusals:                           4
writer real writes enabled:                0
accepted return files written:             0
evidence-ready files:                      0
implementation blockers:                   4
ready blockers:                            0
implementation-gap audit ready:            true
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The two FDTD exporter probes both refuse real export:

```text
fdtd_source_hash_manifest
fdtd_scattered_norm_values
```

The accepted-file writer refuses real writes for all four return-file keys:

```text
fdtd_source_hash_manifest
bem_source_hash_manifest
fdtd_scattered_norm_values
bem_scattered_norm_values
```

## Decision

The next BEM implementation step is still real FDTD value export and schema
validation. The accepted comparison writer should remain disabled until real
BEM and FDTD values both exist in the required return schema.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit.py
3 passed
```

Figure check:

```text
2465x845, dynamic range=255
```
