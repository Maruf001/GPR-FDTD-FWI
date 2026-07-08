# BEM Experiment 144: Aperture Residual Geometry Audit

Date: 2026-06-27

## Purpose

Check whether the run `143` receiver-local residual pattern is associated with
aperture position rather than Tx/Rx offset.

Run `143` showed that post-hoc receiver exclusions can pass the gate, but the
full aperture still fails. This run adds the geometry interpretation: all
receiver rows have the same Tx/Rx offset, so the residual pattern must be tied
to aperture position or receiver-edge modeling rather than offset length.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/144_project_core_bem_aperture_residual_geometry_audit
```

Key artifacts:

```text
data/project_core_bem_aperture_residual_receiver_geometry.csv
data/project_core_bem_aperture_residual_symmetry_pairs.csv
data/project_core_bem_aperture_residual_geometry_audit_summary.json
figures/project_core_bem_aperture_residual_geometry_audit.png
docs/PROJECT_CORE_BEM_APERTURE_RESIDUAL_GEOMETRY_AUDIT.md
scripts/run_project_core_bem_aperture_residual_geometry_audit.py
scripts/test_project_core_bem_aperture_residual_geometry_audit.py
```

## Result

```text
best candidate:                         separable_receiver_frequency_complex_scale
receiver count:                         7
Tx/Rx offset min m:                     0.01999999999999999
Tx/Rx offset max m:                     0.020000000000000018
Tx/Rx offset span m:                    2.7755575615628914e-17
edge receiver residual fraction:        0.4414221920328564
center receiver residual fraction:      0.20007002360452517
edge plus center residual fraction:     0.6414922156373816
top symmetry pair:                      0-6
top symmetry-pair residual fraction:    0.4414221920328564
project-core bridge ready:              false
field FWI ready:                        false
GPU/HPC ready:                          false
```

Symmetry-pair table:

| Pair | Residual energy fraction | Energy imbalance | Left L2 | Right L2 |
| --- | ---: | ---: | ---: | ---: |
| 0-6 | 0.4414221920328564 | 0.017470122046559705 | 0.16298900297213478 | 0.16821359868563193 |
| 1-5 | 0.1560857257325684 | 0.00554400742672026 | 0.08534758838547177 | 0.0891203459127813 |
| 2-4 | 0.2024220586300501 | 0.038079974379570364 | 0.10042620351760659 | 0.08395878170575445 |
| 3 | 0.20007002360452517 | 0.0 | 0.12504188517902454 | 0.12504188517902454 |

## Interpretation

The Tx/Rx offset is effectively constant across all receiver rows. The
receiver-local residual is therefore tied to aperture position. The edge pair
alone carries about `44.1%` of residual energy, and the edge pair plus center
receiver carries about `64.1%`.

This gives the next BEM adapter target a sharper shape: aperture-position
effects and receiver-edge modeling.

## Decision

Keep the project-core BEM/FDTD bridge blocked. The next adapter work should
focus on aperture-position effects and receiver-edge modeling before any 3D
validation, GPU/HPC escalation, or field FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_aperture_residual_geometry_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_aperture_residual_geometry_audit.png
2896x845, dynamic range=255
```
