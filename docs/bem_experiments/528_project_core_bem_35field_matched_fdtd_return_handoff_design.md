# BEM Experiment 528: 35-Field Matched FDTD Return Handoff Design

Date: 2026-06-30

## Purpose

Convert the completed 8x20 BEM candidate-value export into exact matched FDTD
return requirements.

Runs `525-527` produced and guarded the BEM-side values on the 31-receiver by
nine-frequency grid. This run defines the two FDTD-side return tables and the
pairing table needed before any accepted BEM/FDTD comparison can be made.

## Output

```text
outputs/bem_experiments/528_project_core_bem_35field_matched_fdtd_return_handoff_design
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_handoff_design_required_fdtd_source_hash_rows.csv
data/project_core_bem_35field_matched_fdtd_return_handoff_design_required_fdtd_scattered_norm_rows.csv
data/project_core_bem_35field_matched_fdtd_return_handoff_design_comparison_pairing_rows.csv
data/project_core_bem_35field_matched_fdtd_return_handoff_design_summary.json
figures/project_core_bem_35field_matched_fdtd_return_handoff_design.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source BEM export ready:                   true
source BEM validation ready:               true
source BEM sensitivity ready:              true
source FDTD exporter guard ready:          true
receivers:                                 31
frequencies:                               9
matched receiver-frequency keys:           279
BEM source-hash rows:                      279
BEM scattered-norm rows:                   279
required FDTD return files:                2
required FDTD source-hash rows:            279
required FDTD scattered-norm rows:         279
required FDTD return entries:              558
comparison pairing rows:                   279
BEM values ready:                          true
FDTD values ready:                         false
comparison-ready rows:                     0
remaining comparison blockers:             2
handoff design ready:                      true
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

## Interpretation

The BEM side is now concrete enough to hand off to an FDTD return producer. The
missing data are not vague: the project needs two FDTD return tables, each with
279 rows aligned to the same receiver-frequency keys as the BEM values.

The comparison still cannot be made. The two remaining blockers are real FDTD
return values and an accepted evidence writer after both BEM and FDTD values
exist.

## Decision

Use this handoff as the FDTD return requirement for the next BEM/FDTD bridge
step. Do not claim BEM/FDTD agreement, 3D validation, GPU/HPC readiness, field
transfer, or field FWI from this handoff alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_handoff_design.py
3 passed
```

Figure check:

```text
3292x881, dynamic range=255
```
