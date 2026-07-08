# BEM Experiment 527: Bempp 35-Field Fine-Mesh Candidate Value Export Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `526` validator for the full 8x20 Bempp-side candidate
value export.

Run `525` produced complete fine-mesh BEM candidate return files. Run `526`
validated those artifacts. This run verifies that the validator accepts the
exact saved state and rejects damaged values, mesh drift, and false evidence
promotion.

## Output

```text
outputs/bem_experiments/527_project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validation_sensitivity_rows.csv
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validation_sensitivity_summary.json
figures/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    11
expected pass scenarios:                  1
expected failure scenarios:               10
unexpected scenarios:                     0
fine-mesh sensitivity ready:              true
exact source artifacts pass:              true
mesh drift rejected:                      true
accepted evidence promotion rejected:     true
downstream comparison promotion rejected: true
matched FDTD return files present:        false
accepted evidence ready:                  false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
```

The exact run `525` artifacts pass. Ten damaged variants fail as expected:

| Scenario | Expected result | Failed check |
| --- | --- | --- |
| candidate count drift | fail | fine-mesh export counts and values |
| missing norm row | fail | fine-mesh schema |
| bad source hash | fail | fine-mesh schema |
| nonpositive norm | fail | fine-mesh schema |
| frequency failure | fail | fine frequency grid and mesh |
| mesh element drift | fail | fine frequency grid and mesh |
| accepted evidence promotion | fail | acceptance and downstream states |
| downstream comparison promotion | fail | acceptance and downstream states |
| figure damage | fail | figure and script snapshots |
| script snapshot damage | fail | figure and script snapshots |

## Decision

Use runs `525-527` as the guarded 8x20 BEM-side candidate-value export block.
The BEM-side fine-mesh return files are complete and guarded. The remaining
comparison blockers are now outside the BEM value exporter: matched FDTD return
files and accepted evidence writing.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export.py
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator.py
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validation_sensitivity.py
12 passed
```

Figure check:

```text
2645x871, dynamic range=255
```
