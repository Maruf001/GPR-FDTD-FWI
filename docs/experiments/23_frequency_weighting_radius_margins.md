# Experiment 23: Frequency-Weighted Radius Margins

## Goal

Test the cumulative-frequency/WRI idea on the current radius problem without
letting optimizer pathologies obscure the result.

Question:

```text
When x/z are already in the correct basin, do cumulative frequency weights
increase or decrease the objective margin between the true radius and nearby
wrong radii?
```

This follows the five-paper master plan after Experiment 22 showed that
PEBDD-style bandwidth expansion preserved the x/z basin but did not correct
the high-radius Powell basin.

## Code Changes

Added:

```text
inversion/frequency_weighting.py
tests/test_frequency_weighting.py
run_single_rebar_frequency_weight_matrix.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_frequency_weighting.py -q
6 passed
```

## Planned Matrix

Candidate grid:

```text
x:      250.0 mm
z:      90.0, 90.5, 91.0, 91.5 mm
radius: 5.4-7.8 mm in 0.2 mm steps
```

Frequencies:

```text
1.0 GHz, 1.5 GHz
```

Weight sets:

```text
low_only:          1.0 GHz only
onepointfive_only: 1.5 GHz only
unweighted:        equal 1.0 + 1.5 GHz average
carry_low_25:      25% low-frequency carry + 1.5 GHz
carry_low_50:      50% low-frequency carry + 1.5 GHz
```

## Run Log

### 046_frequency_weight_radius_margin_exact

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_frequency_weight_matrix.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequencies-ghz 1.0,1.5 \
  --weight-sets 'low_only:1,0|onepointfive_only:0,1|unweighted:1,1|carry_low_25:0.25,1|carry_low_50:0.5,1' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --run-name frequency_weight_radius_margin_exact
```

Output:

```text
outputs/experiments/046_frequency_weight_radius_margin_exact
```

Files:

```text
data/frequency_weight_matrix_summary.json
data/frequency_weight_matrix.csv
figures/frequency_weight_radius_profiles.png
```

Plot validation:

```text
frequency_weight_radius_profiles.png: 1481x886 px, dynamic range 255
```

Exact-data margin table:

| Weight set | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| low_only | 6.0 | 6.2 | 3.560e-05 |
| onepointfive_only | 6.0 | 6.2 | 1.037e-03 |
| unweighted | 6.0 | 6.2 | 5.364e-04 |
| carry_low_25 | 6.0 | 6.2 | 8.368e-04 |
| carry_low_50 | 6.0 | 6.2 | 7.033e-04 |

Key candidate values for r=6.2 at x=250 mm, z=90 mm:

```text
1.0 GHz misfit:  3.560e-05
1.5 GHz misfit:  1.037e-03
```

## Interpretation After Exact Matrix

This confirms the earlier cumulative-frequency diagnostic in a cleaner matrix:
the 1.0 GHz objective is a weak radius discriminator for this single-rebar
setup. Equal averaging is therefore not neutral; it dilutes the useful
1.5 GHz radius evidence.

`carry_low_25` is the best compromise among the tested cumulative objectives:
it keeps a low-frequency contribution for basin continuity while recovering
about 81% of the 1.5 GHz-only radius margin. `carry_low_50` is still better
than equal weighting, but it loses more radius separation.

## Next Decision

Run the same matrix at 10% noise first. This is the hardest currently used
stress case and will show whether `carry_low_25` is genuinely useful under
noise or only attractive in exact data. If 10% noise changes the ranking or
selects the wrong radius, follow with a 5% noise matrix to identify the failure
threshold.

### 047_frequency_weight_radius_margin_noise10_seed13

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_frequency_weight_matrix.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequencies-ghz 1.0,1.5 \
  --weight-sets 'low_only:1,0|onepointfive_only:0,1|unweighted:1,1|carry_low_25:0.25,1|carry_low_50:0.5,1' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --run-name frequency_weight_radius_margin_noise10_seed13
```

Output:

```text
outputs/experiments/047_frequency_weight_radius_margin_noise10_seed13
```

Plot validation:

```text
frequency_weight_radius_profiles.png: 1481x886 px, dynamic range 255
```

10% noise margin table:

| Weight set | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| low_only | 6.0 | 6.2 | 3.054e-05 |
| onepointfive_only | 6.0 | 6.2 | 1.045e-03 |
| unweighted | 6.0 | 6.2 | 5.377e-04 |
| carry_low_25 | 6.0 | 6.2 | 8.419e-04 |
| carry_low_50 | 6.0 | 6.2 | 7.067e-04 |

The noisy objective values themselves are much larger because the true model
cannot fit the added noise:

```text
true r=6.0:
  1.0 GHz J: 1.697e-02
  1.5 GHz J: 2.003e-01

next r=6.2:
  1.0 GHz J: 1.700e-02
  1.5 GHz J: 2.013e-01
```

The radius margin is still controlled mostly by 1.5 GHz.

## Interpretation After 10% Noise

The 10% noise matrix reinforces, rather than overturning, the exact-data
finding:

```text
1.0 GHz-only:
  keeps the right radius in this controlled grid, but with very weak margin

1.5 GHz-only:
  gives the largest radius margin

unweighted 1.0+1.5 GHz:
  dilutes radius margin by about half

carry_low_25:
  preserves most of the 1.5 GHz margin while keeping some low-frequency carry
```

The dynamic Day 4 conclusion is therefore:

```text
Use low-frequency content for basin finding.
Do not average low and high frequencies equally for radius selection.
Use 1.5 GHz-only or carry_low_25 for final radius evidence.
```

Because the 10% case did not fail, the 5% case is now a completeness run, not
a threshold search.

### 049_frequency_weight_radius_margin_noise05_seed13

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_frequency_weight_matrix.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequencies-ghz 1.0,1.5 \
  --weight-sets 'low_only:1,0|onepointfive_only:0,1|unweighted:1,1|carry_low_25:0.25,1|carry_low_50:0.5,1' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 13 \
  --run-name frequency_weight_radius_margin_noise05_seed13
```

Output:

```text
outputs/experiments/049_frequency_weight_radius_margin_noise05_seed13
```

Plot validation:

```text
frequency_weight_radius_profiles.png: 1481x886 px, dynamic range 255
```

5% noise margin table:

| Weight set | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| low_only | 6.0 | 6.2 | 3.320e-05 |
| onepointfive_only | 6.0 | 6.2 | 1.102e-03 |
| unweighted | 6.0 | 6.2 | 5.677e-04 |
| carry_low_25 | 6.0 | 6.2 | 8.883e-04 |
| carry_low_50 | 6.0 | 6.2 | 7.458e-04 |

## Day 4 Conclusion

Across exact, 5% noise, and 10% noise:

| Case | low_only | onepointfive_only | unweighted | carry_low_25 | carry_low_50 |
| --- | ---: | ---: | ---: | ---: | ---: |
| exact | 3.560e-05 | 1.037e-03 | 5.364e-04 | 8.368e-04 | 7.033e-04 |
| 5% noise | 3.320e-05 | 1.102e-03 | 5.677e-04 | 8.883e-04 | 7.458e-04 |
| 10% noise | 3.054e-05 | 1.045e-03 | 5.377e-04 | 8.419e-04 | 7.067e-04 |

The result is stable:

```text
1.0 GHz-only is too weak for radius selection.
1.5 GHz-only is the strongest radius discriminator in this setup.
Equal 1.0+1.5 GHz averaging consistently cuts radius margin by about half.
carry_low_25 consistently restores most of the 1.5 GHz radius margin.
```

Recommendation:

```text
Use low-frequency stages for x-z basin capture.
Use 1.5 GHz-only or carry_low_25 for final radius/profile evidence.
Do not use unweighted cumulative averaging as the final radius objective.
```

The next branch should be W2 landscape testing. Trace-level W2 convexity was
promising in Experiment 24, but the current radius issue is already
phase-aligned enough that only a local rebar landscape can justify W2
integration.
