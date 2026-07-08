# BEM Experiment 784: Complex Metric Producer-Side Dependency Audit

Date: 2026-07-01

## Purpose

Split the current BEM/FDTD complex-metric real-return blocker into its producer
dependencies.

Runs `778-783` guarded the real-return preflight and claim boundary, but the
blocker was still stated as "five real CSV files are absent." This run answers
which parts of those CSVs can be prepared from the BEM side and which parts
still require matched FDTD export and provenance.

## Output

```text
outputs/bem_experiments/784_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_dependency_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_stage_dependency_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:                 true
source preflight ready:                     true
source claim boundary ready:                true
stages:                                     5
metric rows:                                279
required columns:                           13
dependency groups:                          6
required cells:                             3627
nonblank cells:                             279
blank cells:                                3348
prefilled pair-id cells:                    279
shared sampling cells required:             558
BEM value cells required:                   558
FDTD value cells required:                  558
comparison-policy cells required:           279
FDTD provenance/status cells required:      1395
producer files present:                     0
preflight-passed files:                     0
ready-to-stage files:                       0
real BEM/FDTD comparison ready:             false
field transfer ready:                       false
3D/HPC ready:                               false
gpu priority:                               none
```

## Interpretation

The real-return blocker is not a single undifferentiated file gap. It has a
specific structure:

| Dependency group | Required cells | Current nonblank cells | Needs matched FDTD export |
| --- | ---: | ---: | --- |
| identity/pair IDs | 279 | 279 | no |
| shared receiver-frequency sampling | 558 | 0 | no |
| BEM complex values | 558 | 0 | no |
| FDTD complex values | 558 | 0 | yes |
| normalization policy | 279 | 0 | no |
| FDTD provenance and status | 1395 | 0 | yes |

The BEM side can prepare 558 complex-value cells, but those cells alone do not
support comparison. A real comparison still requires all five CSV files to
contain shared sampling fields, BEM values, FDTD values, normalization policy,
and FDTD provenance/status fields, then pass preflight.

## Decision

Use this run to guide partial producer work on the BEM side. Do not treat a
BEM-only fill as real BEM/FDTD agreement, detector evidence, field transfer, or
3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_producer_side_dependency_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2824x914, dynamic range=255
```
