# BEM Experiment 509: BEM/FDTD 35-Field Real-Return Writer Interface Guard Audit

Date: 2026-06-30

## Purpose

Audit the guarded writer interface for the 35-field BEM/FDTD real-return files.

Runs `506-508` defined and protected the accepted producer contract. This run
adds the exact writer interface name from that contract, but only as a guard:
it can check whether a requested return-file key belongs to the saved contract,
and it refuses real return-file writing.

## Output

```text
outputs/bem_experiments/509_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit
```

Key artifacts:

```text
data/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_audit_rows.csv
data/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit_summary.json
figures/project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
writer script available:                   true
source contract spec ready:                true
source contract sensitivity ready:         true
return-file keys:                          4
audit cases:                               6
audit cases passed:                        6
all return-file keys contract-checkable:   true
unknown file key rejected:                 true
real write refused:                        true
writer interface guard ready:              true
writer real-write enabled:                 false
accepted return file written:              false
exporter blockers:                         2
writer real-write blocker:                 1
remaining real-return blockers:            3
real return production ready:              false
real BEM/FDTD comparison ready:            false
3D validation ready:                       false
GPU/HPC ready:                             false
field FWI ready:                           false
GPU priority:                              none
```

The writer interface checks all four accepted return-file keys:

```text
fdtd_source_hash_manifest
bem_source_hash_manifest
fdtd_scattered_norm_values
bem_scattered_norm_values
```

It rejects an unknown key and refuses a real-write request. No accepted return
file is written, and no evidence state is promoted.

## Decision

Use this guarded writer interface before implementing BEM/FDTD exporters. Real
return production still needs the BEM exporter, the FDTD exporter, and a later
real-write implementation path with real values and provenance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_real_return_files_writer.py
tests/test_project_core_bem_fdtd_35field_real_return_writer_interface_guard_audit.py
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec.py
12 passed
```

Figure check:

```text
2465x864, dynamic range=255
```
