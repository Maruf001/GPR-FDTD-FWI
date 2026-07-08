# BEM Experiment 061: Layered Dense Surface Cache

Date: 2026-06-25

## Purpose

Export the dense layered project-domain target-cell field surface as a reusable
cache.

Runs `058` and `059` showed that low-order analytic/image replacements do not
close the layered replay gate. This run keeps layered work moving by saving the
dense FDTD-derived field table that did pass run `047`, so future layered BEM
diagnostics do not need to recompute the same background surface.

This is CPU-only. It does not run field preprocessing, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/bem_experiments/061_project_core_bem_layered_dense_surface_cache
```

Key artifacts:

```text
data/project_core_bem_layered_dense_surface_cache.csv
data/project_core_bem_layered_dense_surface_cache_summary.json
data/project_core_bem_layered_dense_surface_cache_arrays.npz
figures/project_core_bem_layered_dense_surface_cache.png
docs/PROJECT_CORE_BEM_LAYERED_DENSE_SURFACE_CACHE.md
```

## Result

```text
surface shape:                      19x533x17
cache size:                         2710904 bytes
surface samples:                    19
target cells:                       533
selected frequency bins:            17
best all-scan L2:                   0.5220233499204818
best exact-surface LOO L2:          0.619762715748986
best interpolated-surface LOO L2:   0.697021169360853
edge extrapolated points:           0
cache replay ready:                 true
```

Cache:

```text
outputs/bem_experiments/061_project_core_bem_layered_dense_surface_cache/data/project_core_bem_layered_dense_surface_cache_arrays.npz
```

Stored arrays:

```text
surface
surface_x_m
source_points_m
receiver_points_m
target_ix
target_iz
target_weights
selected_indices
selected_frequencies_hz
fdtd_band
```

## Interpretation

The dense layered project-domain surface can be cached and replayed under the
same layered interpolation gate that repaired run `046`. This gives the layered
track a practical tabulated-surface asset while true layered Green physics
remains unresolved.

## Decision

Use this cache as the current tabulated layered surface asset for future BEM
diagnostics.

This is not a layered analytic Green replacement, measured-field claim, 3D
claim, FWI launch gate, or GPU/HPC escalation.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_dense_surface_cache.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_dense_surface_cache.py
pass
```

Figure check:

```text
project_core_bem_layered_dense_surface_cache.png
1985x846, dynamic range=255
```
