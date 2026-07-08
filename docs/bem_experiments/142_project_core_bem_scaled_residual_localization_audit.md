# BEM Experiment 142: Scaled Residual Localization Audit

Date: 2026-06-27

## Purpose

Localize residual energy after the best run `141` phase-corrected observable
scaling candidate.

Runs `137`-`141` showed that phase correction and separable receiver/frequency
scaling help, but still do not pass the `0.1` project-core BEM/FDTD bridge
gate. This run checks whether the remaining residual is diffuse or localized
by frequency and receiver.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/142_project_core_bem_scaled_residual_localization_audit
```

Key artifacts:

```text
data/project_core_bem_scaled_residual_frequency_localization.csv
data/project_core_bem_scaled_residual_receiver_localization.csv
data/project_core_bem_scaled_residual_localization_audit_summary.json
figures/project_core_bem_scaled_residual_localization_audit.png
docs/PROJECT_CORE_BEM_SCALED_RESIDUAL_LOCALIZATION_AUDIT.md
scripts/run_project_core_bem_scaled_residual_localization_audit.py
scripts/test_project_core_bem_scaled_residual_localization_audit.py
```

## Result

```text
best candidate:                    separable_receiver_frequency_complex_scale
overall spectral relative L2:      0.117062890994582
frequency bins passing gate:       8 / 17
receiver rows passing gate:        3 / 7
top3 frequency residual fraction:  0.3631456510078532
top3 receiver residual fraction:   0.6414922156373815
top frequency GHz:                 1.9992717241415452
top receiver index:                6
project-core bridge ready:         false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Top frequency residuals:

| Rank | Frequency GHz | Relative L2 | Residual energy fraction | Passes gate |
| ---: | ---: | ---: | ---: | --- |
| 1 | 1.9992717241415452 | 0.1515923835110713 | 0.128872356293755 | false |
| 2 | 2.374135172418085 | 0.20263987944437079 | 0.12870723662081976 | false |
| 3 | 0.8746813793119261 | 0.20433864277106215 | 0.10556605809327839 | false |

Top receiver residuals:

| Rank | Receiver | Relative L2 | Residual energy fraction | Passes gate |
| ---: | ---: | ---: | ---: | --- |
| 1 | 6 | 0.16821359868563193 | 0.22944615703970803 | false |
| 2 | 0 | 0.16298900297213478 | 0.21197603499314832 | false |
| 3 | 3 | 0.12504188517902454 | 0.20007002360452517 | false |

## Interpretation

The residual after best separable scaling is not uniform. It is localized by
both frequency and receiver. Three frequency bins carry about `36.3%` of the
remaining residual energy, and three receiver rows carry about `64.1%`.

This supports a more specific next adapter target: frequency-local and
receiver-local residual structure, not another global scale, global phase, or
simple weak-source filter.

## Decision

Keep the project-core BEM/FDTD bridge blocked. The next adapter work should
target frequency-local and receiver-local residual structure before any 3D
validation, GPU/HPC escalation, or field FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_scaled_residual_localization_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_scaled_residual_localization_audit.png
2914x845, dynamic range=255
```
