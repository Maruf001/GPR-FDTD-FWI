# BEM Experiment 560: Matched-FDTD Return Candidate Source Locator Audit

Date: 2026-06-30

## Purpose

Locate any existing source that could legitimately populate the two missing
matched-FDTD return CSV files required by runs `555-556`.

Runs `557-559` closed and guarded the BEM-side return-file block. This run
checks whether the FDTD side can be populated from existing exact, proxy,
synthetic, or local 2D FDTD-like artifacts.

This run does not create FDTD return files, run FDTD, compare BEM with FDTD,
launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/560_project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit_required_file_rows.csv
data/project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit_candidate_rows.csv
data/project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
BEM return block ready:                    true
required FDTD return files:                2
present required FDTD return files:        0
ready required FDTD return files:          0
candidate sources audited:                 5
candidate sources with 279-row shape:      1
proxy shape matches:                       1
usable exact FDTD return sources:          0
unusable candidates:                       5
BEM/FDTD comparison ready:                 false
3D validation claim ready:                 false
field transfer ready:                      false
GPU priority:                              none
```

## Interpretation

The expected return-file directory is still empty. The only candidate with the
right 279-row receiver-frequency shape is an older 2D scalar proxy export. It
is useful as a reference for shape and bookkeeping, but it is not a real
matched-FDTD return source and cannot be used as comparison evidence.

Synthetic pairwise rows, synthetic inbox files, and local 2D FDTD objective
summaries are also not acceptable substitutes for the two real return CSV
files.

## Decision

The comparison-changing next task is to produce the real matched-FDTD
source-hash manifest and scattered-norm values CSVs required by runs `555-556`.
Do not fill those files from proxy, synthetic, or unrelated 2D summary
artifacts.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_candidate_source_locator_audit.py
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity.py
9 passed
```

Figure check:

```text
2610x873, dynamic range=255
```
