# BEM Experiment 290: Bempp Fine-Mesh Reference Adoption Checklist

Date: 2026-06-28

## Purpose

Convert the existing Bempp 3D prototype audits into one BEM-side reference
checklist for future paired BEM/FDTD work.

This run combines three saved evidence streams:

```text
107: source convention sensitivity
108: receiver geometry sensitivity
113: fine-mesh frequency-grid audit
```

It does not run 3D FDTD, ingest real FDTD traces, run a real BEM/FDTD
comparison, calibrate thresholds, launch GPU/HPC work, run field FWI, or
validate a layered 3D GPR model.

## Output

```text
outputs/bem_experiments/290_project_core_bem_bempp_fine_mesh_reference_adoption_checklist
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_reference_adoption_checklist_rows.csv
data/project_core_bem_bempp_fine_mesh_reference_adoption_checklist_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_reference_adoption_checklist.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_REFERENCE_ADOPTION_CHECKLIST.md
scripts/run_project_core_bem_bempp_fine_mesh_reference_adoption_checklist.py
scripts/test_project_core_bem_bempp_fine_mesh_reference_adoption_checklist.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checklist rows:                         7
reference-ready rows:                   4
superseded reference rows:              1
blocked rows:                           2
fine mesh frequency grid usable:        true
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

The four reference-ready items are:

| Item | Result |
| --- | --- |
| 8x20 surface mesh | Adopt as the future BEM-side high-frequency reference mesh. |
| Frequency grid | Keep the run `113` grid for future FDTD frequency-bin matching. |
| Source convention | Preserve source position and y-oriented electric-dipole convention. |
| Receiver geometry | Preserve 31 receiver samples, 0.16 m span, and 0.09 m receiver height. |

The 6x16 mesh remains useful for smoke tests, but it is not sufficient as the
full-grid high-frequency reference mesh.

## Interpretation

The BEM-side 3D prototype now has a concrete reference checklist. Future paired
FDTD work should compare against the 8x20 finite-cylinder mesh, the run `113`
frequency grid, and the locked source/receiver metadata. The earlier 6x16 mesh
should be kept only for fast smoke checks.

This is still BEM-side reference readiness only. It is not evidence of real
BEM/FDTD agreement, 3D validation, layered GPR readiness, field transfer, GPU
readiness, or field FWI readiness.

## Decision

Use run `290` as the Bempp fine-mesh reference adoption checklist for future
paired FDTD work. Do not promote real BEM/FDTD agreement or any downstream
validation claim until a matched real FDTD comparison exists.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_reference_adoption_checklist.py
3 passed
```

Figure validation:

```text
2789x865, dynamic range=255
```
