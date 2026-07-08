# BEM Experiment 515: FDTD 35-Field Real-Return Exporter Interface Guard Audit

Date: 2026-06-30

## Purpose

Audit the guarded FDTD-side exporter interface for the 35-field real-return
files.

Runs `506-508` defined the accepted four-file producer contract. Runs `509-511`
guarded the return-file writer interface. Runs `512-514` guarded the
Bempp-side exporter interface. This run adds the matching FDTD-side exporter
interface, but only as a contract guard: it can verify that the two FDTD
return-file keys belong to the saved contract, and it refuses real export
requests.

## Output

```text
outputs/bem_experiments/515_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit
```

Key artifacts:

```text
data/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_audit_rows.csv
data/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit_summary.json
figures/project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
FDTD exporter script available:             true
source producer contract ready:             true
source writer validation ready:             true
source Bempp exporter validation ready:     true
FDTD return-file keys:                      2
audit cases:                                5
audit cases passed:                         5
all FDTD return-file keys contract-checkable: true
Bempp-side key rejected:                    true
unknown file key rejected:                  true
real FDTD export refused:                   true
FDTD exporter interface guard ready:        true
real FDTD export enabled:                   false
real return values exported:                false
accepted return file written:               false
remaining real-return blockers:             3
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
GPU priority:                               none
```

The exporter interface checks these two FDTD-side return-file keys:

```text
fdtd_source_hash_manifest
fdtd_scattered_norm_values
```

It rejects a Bempp-side file key, rejects an unknown key, and refuses a real
FDTD export request. No real values are exported, no accepted return file is
written, and no downstream evidence state is promoted.

## Decision

Use this guarded exporter interface as the FDTD-side contract check before
implementing real FDTD return-value export. Real return production still needs
real FDTD values, real Bempp values, and a later evidence-producing writer path
with provenance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_real_return_exporter.py
tests/test_project_core_bem_fdtd_35field_real_return_exporter_interface_guard_audit.py
tests/test_project_core_bem_bempp_35field_real_return_exporter_interface_guard_audit_validator.py
tests/test_project_core_bem_fdtd_35field_real_return_files_writer.py
18 passed
```

Figure check:

```text
2465x864, dynamic range=255
```
