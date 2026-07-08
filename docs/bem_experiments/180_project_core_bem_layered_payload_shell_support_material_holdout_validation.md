# BEM Experiment 180: Layered Payload Shell-Support Material Holdout Validation

Date: 2026-06-28

## Purpose

Validate the 11 mm shell-support rule on 35 mm material and interface holdout
cases.

Run `178` validated the shell rule on neighboring geometry changes. This run
checks whether the same shell rule holds when the larger-radius target contrast
or lower-halfspace contrast changes.

This run reruns local CPU project-core FDTD/BEM adapter comparisons. It does
not compare against field data, run 3D validation, launch GPU/HPC work, or run
field FWI.

## Output

```text
outputs/bem_experiments/180_project_core_bem_layered_payload_shell_support_material_holdout_validation
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_material_holdout_rows.csv
data/project_core_bem_layered_payload_shell_support_material_holdout_worst_payload_arrays.npz
data/project_core_bem_layered_payload_shell_support_material_holdout_validation_summary.json
figures/project_core_bem_layered_payload_shell_support_material_holdout_validation.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_MATERIAL_HOLDOUT_VALIDATION.md
scripts/run_project_core_bem_layered_payload_shell_support_material_holdout_validation.py
scripts/run_project_core_bem_layered_payload_shell_support_holdout_validation.py
scripts/test_project_core_bem_layered_payload_shell_support_material_holdout_validation.py
```

## Result

```text
material holdout cases:              3
support rows:                        6
volume pass count:                   3
shell pass count:                    3
shell failed count:                  0
acceptance L2 gate:                  0.75
worst shell case:                    radius35_low_contrast_epsr7p5
worst shell leave-one L2:            0.7109170307749919
mean shell-vs-volume improvement:    0.017563841009369696
shell material holdout ready:        true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

| Case | Volume L2 | 11 mm shell L2 | Shell ready |
| --- | ---: | ---: | --- |
| radius35_low_contrast_epsr7p5 | 0.7263009768189804 | 0.7109170307749919 | true |
| radius35_high_target_epsr12 | 0.6687223058876123 | 0.6594947255694751 | true |
| radius35_high_interface_epsr12 | 0.6043329056909441 | 0.5762529090249607 | true |

## Interpretation

The 11 mm shell rule passes all three material/interface holdouts and improves
all three relative to full-volume support. The worst shell result remains below
the `0.75` gate at `0.7109170307749919`.

This strengthens the local 2D layered-payload BEM evidence beyond geometric
holdouts, but it still does not establish measured-field transfer or 3D
validity.

## Decision

Use this as the material/interface shell-support validation checkpoint.

Keep field transfer, 3D validation, GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_holdout_validation.py
tests/test_project_core_bem_layered_payload_shell_support_material_holdout_validation.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_material_holdout_validation.py: pass
tests/test_project_core_bem_layered_payload_shell_support_material_holdout_validation.py: pass
```

Figure check:

```text
2986x770, dynamic range=255
```
