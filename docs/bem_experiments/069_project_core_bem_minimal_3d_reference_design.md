# BEM Experiment 069: Minimal 3D Reference Design

Date: 2026-06-25

## Purpose

Define a minimal 3D FDTD/BEM reference problem for finite-rebar comparison.

This is a design artifact only. It does not launch 3D simulation, FWI, GPU, or
HPC work.

## Output

```text
outputs/bem_experiments/069_project_core_bem_minimal_3d_reference_design
```

Key artifacts:

```text
data/project_core_bem_minimal_3d_reference_design.csv
data/project_core_bem_minimal_3d_reference_design_summary.json
figures/project_core_bem_minimal_3d_reference_design.png
docs/PROJECT_CORE_BEM_MINIMAL_3D_REFERENCE_DESIGN.md
```

## Result

```text
physical domain:                    0.30 x 0.20 x 0.18 m
grid resolution:                    0.005 m
cells with PML:                     80 x 60 x 56 = 268800
time step:                          9.533e-12 s
time steps for 6 ns:                630
cells per 3 GHz concrete wavelength:8.159317231497297
padded memory estimate:             0.16021728515625 GiB
ready for design review:            true
ready for 3D launch:                false
```

## Interpretation

A small 3D reference problem is feasible to specify, but launch still needs
backend selection, explicit approval, and a matched BEM comparison plan.

## Decision

Use this as the first 3D benchmark design candidate.

Do not launch 3D/HPC/GPU from the design alone.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_minimal_3d_reference_design.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_minimal_3d_reference_design.py
pass
```

Figure check:

```text
project_core_bem_minimal_3d_reference_design.png
1925x792, dynamic range=255
```
