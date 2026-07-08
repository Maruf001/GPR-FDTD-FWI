# BEM Experiment 148: Symmetry-Constrained Aperture Correction Holdout Audit

Date: 2026-06-27

## Purpose

Test whether a pre-registered aperture-symmetry correction can close the
project-core BEM/FDTD bridge residual without dropping receiver rows after
seeing the residual.

Runs `142` through `145` showed that the remaining mismatch is concentrated at
the aperture edges and center, not in Tx/Rx offset. Run `146` then tested a
general receiver-position correction under leave-one-receiver-out validation
and found that the edge receivers still failed. This run tests a more
physically constrained family: the correction is even in aperture position, so
receivers at symmetric positions share the same correction structure.

Two holdout modes are compared:

```text
leave-one-receiver-out:        one receiver withheld at a time
leave-one-symmetry-pair-out:   both symmetric receivers withheld together
```

The second mode is stricter for edge modeling because the edge pair cannot be
learned from the other edge receiver.

This is a CPU-only audit from saved BEM/FDTD bridge arrays. It does not rerun
FDTD, rerun BEM solvers, compare against field data, launch GPU/HPC work, run
3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/148_project_core_bem_symmetry_constrained_aperture_correction_holdout_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_constrained_aperture_correction_model_rows.csv
data/project_core_bem_symmetry_constrained_aperture_correction_holdout_rows.csv
data/project_core_bem_symmetry_constrained_aperture_correction_holdout_audit_summary.json
figures/project_core_bem_symmetry_constrained_aperture_correction_holdout_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CONSTRAINED_APERTURE_CORRECTION_HOLDOUT_AUDIT.md
scripts/run_project_core_bem_symmetry_constrained_aperture_correction_holdout_audit.py
scripts/test_project_core_bem_symmetry_constrained_aperture_correction_holdout_audit.py
```

## Result

```text
baseline scaled relative L2:        0.117062890994582
model rows:                         8
best LORO degree:                   2
best LORO spectral relative L2:     0.06977055235365863
best LORO receiver rows passing:    7 / 7
LORO candidate passes:              true
best LOSPO degree:                  1
best LOSPO spectral relative L2:    0.12895136750102182
best LOSPO holdout groups passing:  2 / 4
LOSPO candidate passes:             false
symmetry correction promotable:     false
project-core bridge ready:          false
3D validation ready:                false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Model summary:

| Holdout mode | Degree | Spectral L2 | Receiver rows passing | Groups passing | Worst receiver L2 | Worst group L2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| leave-one-receiver-out | 0 | 0.13827151342965754 | 2 | 2 | 0.17604856938290153 | 0.17604856938290153 |
| leave-one-receiver-out | 1 | 0.08155501860894676 | 7 | 7 | 0.09705114440495574 | 0.09705114440495574 |
| leave-one-receiver-out | 2 | 0.06977055235365863 | 7 | 7 | 0.09624258088172859 | 0.09624258088172859 |
| leave-one-receiver-out | 3 | 0.08356570741682028 | 5 | 5 | 0.10276849976682592 | 0.10276849976682592 |
| leave-one-symmetry-pair-out | 0 | 0.15433878648784805 | 0 | 0 | 0.20851605909016685 | 0.2059274392560659 |
| leave-one-symmetry-pair-out | 1 | 0.12895136750102182 | 3 | 2 | 0.22502213680517932 | 0.22459384513474856 |
| leave-one-symmetry-pair-out | 2 | 0.1527655213926283 | 5 | 3 | 0.3106450859225372 | 0.30612003560754925 |
| leave-one-symmetry-pair-out | 3 | 0.23805834827724284 | 5 | 3 | 0.4941267605216564 | 0.49012378574856147 |

## Interpretation

The even aperture-position correction is a useful diagnostic candidate. Under
leave-one-receiver-out validation, degree `2` lowers the bridge mismatch from
`0.117062890994582` to `0.06977055235365863`, and all seven receivers pass the
`0.1` gate.

That result does not survive the stricter symmetry-pair holdout. When both
edge receivers are withheld together, the best pair-holdout model is degree
`1`, with spectral relative L2 `0.12895136750102182`. Only two of four holdout
groups pass, and the edge-pair error remains too large. This means the
correction still relies on seeing an edge receiver during calibration.

## Decision

Do not promote the symmetry-constrained aperture correction yet. It is a useful
diagnostic and should inform the next adapter design, but project-core
comparison, 3D validation, GPU/HPC, and field FWI remain blocked until the
edge-pair holdout closes or a fresh matched case validates the correction.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_constrained_aperture_correction_holdout_audit.py
7 passed
```

Figure validation:

```text
project_core_bem_symmetry_constrained_aperture_correction_holdout_audit.png
2896x845, dynamic range=255
```
