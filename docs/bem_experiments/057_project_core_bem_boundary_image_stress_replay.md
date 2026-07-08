# BEM Experiment 057: Boundary-Image Stress Replay

Date: 2026-06-25

## Purpose

Stress-test the run `056` boundary-image scattering replay on saved lateral,
geometry, and Tx/Rx offset cases.

This is still a CPU-only BEM/project-core bridge check. It reuses saved
project-core case outputs from runs `042`, `044`, and `045`; it does not run
new FDTD, field preprocessing, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/057_project_core_bem_boundary_image_stress_replay
```

Key artifacts:

```text
data/project_core_bem_boundary_image_stress_replay.csv
data/project_core_bem_boundary_image_stress_replay_summary.json
figures/project_core_bem_boundary_image_stress_replay.png
docs/PROJECT_CORE_BEM_BOUNDARY_IMAGE_STRESS_REPLAY.md
```

## Result

```text
stress cases:                       10
worst boundary-image all-scan L2:   0.543696265768155
worst boundary-image LOO L2:        0.667995713341894
worst project-grid L2:              0.47273720520920215
stress replay ready:                true
```

Case metrics:

| Group | Case | Project-grid L2 | Boundary LOO L2 | LOO variant |
| --- | --- | ---: | ---: | --- |
| lateral_dense | center_dense_epsr4 | 0.4562437767492717 | 0.667995713341894 | product_no_div |
| lateral_shift | left_shift_epsr4 | 0.4282834683853741 | 0.6283703831876847 | receiver_conjugate_div_source |
| lateral_shift | right_shift_epsr4 | 0.47273720520920215 | 0.6485547348112422 | product_no_div |
| depth_radius | shallow_z_epsr4 | 0.4676059535354029 | 0.5724562814650415 | product_no_div |
| depth_radius | deep_z_epsr4 | 0.43263904624975796 | 0.5251741186206315 | product_no_div |
| depth_radius | small_radius_epsr4 | 0.33350467631625413 | 0.41590110103815076 | product_no_div |
| depth_radius | large_radius_epsr4 | 0.406172653375023 | 0.5266911177309223 | receiver_conjugate_div_source |
| offset | offset_10mm_epsr4 | 0.41652920661270654 | 0.569862288500426 | receiver_conjugate_div_source |
| offset | offset_30mm_epsr4 | 0.4475737608979965 | 0.6050442467130362 | product_div_source |
| offset | offset_40mm_epsr4 | 0.43534169321425303 | 0.5715646609337404 | product_no_div |

## Interpretation

The boundary-image replacement passes saved lateral-density, lateral-shift,
depth, radius, and Tx/Rx-offset stress cases under leave-one-scan scattering
replay.

This makes the boundary-image model the current BEM-derived homogeneous 2D
replacement candidate. It is stronger than the earlier project-domain
target-cell surface because it is no longer only replaying the base contrast
ladder; it has now survived saved geometry and acquisition variations.

## Decision

Use the boundary-image model as the active homogeneous 2D BEM replacement
candidate.

Do not promote it to layered, field, 3D, FWI, GPU, or historical
`outputs/experiments` archive claims. The next gate is layered replay or a
compact contract refresh that states exactly where the replacement is valid.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_boundary_image_stress_replay.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_boundary_image_stress_replay.py
pass
```

Figure check:

```text
project_core_bem_boundary_image_stress_replay.png
2125x919, dynamic range=255
```
