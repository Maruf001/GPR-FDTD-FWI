# BEM Experiment 909: Panel-116 Smooth Frequency-Aware Vertical-Shift Continuous Validation

Date: 2026-07-01

## Purpose

Validate the run `900` smooth frequency-aware source/receiver shift model at
continuous off-grid shift values.

Runs `900-901` showed that a constrained smooth model could pass on the saved
`0.05 mm` shifted grid, and run `905` sensitivity-hardened that scorecard.
Runs `906-908` tested an interpolated surrogate and showed that the bracket
guard remained conservative. This run reruns the 116-panel CPU BEM target
response and compares it against analytic references generated at the actual
continuous gaussian-bump shift values. It does not run project FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/909_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation
```

## Result

```text
source scorecard ready:                 true
source validation ready:                true
source sensitivity ready:               true
model:                                  best_gaussian_bump
model family:                           gaussian_bump
model parameters:                       {"amplitude": 0.05, "base": 0.05, "center": 2.4, "width": 0.25}
frequency count:                        25
high-band frequency count:               9
target relative L2:                     0.001
wall seconds:                           69.11924275802448
continuous pass count:                  25
snapped pass count:                     25
high-band continuous pass count:         9
high-band snapped pass count:            9
continuous worst frequency:             2.65625 GHz
continuous worst relative L2:           0.0008519458802336965
snapped worst frequency:                2.65625 GHz
snapped worst relative L2:              0.0008518855375610986
continuous mean relative L2:            0.0002917621007092406
snapped mean relative L2:               0.00028589085415242193
max absolute continuous/snapped delta:  0.00008112758940537559
continuous shift min:                   0.05000000000000001 mm
continuous shift max:                   0.09970745639274738 mm
continuous shift range:                 0.049707456392747366 mm
off-grid continuous shifts:             true
BEM continuous validation passes:       true
project FDTD comparison candidate:      true
project FDTD comparison completed:      false
smooth correction promoted:             false
field transfer ready:                   false
real 3D validation ready:               false
gpu priority:                           none
```

High-band continuous-shift rows:

| Frequency (GHz) | Continuous shift (mm) | Continuous relative L2 | Pass |
| ---: | ---: | ---: | --- |
| 2.083333333333333 | 0.07241657819704714 | 0.0002561041908356912 | true |
| 2.1979166666666665 | 0.08606495493982644 | 0.00011740460859001224 | true |
| 2.3125 | 0.09702940316821712 | 0.0007614996480819704 | true |
| 2.427083333333333 | 0.09970745639274738 | 0.0008306336427952645 | true |
| 2.5416666666666665 | 0.09258352536147206 | 0.0005072445459545418 | true |
| 2.65625 | 0.07956852660984905 | 0.0008519458802336965 | true |
| 2.770833333333333 | 0.06664124274067677 | 0.00021564780358212675 | true |
| 2.8854166666666665 | 0.05759118938393067 | 0.0003417009297232601 | true |
| 3.0 | 0.05280673814170669 | 0.0003080611230491309 | true |

## Interpretation

The smooth gaussian-bump source/receiver shift model survives the off-grid
continuous-shift check. It keeps every tested frequency below the `0.001`
relative-L2 target, including the high-band frequencies that controlled the
previous failure.

The continuous and snapped results are nearly identical at the worst frequency,
with a maximum absolute relative-L2 difference of about `8.11e-05` across the
full band. This means the run `900` result was not merely an artifact of
snapping to the saved `0.05 mm` grid.

## Decision

Treat the smooth source/receiver model as a BEM-side candidate for a guarded
project-FDTD comparison design. Do not promote a field, 3D, or correction claim
from this result alone.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_continuous_validation.py
4 passed
```

Figure check:

```text
2824x870, dynamic range=255
```
