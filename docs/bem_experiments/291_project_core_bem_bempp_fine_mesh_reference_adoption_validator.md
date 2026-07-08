# BEM Experiment 291: Bempp Fine-Mesh Reference Adoption Validator

Date: 2026-06-28

## Purpose

Validate the saved run `290` Bempp fine-mesh reference adoption checklist from
its output artifacts.

This validator checks that the 8x20 finite-cylinder mesh remains the adopted
BEM-side high-frequency reference, the 6x16 mesh remains a smoke-test mesh, the
source and receiver metadata locks are preserved, and downstream claims remain
blocked.

It does not run BEM, run 3D FDTD, ingest real FDTD traces, run a real
BEM/FDTD comparison, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/291_project_core_bem_bempp_fine_mesh_reference_adoption_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_reference_adoption_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_reference_adoption_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_reference_adoption_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_REFERENCE_ADOPTION_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_reference_adoption_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_reference_adoption_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                                  7
passed checks:                          7
failed checks:                          0
validation ready:                       true
source checklist ready:                 true
reference-ready rows:                   4
superseded reference rows:              1
blocked rows:                           2
8x20 recommended high-frequency ref:    true
6x16 sufficient full-grid ref:          false
source convention lock ready:           true
receiver geometry lock ready:           true
real BEM/FDTD comparison ready:         false
3D validation claim ready:              false
layered 3D GPR model ready:             false
field transfer ready:                   false
GPU/HPC ready:                          false
field FWI ready:                        false
```

## Interpretation

The saved run `290` checklist is internally consistent. The 8x20 mesh is
adopted as the BEM-side reference, the 6x16 mesh is restricted to smoke use,
source/receiver metadata are locked, and downstream claims remain blocked.

## Decision

Use runs `290-291` as the validated Bempp fine-mesh reference adoption
checkpoint. Sensitivity testing is still required before treating the validator
itself as guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_reference_adoption_validator.py
3 passed
```

Figure validation:

```text
2897x853, dynamic range=255
```
