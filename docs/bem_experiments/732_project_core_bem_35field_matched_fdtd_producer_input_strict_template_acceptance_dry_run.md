# BEM Experiment 732: Strict-Template Producer Input Acceptance Dry Run

Date: 2026-07-01

## Purpose

Dry-run the strict shared exporter acceptance path against the run `729`
matched-FDTD producer input templates.

This run does not execute FDTD, run BEM/FDTD comparison, write live producer
input files, run 3D validation, launch GPU/HPC work, transfer to field data, or
run field FWI.

## Output

```text
outputs/bem_experiments/732_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_error_family_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:          true
source template validation ready:    true
source template sensitivity ready:   true
dry-run files:                       2
template rows:                       558
required rows:                       558
row identity matches:                2
strict contract hash matches:        558
strict contract hash errors:         0
blank returned-value cells:          558
accepted files:                      0
accepted rows:                       0
validation errors:                   2232
error families:                      5
live input files present:            0
exporter execution ready:            false
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
dry-run artifact ready:              true
```

The remaining error families are:

| Error family | Count |
| --- | ---: |
| solver log SHA-256 missing or invalid | 558 |
| solver status missing or invalid | 558 |
| real FDTD exported flag false or missing | 558 |
| returned FDTD source hash missing or invalid | 279 |
| returned FDTD scattered norm missing or invalid | 279 |

## Interpretation

The strict contract-hash problem is closed for the current handoff templates:
all 558 rows carry the expected exact hash. The templates still fail acceptance
because they do not contain real solver provenance or real returned FDTD
values.

## Decision

Keep exporter execution blocked. The next promotion requires real matched-FDTD
producer input files at the live routes, with solver provenance and returned
FDTD values filled.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run.py
3 passed
```

Figure check:

```text
3076x867, dynamic range=255
```
