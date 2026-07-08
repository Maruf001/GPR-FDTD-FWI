# BEM Experiment 051: Dense Finite-Domain Field-Map Probe

Date: 2026-06-25

## Purpose

Repeat the run `050` per-target-cell field-map calibration with a denser
homogeneous target-cell field surface.

This is a CPU-only field-map diagnostic. It records additional project-core
background target-cell fields and compares them to analytic `scarep` Green
fields. It does not use field data, GPU work, FWI, 3D/HPC, neural networks, or
the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/051_project_core_bem_finite_domain_field_map_dense_probe
```

Key artifacts:

```text
data/project_core_bem_finite_domain_field_map_dense_probe.csv
data/project_core_bem_finite_domain_field_map_dense_probe_summary.json
data/project_core_bem_finite_domain_field_map_dense_probe_arrays.npz
figures/project_core_bem_finite_domain_field_map_dense_probe.png
docs/PROJECT_CORE_BEM_FINITE_DOMAIN_FIELD_MAP_DENSE_PROBE.md
```

## Result

```text
run 050 sparse LOO L2:              0.8005360330027802
dense surface samples:              19
dense all-source L2:                0.8917842570843266
dense leave-one-source L2:          0.9392735973185401
dense finite-domain map ready:      false
gpu required:                       false
```

## Interpretation

Densifying the finite-domain calibration surface does not bring the field map
inside the held-out gate. It worsens the per-cell transfer result relative to
run `050`.

## Decision

Do not promote finite-domain field mapping as the BEM-derived replacement path.
A replacement needs richer source, boundary, or material physics, or must keep
using explicit project-domain field tables.

## Validation

```text
python -m py_compile run_project_core_bem_finite_domain_field_map_dense_probe.py
python run_project_core_bem_finite_domain_field_map_dense_probe.py
```

Figure check:

```text
project_core_bem_finite_domain_field_map_dense_probe.png: 1732x771, dynamic range=255
```
