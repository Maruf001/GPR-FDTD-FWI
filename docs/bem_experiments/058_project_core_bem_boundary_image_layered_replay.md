# BEM Experiment 058: Boundary-Image Layered Replay

Date: 2026-06-25

## Purpose

Test whether the run `057` homogeneous boundary-image replacement transfers to
the saved air/concrete layered dielectric case from run `046`.

This is a CPU-only layered replay. It recomputes a dense layered background
field surface and reuses the saved layered scattered response. It does not run
field preprocessing, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/058_project_core_bem_boundary_image_layered_replay
```

Key artifacts:

```text
data/project_core_bem_boundary_image_layered_replay.csv
data/project_core_bem_boundary_image_layered_replay_summary.json
figures/project_core_bem_boundary_image_layered_replay.png
docs/PROJECT_CORE_BEM_BOUNDARY_IMAGE_LAYERED_REPLAY.md
```

## Result

```text
variants checked:                   60
surface samples:                    19
target cells:                       533
selected frequency bins:            17
run 046 sparse interpolated L2:     1.1770012780031571
run 046 exact-surface L2:           0.619762715748986
best field-table LOO L2:            1.2033632008026727
best scattering all-scan L2:        0.8085674766282847
best scattering LOO L2:             0.9920836859251249
layered boundary-image ready:       false
```

Best scattering variant:

```text
source z:             0.054 m
speed scale:          0.75
image set:            cardinal
scattering variant:   product_no_div
```

The best variants by layered scattering leave-one-scan L2 were:

| Rank | z | Speed scale | Image set | Field LOO L2 | Scattering LOO L2 | Variant |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 1 | 0.054 | 0.75 | cardinal | 1.23741892018392 | 0.9920836859251249 | product_no_div |
| 2 | 0.038 | 0.75 | cardinal | 1.2388985757157482 | 0.9940951982242249 | product_div_source |
| 3 | 0.046 | 0.75 | cardinal | 1.2381595872063293 | 0.9942159226022668 | product_no_div |
| 4 | 0.054 | 1.05 | cardinal | 1.2033632008026727 | 1.0297380446437654 | product_no_div |

## Interpretation

The homogeneous boundary-image replacement does not transfer to the tested
air/concrete layered dielectric case. Even the best 60-variant replay remains
well above the 0.75 acceptance gate.

This separates the BEM track into two current regimes:

```text
homogeneous tested 2D cases: boundary-image replacement viable
layered tested 2D case:      dense project-domain field table still required
```

## Decision

Keep layered media on the dense project-domain field-table path.

Do not use the boundary-image replacement for layered, field, 3D, FWI, GPU, or
historical `outputs/experiments` archive claims. A true layered replacement
needs layer-aware Green physics, a richer interface basis, or a fresh dense
layered validation ladder.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_boundary_image_layered_replay.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_boundary_image_layered_replay.py
pass
```

Figure check:

```text
project_core_bem_boundary_image_layered_replay.png
2231x1008, dynamic range=255
```
