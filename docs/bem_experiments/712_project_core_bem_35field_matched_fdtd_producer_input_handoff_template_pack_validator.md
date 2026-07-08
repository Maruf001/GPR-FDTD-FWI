# BEM Experiment 712: Producer Input Handoff Template Pack Validator

Date: 2026-06-30

## Purpose

Validate the saved run `711` handoff template packet from artifacts.

The validator checks that the two templates preserve the locked 558-row
matched-FDTD schema, keep real solver fields blank, leave the live external
input paths empty, and do not promote execution readiness.

This is CPU-only artifact validation. It does not run FDTD, execute the
input-bound exporter, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/712_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
checks passed:                       7
checks failed:                       0
template files:                      2
template rows:                       558
target live input files present:     0
blank required FDTD value cells:     558
real FDTD value count:               0
template live evidence count:        0
exporter execution ready:            false
new FDTD executed:                   false
GPU/HPC ready:                       false
```

## Interpretation

The handoff packet validates as a non-live template packet. It is safe to hand
off as a schema and row-identity guide, but it still contains no real
matched-FDTD evidence.

## Decision

Treat run `711` as the current producer-input handoff aid. Continue to block
the exporter and comparison until real filled input files are staged and pass
acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validator.py
3 passed
```

Figure check:

```text
2465x861, dynamic range=255
```
