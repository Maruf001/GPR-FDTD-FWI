# BEM Experiment 559: Bempp Candidate Return File Acceptance Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `558` validator for accepted BEM-side return files.

The sensitivity set copies the run `557` source and applies controlled damage:
summary readiness drift, missing source-hash row, duplicate scattered-norm row
identity, invalid hash value, negative norm value, written-file hash drift,
premature comparison promotion, figure damage, and missing script snapshots.

This run does not produce matched-FDTD return files or promote BEM/FDTD
comparison evidence, 3D validation, field transfer, field FWI, or GPU/HPC work.

## Output

```text
outputs/bem_experiments/559_project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity_rows.csv
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity_summary.json
figures/project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                    true
sensitivity cases:                         10
expected pass cases:                       1
expected fail cases:                       9
actual pass cases:                         1
actual fail cases:                         9
unexpected cases:                          0
damaged cases:                             9
BEM/FDTD comparison ready:                 false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
sensitivity ready:                         true
```

## Interpretation

The validator accepts only the exact accepted BEM-side return-file source and
rejects all damaged states tested here. One useful repair was made during this
run: copied-source validation now checks the copied return files rather than
resolving file paths back to the pristine run `557` directory.

## Decision

Treat runs `557-559` as the guarded BEM-side return-file block. The next
comparison blocker is no longer the BEM return files; it is the missing
matched-FDTD source-hash and scattered-norm return CSV files from runs
`555-556`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance.py
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance_validator.py
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance_validation_sensitivity.py
13 passed
```

Figure check:

```text
2646x910, dynamic range=255
```
