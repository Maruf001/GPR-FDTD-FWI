# Interim Research Summary: Single-Rebar FWI Radius And Source Robustness

## Plain Result

The best current direction is not a broader global optimizer and not W2/IFWI.

The strongest evidence says:

```text
Use LS / weighted LS for final radius evidence.
Use local radius profiling/grid polish for size selection.
Add source-wavelet profiling before trusting radius on mismatched or field data.
```

## What Improved

### Plotting

The plotting templates were repaired and validated:

```text
B-scans no longer render as blank one-column plots.
convergence plots no longer contain oversized annotations.
model-comparison colorbars no longer overlap the right panel.
all new plot writers validate saved image dynamic range.
```

Tracker:

```text
docs/experiments/19_plotting_and_baseline_infrastructure.md
```

### Frequency Weighting

Lower-frequency data are useful for basin finding, but weak for radius
selection.

Radius margin against r=6.2:

| Case | 1.0 GHz only | 1.5 GHz only | unweighted 1.0+1.5 | 25% low carry |
| --- | ---: | ---: | ---: | ---: |
| exact | 3.560e-05 | 1.037e-03 | 5.364e-04 | 8.368e-04 |
| 5% noise | 3.320e-05 | 1.102e-03 | 5.677e-04 | 8.883e-04 |
| 10% noise | 3.054e-05 | 1.045e-03 | 5.377e-04 | 8.419e-04 |

Recommendation:

```text
Do not use equal low/high frequency averaging as the final radius objective.
Use 1.5 GHz-only or carry_low_25 for final radius evidence.
```

Tracker:

```text
docs/experiments/23_frequency_weighting_radius_margins.md
```

### W2 / Optimal Transport

Softplus/Sinkhorn W2 behaved well on shifted Ricker traces, but it failed the
actual rebar radius landscape gate.

Key comparison:

```text
LS radius margin: 1.037e-03
W2 radius margin: ~1.0e-07
```

Decision:

```text
Do not use W2 as the final radius-selection objective for this single-rebar
pipeline.
```

Trackers:

```text
docs/experiments/24_w2_distance_convexity.md
docs/experiments/25_w2_rebar_landscape.md
```

### Source Wavelet Mismatch

This is the biggest newly exposed risk.

Raw fixed-source LS can fail badly:

| Mismatch | Raw best radius |
| --- | ---: |
| center frequency -10% | 5.4 mm |
| center frequency +10% | 7.8 mm |
| source delay +50 ps | 5.4 mm |
| source delay -50 ps | 7.8 mm |
| amplitude +10% | 7.0 mm |

Low-dimensional source profiling fixed the tested cases:

```text
amplitude fit fixes amplitude mismatch.
amplitude + time-shift fit fixes delay mismatch.
amplitude + time-shift + frequency-scale fit fixes all tested cases.
```

Final profiled source result:

| Case | Best radius |
| --- | ---: |
| nominal | 6.0 mm |
| fc_low10 | 6.0 mm |
| fc_high10 | 6.0 mm |
| delay_plus50ps | 6.0 mm |
| delay_minus50ps | 6.0 mm |
| amp_low10 | 6.0 mm |
| amp_high10 | 6.0 mm |

Recommendation:

```text
Source amplitude, time-zero, and center-frequency/bandwidth profiling must be
part of the pre-field-data radius workflow.
```

Tracker:

```text
docs/experiments/26_wavelet_mismatch_and_update.md
```

### Material Ambiguity

At the correct x/z location, radius was not explained away by concrete epsr or
effective rebar conductivity in the tested ranges.

Result:

```text
best: r=6.0 mm, concrete epsr=6.0, rebar sigma=1e7 S/m
next distinct radius: r=6.2 mm
margin: 1.037e-03
```

Recommendation:

```text
Do not add material parameters to the normal single-rebar radius optimizer yet.
```

Tracker:

```text
docs/experiments/27_geometry_material_tradeoff.md
```

## Current Recommended Pipeline

For controlled single-rebar synthetic data:

```text
1. Get x/z into the correct basin using existing staged/PEBDD or Powell path.
2. Evaluate final radius with 1.5 GHz-only or carry_low_25 LS.
3. Use local radius profiling/grid polish, not continuous Powell radius alone.
4. If source mismatch is possible, profile source amplitude, time shift, and
   center-frequency scale during the final local radius stage.
5. Report top-k radius candidates and distinct-radius margin.
```

## What Not To Do Next

Do not spend the next iteration on:

```text
another broad global search,
W2-Powell integration,
free rebar conductivity optimization,
full WRI,
or full neural IFWI.
```

Those branches were either tested and rejected for this stage or documented as
too large for the current single-rebar problem.

## Best Next Experiments

1. Implement a production-style source-profiled radius-polish runner.
2. Replicate it across noise seeds and source mismatch seeds.
3. Stress it with offset x/z/r seeds.
4. Extend the same confidence reporting to two or three rebars.
