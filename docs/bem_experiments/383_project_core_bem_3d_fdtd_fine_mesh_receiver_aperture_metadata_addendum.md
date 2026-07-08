# BEM Experiment 383: Fine-Mesh Receiver-Aperture Metadata Addendum

Date: 2026-06-29

## Purpose

Extend the preferred fine-mesh BEM/FDTD return metadata contract after the
guarded receiver-aperture sensitivity result in runs `380-382`.

This run does not stage returned FDTD data, run comparison, make a 3D
validation claim, use field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/383_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum
```

## Result

```text
previous fine-mesh metadata fields:       30
receiver-aperture addendum fields:        5
updated metadata fields:                  35
blocking metadata fields:                 34
nonblocking metadata fields:              1
prefilled template values:                23
blank template values:                    12
first non-point aperture above 5 pct:     10.666666666666657 mm
max 3-sample relative L2:                 0.08009547612144642
max 9-sample relative L2:                 0.44166920910128993
receiver-aperture metadata required:      true
receiver-aperture operator required:      true
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
```

The five new blocking fields are:

| Metadata key | Required value |
| --- | --- |
| `receiver_aperture_model` | `point_receiver_no_aperture_average` |
| `receiver_aperture_sample_count` | `1` |
| `receiver_aperture_span_m` | `0.0` |
| `receiver_aperture_operator_convention` | Match Bempp point receivers unless a matched finite-aperture operator is declared |
| `receiver_aperture_sensitivity_guard` | Run `380` threshold evidence |

## Decision

Use this 35-field metadata template for future preferred nine-bin 3D BEM/FDTD
returns. Keep real comparison and 3D validation blocked until returned files
pass a preflight that includes these aperture fields.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_receiver_aperture_metadata_addendum.py
4 passed
```

Figure check:

```text
3108x860, dynamic range=255
```
