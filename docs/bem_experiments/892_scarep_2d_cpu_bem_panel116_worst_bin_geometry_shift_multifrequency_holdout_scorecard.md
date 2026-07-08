# BEM Experiment 892: Panel-116 Worst-Bin Geometry-Shift Multi-Frequency Holdout Scorecard

Date: 2026-07-01

## Purpose

Test whether the best single-bin geometry proxy from run `890` survives across
the full 116-panel frequency grid.

The tested proxy is a common source/receiver vertical shift of `+0.15 mm`.
This run reruns the 116-panel CPU BEM target case across 25 frequencies and
compares the same BEM response against both the baseline analytic reference and
the shifted analytic reference. It does not run project FDTD, field processing,
3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/892_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_multifrequency_holdout_scorecard
```

## Result

```text
source geometry scorecard ready:          true
source geometry validation ready:         true
tested shift:                             common_z_plus_0p15mm
tested shift value:                       0.15 mm
frequency count:                          25
high-band frequency count:                 9
target relative L2:                       0.001
wall seconds:                             65.29120930796489
baseline full-band relative L2:           0.0003383618947272846
shifted full-band relative L2:            0.0004561554424179171
baseline high-band relative L2:           0.0009518291083452528
shifted high-band relative L2:            0.0007586109080035837
baseline per-frequency pass count:        23
shifted per-frequency pass count:         19
baseline high-band pass count:             7
shifted high-band pass count:              5
baseline worst frequency:                 2.3125 GHz
baseline worst relative L2:               0.0020304660813911003
shifted worst frequency:                  3.0 GHz
shifted worst relative L2:                0.0016529582704013506
original worst bin repaired:              true
high-band aggregate improves:             true
full-band aggregate improves:             false
per-frequency pass count improves:        false
multi-frequency holdout passes:           false
geometry-shift correction promoted:       false
project FDTD comparison ready:            false
field transfer ready:                     false
real 3D validation ready:                 false
gpu priority:                             none
```

High-band frequency rows:

| Frequency (GHz) | Baseline relative L2 | Shifted relative L2 | Baseline pass | Shifted pass | Shift improves |
| ---: | ---: | ---: | --- | --- | --- |
| 2.083333333333333 | 0.0004436868487678074 | 0.0007336972859155485 | true | true | false |
| 2.1979166666666665 | 0.0005216069052595891 | 0.00022120375591023217 | true | true | true |
| 2.3125 | 0.0020304660813911003 | 0.00029663254700154477 | false | true | true |
| 2.427083333333333 | 0.0004092037546254354 | 0.0014507617705892283 | true | false | false |
| 2.5416666666666665 | 0.0005526488245481426 | 0.0010978676197812396 | true | false | false |
| 2.65625 | 0.001124829226316987 | 0.0009818012225533124 | false | true | true |
| 2.770833333333333 | 0.0006783429800694514 | 0.0008974294720370662 | true | true | false |
| 2.8854166666666665 | 0.0005607606328217628 | 0.0015917864125605012 | true | false | false |
| 3.0 | 0.0005620505398097652 | 0.0016529582704013506 | true | false | false |

## Interpretation

The `+0.15 mm` common vertical proxy repairs the original `2.3125 GHz` worst
bin and improves the aggregate high-band error. However, it worsens the
full-band aggregate error, reduces the total per-frequency pass count from 23
to 19, reduces the high-band pass count from 7 to 5, and moves the worst
above-target bin to `3.0 GHz`.

This means the vertical proxy is a useful diagnostic lead, not a correction.
It likely captures part of the source/receiver representation error near the
original worst bin, but a fixed height shift is too blunt across frequency.

## Decision

Do not promote the geometry-shift proxy. The next useful BEM branch is a
constrained frequency-aware source/receiver model or a boundary/source
representation change that preserves the gains at `2.3125 GHz` without
creating new upper-band failures.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_multifrequency_holdout_scorecard.py
4 passed
```

Figure check:

```text
2788x870, dynamic range=255
```

