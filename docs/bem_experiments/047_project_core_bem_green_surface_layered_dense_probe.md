# BEM Experiment 047: Layered Dense Surface Probe

Date: 2026-06-25

## Purpose

Diagnose the run `046` layered interpolation failure by recording a denser
layered target-cell background surface while reusing the saved run `046`
scattered band and target cells.

This is a CPU-only diagnostic. It records additional layered background
target-cell fields, but it does not rerun target FDTD, field data, GPU work,
FWI, 3D/HPC, neural networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/047_project_core_bem_green_surface_layered_dense_probe
```

Key artifacts:

```text
data/project_core_bem_green_surface_layered_dense_probe.csv
data/project_core_bem_green_surface_layered_dense_probe_summary.json
data/project_core_bem_green_surface_layered_dense_probe_arrays.npz
figures/project_core_bem_green_surface_layered_dense_probe.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_LAYERED_DENSE_PROBE.md
```

## Result

```text
run 046 sparse interpolated L2:     1.1770012780031571
dense surface samples:              19
dense all-scan L2:                  0.5220233499204818
dense exact-surface LOO L2:         0.619762715748986
dense interpolated-surface LOO L2:  0.697021169360853
dense layered surface ready:        true
edge extrapolated points:           0
gpu required:                       false
```

## Interpretation

Densifying the layered target-cell surface repairs the run `046` interpolation
failure. Layered media are viable for this tested case, but only with denser
project-domain surface sampling than the homogeneous cases needed.

## Decision

Promote layered media to a conditional extension of the contract: require dense
target-cell surface sampling before any layered BEM/FDTD, field, 3D, or
BEM-derived replacement claim.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_layered_dense_probe.py
python run_project_core_bem_green_surface_layered_dense_probe.py
```

Figure check:

```text
project_core_bem_green_surface_layered_dense_probe.png: 1911x788, dynamic range=255
```
