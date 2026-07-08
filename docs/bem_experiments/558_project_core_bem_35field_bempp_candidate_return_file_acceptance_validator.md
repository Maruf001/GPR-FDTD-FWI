# BEM Experiment 558: Bempp Candidate Return File Acceptance Validator

Date: 2026-06-30

## Purpose

Validate run `557`, which accepted the fine-mesh Bempp candidate values as two
BEM-side return CSV files.

The validator checks the source summary, file shape, row identities, value
domains, written-file hashes, blocked downstream states, figure output, and
frozen script snapshots.

This run does not produce matched-FDTD return files or promote BEM/FDTD
comparison evidence, 3D validation, field transfer, field FWI, or GPU/HPC work.

## Output

```text
outputs/bem_experiments/558_project_core_bem_35field_bempp_candidate_return_file_acceptance_validator
```

Key artifacts:

```text
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_validator_checks.csv
data/project_core_bem_35field_bempp_candidate_return_file_acceptance_validator_summary.json
figures/project_core_bem_35field_bempp_candidate_return_file_acceptance_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source acceptance ready:                   true
validation checks:                         6
passed checks:                             6
failed checks:                             0
accepted BEM return files:                 2
accepted BEM return rows:                  558
matched-FDTD return files:                 0
BEM/FDTD comparison ready:                 false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
validation ready:                          true
```

## Interpretation

The BEM-side return files from run `557` are internally consistent and complete.
They contain the expected 279 source-hash rows and 279 positive
scattered-norm rows, and their hashes match the acceptance table.

The comparison remains blocked because the matched-FDTD return files are still
absent.

## Decision

Use runs `557-558` as the validated BEM-side return-file block. The next
defensible work is sensitivity hardening of this validator, followed by
matched-FDTD return production or a tighter FDTD producer interface.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance.py
tests/test_project_core_bem_35field_bempp_candidate_return_file_acceptance_validator.py
9 passed
```

Figure check:

```text
1926x843, dynamic range=255
```
