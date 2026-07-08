# BEM Experiment 890: Panel-116 Worst-Bin Geometry-Shift Proxy Scorecard

Date: 2026-07-01

## Purpose

Check whether the remaining `2.3125 GHz` worst-bin mismatch can be explained
by a small source/receiver sampling-position proxy.

This run reads the saved run `869` complex receiver responses and the guarded
phase-only block from runs `887-889`. It compares the saved BEM response
against analytic references with small millimeter-scale source and receiver
position shifts. It does not rerun BEM, project FDTD, field processing, 3D/HPC
work, or GPU kernels.

## Output

```text
outputs/bem_experiments/890_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_proxy_scorecard
```

## Result

```text
source spatial audit ready:             true
source phase validation ready:          true
source phase sensitivity ready:         true
receiver rows:                          13
candidate shifts:                       36
frequency:                              2.3125 GHz
target relative L2:                     0.001
baseline relative L2:                   0.0020304660813910734
best candidate:                         common_z_plus_0p15mm
best shift mode:                        common_z
best shift:                             0.15 mm
best candidate relative L2:             0.0002966325470015585
best reduction fraction:                0.8539091345971486
target-passing candidates:              13
vertical-shift passing candidates:      13
horizontal-shift passing candidates:     0
single-frequency geometry proxy passes: true
multi-frequency holdout required:       true
geometry-shift correction promoted:     false
project FDTD comparison ready:          false
field transfer ready:                   false
real 3D validation ready:               false
gpu priority:                           none
```

Top candidate rows:

| Candidate | Relative L2 | Passes target | Reduction fraction |
| --- | ---: | --- | ---: |
| common z +0.15 mm | 0.0002966325470015585 | true | 0.8539091345971486 |
| source z +0.30 mm | 0.0003032473147103997 | true | 0.850651376307333 |
| receiver z +0.30 mm | 0.000315455761989989 | true | 0.8446387433500637 |
| source z +0.25 mm | 0.0004437340471816486 | true | 0.7814619750369599 |
| receiver z +0.25 mm | 0.00045575803255199144 | true | 0.7755401891570869 |
| source z +0.35 mm | 0.0004602243328189002 | true | 0.7733405462731984 |
| receiver z +0.35 mm | 0.0004629072739856745 | true | 0.7720192037541763 |

## Interpretation

This is the first branch in the current worst-bin sequence that can close the
single-bin target. A very small upward source/receiver height proxy gives a
large reduction, and all target-passing candidates are vertical shifts. The
horizontal source/receiver shifts do not pass the target.

This result is important but not yet a correction. It is a single-frequency
proxy against an analytic reference. It needs a multi-frequency holdout and a
physical source/receiver interpretation before it can support any correction,
project-FDTD comparison, field transfer, or 3D claim.

## Decision

Use this as the next BEM branch direction: test the vertical geometry proxy
across frequency and holdout conditions. Do not promote a geometry-shift
correction from run `890` alone.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_geometry_shift_proxy_scorecard.py
3 passed
```

Figure check:

```text
3004x928, dynamic range=255
```

