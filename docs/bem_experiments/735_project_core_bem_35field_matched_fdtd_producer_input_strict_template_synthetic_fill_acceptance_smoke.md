# BEM Experiment 735: Strict-Template Synthetic Fill Acceptance Smoke

Date: 2026-07-01

## Purpose

Create a run-local synthetic positive control for the strict matched-FDTD
producer input acceptance path.

This run does not execute FDTD, create real BEM/FDTD evidence, write live
producer input files, run 3D validation, launch GPU/HPC work, transfer to field
data, or run field FWI.

## Output

```text
outputs/bem_experiments/735_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke
```

Key artifacts:

```text
data/synthetic_strict_input_files/
data/synthetic_accepted_return_files/
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source dry-run ready:              true
source validation ready:           true
source sensitivity ready:          true
synthetic files:                   2
synthetic input rows:              558
synthetic accepted files:          2
synthetic accepted rows:           558
synthetic validation errors:       0
strict contract hash errors:       0
output-local synthetic files:      2
real evidence ready files:         0
exporter execution ready:          false
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
smoke artifact ready:              true
```

## Interpretation

The strict acceptance path can accept complete files when all required fields
are populated. This proves that run `732` fails for the intended reason:
missing real solver provenance and returned FDTD values, not a broken strict
contract-hash mechanism.

## Decision

Use this run as output-local positive-control coverage only. Real exporter
execution and real BEM/FDTD comparison remain blocked until live producer input
files are filled with real matched-FDTD output and pass strict acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke.py
3 passed
```

Figure check:

```text
2644x850, dynamic range=255
```
