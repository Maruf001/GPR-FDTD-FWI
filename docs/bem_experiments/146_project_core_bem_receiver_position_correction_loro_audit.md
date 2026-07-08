# BEM Experiment 146: Receiver-Position Correction LORO Audit

Date: 2026-06-27

## Purpose

Test receiver-position correction under leave-one-receiver-out validation.

Run `145` defined the promotion contract for receiver-edge modeling. This run
tests one concrete correction family: polynomial complex correction as a
function of aperture midpoint position, evaluated by holding out one receiver
row at a time.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/146_project_core_bem_receiver_position_correction_loro_audit
```

Key artifacts:

```text
data/project_core_bem_receiver_position_correction_degree_summary.csv
data/project_core_bem_receiver_position_correction_holdout_rows.csv
data/project_core_bem_receiver_position_correction_loro_audit_summary.json
figures/project_core_bem_receiver_position_correction_loro_audit.png
docs/PROJECT_CORE_BEM_RECEIVER_POSITION_CORRECTION_LORO_AUDIT.md
scripts/run_project_core_bem_receiver_position_correction_loro_audit.py
scripts/test_project_core_bem_receiver_position_correction_loro_audit.py
```

## Result

```text
baseline scaled relative L2:        0.117062890994582
polynomial degrees tested:          4
best polynomial degree:             2
best LORO spectral relative L2:     0.1082856299479433
best degree receiver rows passing:  5
best degree passes gate:            false
improvement factor:                 1.0810565635611875
receiver-position correction ready: false
project-core bridge ready:          false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Degree summary:

| Degree | LORO spectral L2 | Receiver rows passing | Worst receiver L2 | Passes gate |
| ---: | ---: | ---: | ---: | --- |
| 0 | 0.13827151342965752 | 2 | 0.1760485693829015 | false |
| 1 | 0.17259215295088212 | 2 | 0.2907776822781744 | false |
| 2 | 0.1082856299479433 | 5 | 0.17298631269723536 | false |
| 3 | 0.19291184932894528 | 3 | 0.38264010854953834 | false |

## Interpretation

A quadratic receiver-position correction improves the leave-one-receiver-out
metric from `0.117062890994582` to `0.1082856299479433`, but it still does not
pass the `0.1` gate. Edge holdouts remain above the gate. The result therefore
does not satisfy the receiver-edge promotion contract from run `145`.

## Decision

Do not promote receiver-position correction, project-core comparison, 3D
validation, GPU/HPC escalation, or field FWI from this result. Keep
receiver-edge modeling as an open adapter problem.

## Validation

Focused tests:

```text
tests/test_project_core_bem_receiver_position_correction_loro_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_receiver_position_correction_loro_audit.png
2896x845, dynamic range=255
```
