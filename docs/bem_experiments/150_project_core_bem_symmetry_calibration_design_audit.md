# BEM Experiment 150: Symmetry Calibration Design Audit

Date: 2026-06-27

## Purpose

Test pre-registered receiver calibration designs for the symmetry-constrained
project-core BEM/FDTD correction.

Run `148` showed that an even aperture-position correction passes
leave-one-receiver-out but fails leave-one-symmetry-pair-out, mainly because
the edge pair cannot be inferred when both edge receivers are withheld. Run
`149` validated that no-go. This run asks the next practical design question:
which receiver subset must be included in a calibration set before the
symmetry correction can predict the remaining receivers?

This is a CPU-only audit from saved bridge arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/150_project_core_bem_symmetry_calibration_design_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_design_rows.csv
data/project_core_bem_symmetry_calibration_design_audit_summary.json
figures/project_core_bem_symmetry_calibration_design_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_DESIGN_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_design_audit.py
scripts/test_project_core_bem_symmetry_calibration_design_audit.py
```

## Result

```text
baseline scaled relative L2:             0.117062890994582
calibration designs tested:              9
model rows:                              28
passing calibration designs:             1
passing no-edge designs:                 0
edge pair required by passing designs:   true
best passing design:                     edge_pair_plus_inner_pair
best passing degree:                     1
best passing train receivers:            0;2;4;6
best passing holdout receivers:          1;3;5
best passing overall relative L2:        0.06410622276417251
best passing holdout relative L2:        0.08334442794624965
design candidate ready:                  true
project-core bridge ready:               false
3D validation ready:                     false
field FWI ready:                         false
GPU/HPC ready:                           false
```

Key design outcome:

| Design | Degree | Train receivers | Holdout receivers | Holdout L2 | Holdout rows passing | Passes |
| --- | ---: | --- | --- | ---: | ---: | --- |
| interior_without_edges | 1 | 1;2;3;4;5 | 0;6 | 0.22459384513474856 | 0 / 2 | false |
| edge_pair_plus_center | 1 | 0;3;6 | 1;2;4;5 | 0.10116490954880135 | 2 / 4 | false |
| edge_pair_plus_inner_pair | 1 | 0;2;4;6 | 1;3;5 | 0.08334442794624965 | 3 / 3 | true |
| edge_pair_plus_near_edge_pair | 1 | 0;1;5;6 | 2;3;4 | 0.15836370213478212 | 0 / 3 | false |

## Interpretation

The saved project-core case needs edge receivers in the calibration set. No
design without both edge receivers passes. The best passing holdout design is
`edge_pair_plus_inner_pair` with degree `1`, using receivers `0`, `2`, `4`,
and `6` to predict receivers `1`, `3`, and `5`.

This explains the run `148` failure more constructively. The issue is not only
that the edge pair is hard; the candidate correction needs the edge pair plus
an interior symmetric pair to generalize across the aperture on this saved
case.

## Decision

Treat `edge_pair_plus_inner_pair`, degree `1`, as the next BEM adapter
candidate. Do not promote the project-core bridge from this single saved-case
result. A fresh matched case or new project-core comparison must validate the
candidate before 3D validation, GPU/HPC, or field FWI escalation.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_design_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_design_audit.png
2932x839, dynamic range=255
```
