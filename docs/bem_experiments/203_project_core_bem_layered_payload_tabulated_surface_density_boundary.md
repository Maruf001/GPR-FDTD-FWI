# BEM Experiment 203: Tabulated Surface Density Boundary

Date: 2026-06-28

## Purpose

Measure how dense the tabulated field surface must be for the guarded
tabulated-surface BEM repair to remain valid across the five tested 35 mm
offset cases.

This run reruns local CPU project-core FDTD/BEM adapter cases. It does not
compare against field data, launch GPU/HPC work, run 3D validation, run field
FWI, or promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/203_project_core_bem_layered_payload_tabulated_surface_density_boundary
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_policy_summary.csv
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_density_boundary.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_DENSITY_BOUNDARY.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_density_boundary.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_density_boundary.py
```

## Result

```text
offset cases:                                5
support modes:                               3
surface policies:                            5
support/policy rows:                         75
ready support/policy rows:                   33
all-case-ready policies:                     3
minimum all-case-ready policy:               dense_10mm_plus_exact
minimum all-case-ready max sample count:     19
minimum all-case-ready worst best L2:        0.650662226077945
minimum all-case-ready margin:               0.099337773922055
coarser grid than 10 mm all-case ready:      true
coarser grid than 10 mm best policy:         dense_15mm_plus_exact
lower sample count than 10 mm all-case ready:false
best overall policy:                         dense_5mm_plus_exact
best overall leave-one L2:                   0.5651855941104873
density-boundary ready:                      true
analytic contract refresh ready:             false
field transfer ready:                        false
3D validation ready:                         false
GPU work ready:                              false
field FWI ready:                             false
```

Policy summary:

| Policy | Max samples | Ready cases | Worst best case | Worst best support | Worst best L2 | Margin | All cases ready |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| exact source/receiver only | 10 | 0 | z_minus_2p5mm | volume_full | 1.096856452174814 | -0.3468564521748141 | false |
| 20 mm plus exact | 14 | 0 | z_minus_2p5mm | outer_shell_11mm_binary | 0.8612125686585872 | -0.1112125686585872 | false |
| 15 mm plus exact | 23 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.6075420339182941 | 0.1424579660817059 | true |
| 10 mm plus exact | 19 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.650662226077945 | 0.099337773922055 | true |
| 5 mm plus exact | 37 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.5917389381889764 | 0.15826106181102362 | true |

## Interpretation

The exact source/receiver-only surface and 20 mm plus exact policy are not
enough for this five-case offset family. The 15 mm, 10 mm, and 5 mm plus exact
policies all keep every tested offset case below the acceptance gate.

The 15 mm policy is a coarser grid spacing than 10 mm, but it is not cheaper in
actual sample count here because the exact source and receiver positions must be
inserted. It uses 23 samples, while the 10 mm plus exact policy uses 19 samples.
The 5 mm policy gives the best overall L2, but it uses 37 samples.

## Decision

Use 10 mm plus exact as the current cheapest all-case-ready tabulated-surface
policy for follow-on BEM repair checks. Treat 5 mm plus exact as the higher-cost
accuracy reference and 15 mm plus exact as a viable but not lower-sample
alternative. Keep analytic replacement, field transfer, 3D validation, GPU/HPC,
field FWI, and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_density_boundary.py
4 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_density_boundary.png
3041x904, dynamic range=255
```
