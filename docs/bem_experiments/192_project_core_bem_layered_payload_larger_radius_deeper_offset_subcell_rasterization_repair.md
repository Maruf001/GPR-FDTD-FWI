# BEM Experiment 192: Deeper-Offset Subcell Rasterization Repair

Date: 2026-06-27

## Purpose

Test whether the known deeper `z_plus_2p5mm` 35 mm larger-radius failure is
caused by target rasterization on the FDTD grid.

Run `191` showed that radial target weighting improves the failure but does not
bring it below the `0.75` acceptance gate. This run changes the subcell
rasterization density for the same target, while comparing full-volume support,
the original 11 mm shell, and the best radial shell candidate from run `191`.

This is a CPU-only local project-core FDTD/BEM adapter run. It does not compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/192_project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair_summary.json
data/project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_best_payload_shapes.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_best_payload_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_SUBCELL_RASTERIZATION_REPAIR.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.py
```

## Result

```text
subcell sample counts:              5
support rows:                      15
ready support count:                0
source best support mode:           outer_shell_18mm_linear_radial
source best leave-one L2:           0.7525645647728268
default sample best L2:             0.7525645647728268
best subcell samples:               5
best support mode:                  outer_shell_18mm_linear_radial
best leave-one L2:                  0.7525645647728268
best acceptance margin:            -0.0025645647728268495
subcell rasterization repair ready: false
depth repair validation ready:      false
contract refresh ready:             false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The best rows were:

| Rank | Subcell samples | Support mode | Active cells | Leave-one L2 | Ready |
| ---: | ---: | --- | ---: | ---: | --- |
| 1 | 5 | outer_shell_18mm_linear_radial | 785 | 0.7525645647728268 | false |
| 2 | 3 | outer_shell_18mm_linear_radial | 777 | 0.753723324265082 | false |
| 3 | 7 | outer_shell_18mm_linear_radial | 785 | 0.7537811274963909 | false |
| 4 | 11 | outer_shell_18mm_linear_radial | 787 | 0.753794254705023 | false |
| 5 | 9 | outer_shell_18mm_linear_radial | 787 | 0.7538574469794795 | false |

## Interpretation

The deeper-offset failure is not repaired by changing subcell rasterization
density. The default five-sample rasterization remains the best case, and all
tested rasterizations stay above the `0.75` L2 acceptance gate.

This narrows the likely blocker. The failure is less likely to be a simple
target rasterization artifact and more likely to require an operator/source
model change, a different Green-surface representation, or a more explicit
boundary treatment.

## Decision

Do not refresh the shell-support contract from subcell rasterization. Keep the
run `181` scoped local 2D BEM/FDTD contract and the run `188` depth-boundary
failure. The next BEM repair should target the operator/source model rather
than only the target rasterization. Keep field transfer, 3D validation,
GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.py
7 passed
```

Figure validation:

```text
project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.png
3040x818, dynamic range=255
```
