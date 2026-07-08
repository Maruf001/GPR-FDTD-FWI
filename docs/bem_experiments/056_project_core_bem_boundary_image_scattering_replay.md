# BEM Experiment 056: Boundary-Image Scattering Replay

Date: 2026-06-25

## Purpose

Replay the discrete scattering adapter with the run `055` boundary-image
field-table replacement candidate.

This is a CPU-only scattering replay gate. It uses held-out scan validation:
for each held-out scan, the boundary-image field model is trained without that
scan's Tx/Rx field-table positions, then the scattering scale is fit on the
remaining scans. It does not use field data, GPU work, FWI, 3D/HPC, neural
networks, or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/056_project_core_bem_boundary_image_scattering_replay
```

Key artifacts:

```text
data/project_core_bem_boundary_image_scattering_replay.csv
data/project_core_bem_boundary_image_scattering_replay_summary.json
figures/project_core_bem_boundary_image_scattering_replay.png
docs/PROJECT_CORE_BEM_BOUNDARY_IMAGE_SCATTERING_REPLAY.md
```

## Result

```text
cases checked:                      3
worst all-scan replay L2:           0.4375137396284387
worst leave-one-scan replay L2:     0.5620892946687726
boundary-image scattering ready:    true
project-grid best worst L2:         0.44601690298659386
gpu required:                       false
```

Metrics:

| epsr | Project-grid L2 | Boundary all-scan L2 | Boundary LOO L2 | LOO variant | Ready |
| ---: | ---: | ---: | ---: | --- | --- |
| 1.25 | 0.0989465314024021 | 0.2226963599106419 | 0.34541581723563025 | product_no_div | true |
| 2.0 | 0.23018542478328735 | 0.3096727101433991 | 0.4156849542835839 | product_div_source | true |
| 4.0 | 0.44601690298659386 | 0.4375137396284387 | 0.5620892946687726 | receiver_conjugate_div_source | true |

## Interpretation

The boundary-image field-table replacement passes the discrete scattering
replay gate under leave-one-scan validation across the tested contrast ladder.

This is the first BEM-derived 2D homogeneous project-core replacement candidate
that passes both the field-table gate and the target-scattering replay gate.

## Decision

Promote the boundary-image model as the current BEM-derived 2D replacement
candidate for the tested homogeneous project-core adapter. Field, 3D, FWI, GPU,
and historical-archive claims remain blocked.

## Validation

```text
python -m py_compile run_project_core_bem_boundary_image_scattering_replay.py
python run_project_core_bem_boundary_image_scattering_replay.py
```

Figure check:

```text
project_core_bem_boundary_image_scattering_replay.png: 1745x787, dynamic range=255
```
