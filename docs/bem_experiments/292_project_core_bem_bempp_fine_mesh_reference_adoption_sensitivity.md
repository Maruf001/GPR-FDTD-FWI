# BEM Experiment 292: Bempp Fine-Mesh Reference Adoption Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `291` validator for the run `290` Bempp fine-mesh
reference adoption checklist.

This run checks whether the validator accepts the exact saved run `290`
checklist and rejects controlled damage to checklist rows, summary counts,
8x20 reference adoption, 6x16 smoke-only demotion, source/receiver metadata
locks, downstream readiness states, figure validation, and script snapshots.

It does not run BEM, run 3D FDTD, ingest real FDTD traces, run a real
BEM/FDTD comparison, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/292_project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_REFERENCE_ADOPTION_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                              31
expected pass scenarios:                1
observed pass scenarios:                1
expected failure scenarios:             30
observed failure scenarios:             30
unexpected outcomes:                    0
sensitivity ready:                      true
exact run 290 accepted:                 true
damaged variants rejected:              true
real BEM/FDTD comparison ready:         false
3D validation claim ready:              false
layered 3D GPR model ready:             false
field transfer ready:                   false
GPU/HPC ready:                          false
field FWI ready:                        false
```

## Interpretation

The validator accepts the exact run `290` checklist and rejects every damaged
variant. The rejected cases cover missing or changed checklist rows,
summary-count drift, 8x20 demotion, 6x16 promotion, source/receiver lock drift,
downstream promotion, figure validation drift, and script-snapshot drift.

## Decision

Use runs `290-292` as the guarded Bempp fine-mesh reference adoption checkpoint.
The next BEM-side work should consume this reference contract in the future
matched FDTD export/comparison path, not promote downstream claims from
BEM-only evidence.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_reference_adoption_sensitivity.py
3 passed
```

Figure validation:

```text
4031x892, dynamic range=255
```
