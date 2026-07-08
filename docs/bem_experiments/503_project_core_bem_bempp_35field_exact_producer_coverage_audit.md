# BEM Experiment 503: Bempp 35-Field Exact Producer Coverage Audit

Date: 2026-06-29

## Purpose

Check whether historical Bempp-side runs already cover the exact 35-field
producer grid needed by the real return-file contract.

The target producer grid is 31 receivers by nine frequencies, for 279 rows.
This run scans existing BEM summaries and separates grid metadata, Bempp
runtime metadata, 31x9 metadata matches, and exact real-return producer
candidates.

## Output

```text
outputs/bem_experiments/503_project_core_bem_bempp_35field_exact_producer_coverage_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_candidate_rows.csv
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_summary.json
figures/project_core_bem_bempp_35field_exact_producer_coverage_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
target receiver count:                      31
target frequency count:                     9
target grid rows:                           279
audited candidate summaries:                145
grid metadata candidates:                   106
Bempp runtime candidates:                   54
31x9 metadata matches:                      41
Bempp-tagged 31x9 metadata matches:         1
exact 35-field Bempp producer candidates:   0
best Bempp receiver-matched frequency count:9
Bempp frequency shortfall to 35-field:      0
exact Bempp 35-field producer ready:        false
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
```

The important nuance is that the project does contain one Bempp-tagged 31x9
metadata match, but it is not an exact real-return producer. It does not
provide the accepted `real_return_files` writer with 279 BEM scattered-norm
entries and the required source-hash lineage.

## Decision

The BEM side needs an explicit 9-frequency Bempp export plus a
`real_return_files` writer before it can provide accepted real return files.
Do not promote real BEM/FDTD comparison, 3D validation, GPU/HPC, field
transfer, or field FWI claims from the current historical metadata.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_exact_producer_coverage_audit.py
5 passed
```

Figure check:

```text
3220x845, dynamic range=255
```
