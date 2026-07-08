# BEM Experiment 108: Bempp Receiver-Height Sensitivity

Date: 2026-06-27

## Purpose

Check how much the local 3D Bempp finite-rebar response changes when the
receiver-line height changes while the source convention is locked.

Runs `106` and `107` established a stable baseline mesh and showed that source
orientation, source position, and source height must be explicit comparison
metadata. This run asks the matching receiver-side question:

```text
Can future paired 3D FDTD data treat receiver geometry loosely, or must receiver
height and coordinates be locked explicitly?
```

This is a homogeneous frequency-domain BEM sensitivity audit. It does not run
3D FDTD, use measured field data, launch GPU/HPC work, or validate a layered 3D
GPR forward model.

## Output

```text
outputs/bem_experiments/108_project_core_bem_bempp_receiver_height_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_receiver_height_variants.csv
data/project_core_bem_bempp_receiver_height_frequency_summary.csv
data/project_core_bem_bempp_receiver_height_receivers.csv
data/project_core_bem_bempp_receiver_height_comparisons.csv
data/project_core_bem_bempp_receiver_height_sensitivity_summary.json
figures/project_core_bem_bempp_receiver_height_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_RECEIVER_HEIGHT_SENSITIVITY.md
scripts/run_project_core_bem_bempp_receiver_height_sensitivity.py
scripts/test_project_core_bem_bempp_receiver_height_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
receiver-height variants:           4
frequencies checked:                2
receiver rows:                      248
comparison rows:                    6
finite all responses:               true
Bempp return codes all zero:         true
height max relative L2:              0.19131367619758774
height max shape L2:                 0.039446254706971995
receiver metadata critical:          true
receiver convention lock ready:      true
3D FDTD validation ready:            false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Comparisons to the baseline receiver line at `z=0.09 m`:

| Frequency GHz | Variant | Receiver height m | Relative L2 | Shape L2 | Peak ratio |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.5 | receiver_z075 | 0.075 | 0.13056525 | 0.02900336 | 1.16317419 |
| 0.5 | receiver_z105 | 0.105 | 0.10494320 | 0.02199746 | 0.87564530 |
| 0.5 | receiver_z120 | 0.120 | 0.19131368 | 0.03897736 | 0.77769519 |
| 1.5 | receiver_z075 | 0.075 | 0.11817849 | 0.03074005 | 1.15399935 |
| 1.5 | receiver_z105 | 0.105 | 0.09935438 | 0.02256331 | 0.87996173 |
| 1.5 | receiver_z120 | 0.120 | 0.18319686 | 0.03944625 | 0.78419149 |

## Interpretation

The local 3D Bempp response is materially sensitive to receiver-line height. A
15 mm height shift changes the receiver-line response by about 10% to 13%, and
the larger 30 mm upward shift reaches about 19% in this bounded test.

Receiver height affects both amplitude and line shape. The response is not
stable enough to treat receiver geometry as approximate in a future paired 3D
BEM/FDTD comparison.

## Decision

Lock the current BEM-side receiver convention to 31 receiver samples over a
0.16 m y-span at `z=0.09 m` unless a later paired FDTD design deliberately
changes it.

Treat receiver coordinates, height, span, and sample count as required metadata
for any future 3D BEM/FDTD comparison.

This does not validate 3D BEM against FDTD and does not promote the result to a
layered 3D GPR model, field FWI input, or GPU/HPC workflow.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_bempp_receiver_height_sensitivity.py
sha256: fbdd676ac2003f431688f103a7437d0dc4b5b50cad060acf0eb3cc2819f09a16

test_project_core_bem_bempp_receiver_height_sensitivity.py
sha256: 9e925d1fa3ab6fcb20506ac2fa00f48049d0c3f75a886aa1fd545c22fd4d72c8
```

Subsequent Bempp 3D comparison-design experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_receiver_height_sensitivity.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_receiver_height_sensitivity.png
2680x848, dynamic range=255
```
