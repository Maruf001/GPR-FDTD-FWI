# BEM Experiment 534: Matched FDTD Return Real-Export Preflight Gap Audit

Date: 2026-06-30

## Purpose

Audit what still blocks real matched-FDTD return export after the guarded
contract-check command inventory in runs `531-533`.

This run probes the existing FDTD return exporter in real-export mode for the
two required FDTD return-file keys. The expected result is refusal, not
evidence production.

## Output

```text
outputs/bem_experiments/534_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_real_export_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source command inventory ready:            true
source validation ready:                   true
source sensitivity ready:                  true
FDTD return file keys:                     2
required FDTD return entries:              558
real-export probes:                        2
real-export refusals:                      2
real FDTD export enabled:                  0
real return values exported:               0
accepted return files written:             0
evidence-ready files:                      0
implementation actions:                    4
ready implementation actions:              0
remaining real-export blockers:            4
GPU priority:                              none
```

Probe result:

| File key | Real-export exit code | Refused | Values exported | Evidence ready |
| --- | ---: | --- | --- | --- |
| fdtd_source_hash_manifest | 2 | true | false | false |
| fdtd_scattered_norm_values | 2 | true | false | false |

## Decision

The matched FDTD return keys are guarded, but real FDTD value export is not
implemented. The next BEM-side implementation step is real FDTD value export
and validation, followed by the accepted evidence writer only after both BEM
and FDTD real values exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_preflight_gap_audit.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
