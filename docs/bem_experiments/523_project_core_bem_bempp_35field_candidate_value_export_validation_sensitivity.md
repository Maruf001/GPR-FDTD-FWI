# BEM Experiment 523: Bempp 35-Field Candidate Value Export Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `522` validator for the Bempp-side 35-field candidate
value export.

Run `521` produced complete candidate BEM source-hash and scattered-norm return
files. Run `522` validated those artifacts. This run verifies that the
validator accepts the exact saved state and rejects damaged or falsely promoted
states.

## Output

```text
outputs/bem_experiments/523_project_core_bem_bempp_35field_candidate_value_export_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_candidate_value_export_validation_sensitivity_rows.csv
data/project_core_bem_bempp_35field_candidate_value_export_validation_sensitivity_summary.json
figures/project_core_bem_bempp_35field_candidate_value_export_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    11
expected pass scenarios:                  1
expected failure scenarios:               10
unexpected scenarios:                     0
candidate export sensitivity ready:       true
exact source artifacts pass:              true
accepted evidence promotion rejected:     true
downstream comparison promotion rejected: true
real return files present:                false
real return values present:               false
real return packet accepted:              false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
```

The exact run `521` artifacts pass. Ten damaged variants fail as expected:

| Scenario | Expected result | Failed check |
| --- | --- | --- |
| candidate count drift | fail | candidate export counts and values |
| missing norm row | fail | candidate return-file schema |
| bad source hash | fail | candidate return-file schema |
| nonpositive norm | fail | candidate return-file schema |
| frequency failure | fail | frequency grid and mesh smoke |
| false fine-mesh promotion | fail | acceptance and downstream states |
| accepted evidence promotion | fail | acceptance and downstream states |
| downstream comparison promotion | fail | acceptance and downstream states |
| figure damage | fail | figure and script snapshots |
| script snapshot damage | fail | figure and script snapshots |

## Decision

Use runs `521-523` as the guarded BEM-side candidate-value export block. The
BEM side can now produce complete candidate values for the required grid, but
accepted BEM/FDTD comparison remains blocked until the matched FDTD return
files, fine-mesh acceptance path, and evidence writer are present.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_candidate_value_export.py
tests/test_project_core_bem_bempp_35field_candidate_value_export_validator.py
tests/test_project_core_bem_bempp_35field_candidate_value_export_validation_sensitivity.py
12 passed
```

Figure check:

```text
2645x875, dynamic range=255
```
