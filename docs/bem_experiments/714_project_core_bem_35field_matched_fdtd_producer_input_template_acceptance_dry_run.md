# BEM Experiment 714: Producer Input Template Acceptance Dry Run

Date: 2026-06-30

## Purpose

Dry-run the input-bound exporter acceptance checks against the non-live
producer input templates from run `711`.

This run answers a narrow question: do the templates preserve the required row
identities while still failing acceptance as non-evidence because real solver
provenance and real FDTD values are blank?

This is CPU-only validation. It does not run FDTD, execute the exporter, create
accepted return files, run a real BEM/FDTD comparison, launch GPU/HPC work,
transfer to field evidence, or promote 3D validation claims.

## Output

```text
outputs/bem_experiments/714_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_error_family_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run.png
scripts/script_snapshot_manifest.json
```

## Result

```text
dry-run files:                       2
template rows:                     558
required rows:                     558
row-identity matches:                2 / 2
blank required FDTD values:        558
accepted files:                      0
accepted rows if valid:              0
validation errors:                2790
error families:                      6
live input files present:            0
exporter execution ready:        false
new FDTD executed:               false
GPU/HPC ready:                   false
```

The six error families are the expected missing real fields:

```text
input_contract_sha256_missing_or_invalid:        558
real_fdtd_exported_false_or_missing:             558
solver_log_sha256_missing_or_invalid:            558
solver_status_missing_or_invalid:                558
returned_fdtd_source_hash_missing_or_invalid:    279
returned_fdtd_scattered_norm_missing_or_invalid: 279
```

## Interpretation

The templates are useful: they exactly preserve the required row identities.
They are also correctly rejected as non-evidence because they contain no real
matched-FDTD solver provenance or returned values.

## Decision

Do not run the exporter until the two live input files are filled with real
matched-FDTD output and pass acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run.py
3 passed
```

Figure check:

```text
2716x868, dynamic range=255
```
