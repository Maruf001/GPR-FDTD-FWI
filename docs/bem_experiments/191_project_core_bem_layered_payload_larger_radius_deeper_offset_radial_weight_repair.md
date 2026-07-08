# BEM Experiment 191: Larger-Radius Deeper-Offset Radial Weight Repair

Date: 2026-06-28

## Purpose

Test radial target-weight profiles for the failing deeper +2.5 mm 35 mm
larger-radius case.

Runs `186`-`190` showed that the deeper offset is a known shell-support failure
and that shell thickness alone does not repair it. This run keeps the same local
BEM/FDTD observable but changes the target-cell weighting profile.

This run reruns one local CPU project-core FDTD case through the BEM adapter. It
does not compare against field data, launch GPU/HPC work, run 3D validation, or
run field FWI.

## Output

```text
outputs/bem_experiments/191_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair_best_payload_shapes.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair_summary.json
data/project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair_best_payload_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_RADIAL_WEIGHT_REPAIR.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py
```

## Result

```text
weighted support modes:              8
ready support modes:                 0
baseline binary shell L2:            0.7549628470028724
best support mode:                   outer_shell_18mm_linear_radial
best leave-one L2:                   0.7525645647728268
best acceptance margin:              -0.0025645647728268495
best vs binary shell improvement:    0.0023982822300455675
radial weight repair ready:          false
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

## Interpretation

Radial target weighting improves the deeper-offset failure but does not repair
it. The best row is `outer_shell_18mm_linear_radial` with L2
`0.7525645647728268`, improving the binary 11 mm shell by
`0.0023982822300455675` but still missing the `0.75` gate.

## Decision

Do not refresh the shell-support contract from radial weighting alone.

The next repair must change the deeper-offset model/grid treatment more
substantially. Keep field transfer, 3D validation, GPU/HPC, field FWI, and
synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_radial_weight_repair.py: pass
```

Figure check:

```text
3040x815, dynamic range=255
```
