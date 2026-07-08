# BEM Experiment 555: Matched-FDTD Return Producer Checklist

Date: 2026-06-30

## Purpose

Convert the guarded matched-FDTD return requirements into a two-file producer
checklist.

Runs `549-554` lock row identity and value domains. This run turns those
requirements into the exact two real FDTD return CSV exports needed before
BEM/FDTD comparison evidence can be written.

This run does not create real FDTD return files and does not promote BEM/FDTD
comparison evidence, 3D validation, GPU/HPC work, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/555_project_core_bem_35field_matched_fdtd_return_producer_checklist
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_producer_checklist_checklist_rows.csv
data/project_core_bem_35field_matched_fdtd_return_producer_checklist_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_producer_checklist_summary.json
figures/project_core_bem_35field_matched_fdtd_return_producer_checklist.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source value-domain contract ready:        true
source validation ready:                   true
source sensitivity ready:                  true
checklist files:                           2
required return rows:                      558
source-hash return rows:                   279
positive-float return rows:                279
pending export files:                      2
comparison-ready files:                    0
checklist actions:                         4
producer checklist ready:                  true
GPU priority:                              none
```

## Decision

Produce both real matched-FDTD return CSV files before rerunning row-identity,
value-domain, and BEM/FDTD comparison acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_producer_checklist.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
