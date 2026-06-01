# Previous Experiment Wavefield Animations

## Goal

Add representative wavefield GIFs to selected earlier experiment folders,
especially the single-rebar source-profile, mismatch, material, and local
geometry studies around experiments 052-062.

This is not a new scientific experiment branch. It is visualization support
for existing results.

## Animation Policy

Use `run_wavefield_animation.py` and save into the original experiment folder:

```text
outputs/experiments/<NNN_name>/figures/*.gif
outputs/experiments/<NNN_name>/data/*_wavefield_animation_summary.json
```

For single-rebar studies:

```text
x = 250 mm
z = 90 mm
radius = 6 mm
source_x = 240 mm
```

`source_x=240 mm` places the source/receiver midpoint over the 250 mm rebar
because the TX/RX offset is 20 mm.

These animations must be scientifically tied to the specific experiment:

- Use the true geometry when showing the observed/true forward wavefield.
- Use the selected or competing candidate geometry when showing a candidate
  comparison.
- Use the same source wavelet perturbation that appears in the experiment case
  label. For example, `fc_high10` means frequency scale 1.1, not a combined
  frequency/time/amplitude mismatch.
- Keep source/receiver positions explicit and physically meaningful for the
  target being visualized.
- Do not present an adjoint or time-reversed residual field as a physical
  received wave. Label it as residual back-propagation or adjoint wavefield.

This policy applies to current/future experiments too, including the Stage 9
objective-matrix animations already generated. Any new or regenerated GIFs
should include transmitter/receiver markers.

For mismatch/source-profile experiments, add both nominal and mismatch wavelet
animations where that distinction is central to the experiment. Do not invent
combined mismatch settings for experiments that only tested separate
perturbations.

## Initial Target Folders

| Experiment | Type | Planned animations |
| --- | --- | --- |
| 062 | single-rebar geometry window, 10% noise | nominal + source mismatch |
| 061 | single-rebar geometry window, exact/mismatch | nominal + source mismatch |
| 060 | single-rebar source-profile seed matrix | nominal + representative source mismatch |
| 059 | single-rebar source-profile compact | nominal + representative source mismatch |
| 058 | source-profiled polish combined mismatch | nominal + source mismatch |
| 057 | source-profiled polish nominal smoke | nominal |
| 056 | material/radius tradeoff | nominal |
| 055 | wavelet mismatch amplitude/time/frequency fit | nominal + `fc_high10`, `delay_minus50ps`, `amp_high10` |
| 054 | wavelet mismatch amplitude/time fit | nominal + `delay_minus50ps`, `amp_high10` |
| 053 | wavelet mismatch amplitude fit | nominal + `amp_high10` |
| 052 | wavelet mismatch exact | nominal + `fc_high10`, `delay_minus50ps`, `amp_high10` |

## Runtime Note

Do not launch these while a production GPU optimization run is saturating the
device. Generate them after the active run finishes or during an idle GPU
window.

## Animation Types

### Forward True-Model Wavefield

Purpose:

```text
show the incident wave, concrete/interface interaction, rebar scattering, and
received reflection for the true experiment geometry and source case
```

Use for:

```text
all selected previous experiments
```

### Forward Candidate-Model Wavefield

Purpose:

```text
show how a recovered, high-radius, or competing candidate changes the scattering
pattern relative to truth
```

Use for:

```text
experiments with meaningful competing radius/depth candidates
```

### Side-By-Side Truth Vs Candidate

Purpose:

```text
compare the true and selected/competing wavefields under the same source,
receiver, color scale, and time sampling
```

Use for:

```text
high-radius ambiguity cases and representative radius-bias cases
```

Implementation:

```text
run_wavefield_comparison_animation.py
```

The comparison animation uses the same source, receiver, frame times, and
color scale for true and candidate fields, plus a third `candidate - true`
panel. It is the preferred visualization for radius/depth ambiguity cases.

### Residual Back-Propagation / Adjoint Field

Purpose:

```text
show where a candidate mismatch sends sensitivity during FWI by injecting the
time-reversed residual at the receiver
```

Use for:

```text
selected FWI diagnostic cases only, because it is a sensitivity visualization,
not a physical forward receive animation
```

Implementation:

```text
run_residual_backprop_animation.py
```

The runner simulates the observed true trace and candidate trace, injects the
time-reversed `candidate - observed` residual at the receiver, and saves the
result as a residual/adjoint-style animation. Use it only where the residual is
meaningful and label it clearly.

## Current Status

- [x] Identified target folders and summary files.
- [x] Verified single-rebar geometry/source placement convention.
- [x] Added Tx/Rx markers to new wavefield animations.
- [x] Added side-by-side truth-vs-candidate comparison animation runner.
- [x] Added residual back-propagation animation runner.
- [x] Generate GIFs for experiments 062-052.
- [x] Validate all generated GIFs.
- [x] Update this tracker with paths and metrics.

## 062: Source-Profiled Geometry Window Noise10

Output folder:

```text
outputs/experiments/062_source_profiled_geometry_window_noise10
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_noise10_seed13_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.62 |
| `figures/true_source_mismatch_noise10_seed13_wavefield.gif` | true-model source-mismatch forward wavefield | 48 | `1000x600` | 255 | 32.97 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.48 |
| `figures/high_radius_candidate_muted_residual_backprop.gif` | muted residual back-propagation for high-radius candidate | 48 | `1000x600` | 255 | 32.31 |

Interpretation:

These are not decorative wave movies. They map directly to the experiment's
source-profiled geometry-window question: nominal/mismatch true scattering,
the high-radius competing branch, and where its muted residual back-propagates
when injected at the receiver.

## 061: Source-Profiled Geometry Window Exact/Mismatch

Output folder:

```text
outputs/experiments/061_source_profiled_geometry_window_exact_mismatch
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.61 |
| `figures/true_source_mismatch_wavefield.gif` | true-model source-mismatch forward wavefield | 48 | `1000x600` | 255 | 32.97 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.48 |
| `figures/high_radius_candidate_muted_residual_backprop.gif` | muted residual back-propagation for high-radius candidate | 48 | `1000x600` | 255 | 32.31 |

Interpretation:

Experiment 061 is the exact/source-mismatch version of the single-rebar
geometry-window ambiguity test. These GIFs mirror the same physical questions
as experiment 062 without noise.

## 060: Source-Profiled Replication Seed Matrix

Output folder:

```text
outputs/experiments/060_source_profiled_replication_seed_matrix
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.63 |
| `figures/true_source_mismatch_noise10_seed13_wavefield.gif` | representative source-mismatch/noise forward wavefield | 48 | `1000x600` | 255 | 33.71 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.50 |

Interpretation:

Experiment 060 contains many noise/source seeds. The GIFs are representative,
not exhaustive: nominal truth, the seed13 source-mismatch/noise source case,
and a geometry comparison for the high-radius branch.

## 059: Source-Profiled Replication Compact

Output folder:

```text
outputs/experiments/059_source_profiled_replication_compact
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.62 |
| `figures/true_source_mismatch_noise05_seed13_wavefield.gif` | representative source-mismatch/noise forward wavefield | 48 | `1000x600` | 255 | 33.71 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.49 |

## 058: Source-Profiled Polish Combined Mismatch

Output folder:

```text
outputs/experiments/058_source_profiled_polish_combined_mismatch
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.63 |
| `figures/true_combined_source_mismatch_wavefield.gif` | true-model combined source-mismatch forward wavefield | 48 | `1000x600` | 255 | 33.34 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.49 |

## 057: Source-Profiled Polish Nominal Smoke

Output folder:

```text
outputs/experiments/057_source_profiled_polish_nominal_smoke
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.60 |
| `figures/true_vs_high_radius_candidate_comparison.gif` | true vs `x=250,z=91,r=6.8` candidate comparison | 48 | `1550x560` | 255 | 38.47 |

## 056: Material Tradeoff Fixed X/Z

Output folder:

```text
outputs/experiments/056_material_tradeoff_fixed_xz_exact
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal material forward wavefield | 48 | `1000x600` | 255 | 33.64 |
| `figures/candidate_rebar_sigma1e5_wavefield.gif` | candidate forward wavefield with true radius and low steel conductivity `1e5 S/m` | 48 | `1000x600` | 255 | 33.86 |

Note:

This experiment varies material/radius tradeoffs. I added single-rebar material
overrides to the forward animation runner before generating the candidate GIF,
so the low-conductivity animation uses the actual `r=6.0 mm, sigma=1e5 S/m`
candidate instead of a geometry-only substitute. The material matrix showed the
radius remained robust at 6.0 mm while steel conductivity from `1e7` down to
`1e5 S/m` was nearly indistinguishable in the objective.

## 055: Wavelet Mismatch Radius, Amplitude/Time/Frequency Fit

Output folder:

```text
outputs/experiments/055_wavelet_mismatch_radius_amp_time_freqfit
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.61 |
| `figures/true_fc_high10_wavefield.gif` | true-model `fc_high10` forward wavefield | 48 | `1000x600` | 255 | 32.68 |
| `figures/true_delay_minus50ps_wavefield.gif` | true-model `delay_minus50ps` forward wavefield | 48 | `1000x600` | 255 | 33.83 |
| `figures/true_amp_high10_wavefield.gif` | true-model `amp_high10` forward wavefield | 48 | `1000x600` | 255 | 33.67 |

Interpretation:

Experiment 055 is the source-profiled recovery case. The animations show the
observed wavefields for the nominal and tested perturbation cases that the
fit was allowed to absorb. The summary confirms that amplitude, time, and
frequency profiling returns the true 6.0 mm radius for these cases, so no
candidate/residual animation is needed here.

## 054: Wavelet Mismatch Radius, Amplitude/Time Fit

Output folder:

```text
outputs/experiments/054_wavelet_mismatch_radius_amp_timefit
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.62 |
| `figures/true_delay_minus50ps_wavefield.gif` | true-model `delay_minus50ps` forward wavefield | 48 | `1000x600` | 255 | 33.83 |
| `figures/true_amp_high10_wavefield.gif` | true-model `amp_high10` forward wavefield | 48 | `1000x600` | 255 | 33.68 |

Interpretation:

Experiment 054 tested whether amplitude and time-shift fitting can remove the
radius bias caused by those nuisance parameters. The generated GIFs therefore
cover the nominal, time-shift, and amplitude cases without adding unrelated
frequency-mismatch animations to this folder.

## 053: Wavelet Mismatch Radius, Amplitude Fit

Output folder:

```text
outputs/experiments/053_wavelet_mismatch_radius_amplitude_fit
```

Generated animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.61 |
| `figures/true_amp_high10_wavefield.gif` | true-model `amp_high10` forward wavefield | 48 | `1000x600` | 255 | 33.68 |

Interpretation:

Experiment 053 isolates amplitude fitting. The forward GIFs show the true
nominal and high-amplitude observations; the source-profiled objective recovers
the true 6.0 mm radius for `amp_high10`.

## 052: Wavelet Mismatch Radius, Exact Model

Output folder:

```text
outputs/experiments/052_wavelet_mismatch_radius_exact
```

Generated forward animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/true_nominal_wavefield.gif` | true-model nominal forward wavefield | 48 | `1000x600` | 255 | 33.61 |
| `figures/true_fc_high10_wavefield.gif` | true-model `fc_high10` forward wavefield | 48 | `1000x600` | 255 | 32.67 |
| `figures/true_delay_minus50ps_wavefield.gif` | true-model `delay_minus50ps` forward wavefield | 48 | `1000x600` | 255 | 33.82 |
| `figures/true_amp_high10_wavefield.gif` | true-model `amp_high10` forward wavefield | 48 | `1000x600` | 255 | 33.68 |

Generated source-aware candidate comparisons:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/fc_high10_truth_vs_nominal_r7p8_candidate_comparison.gif` | `fc_high10` observed truth vs nominal-source `r=7.8 mm` candidate | 48 | `1550x560` | 255 | 38.92 |
| `figures/delay_minus50ps_truth_vs_nominal_r7p8_candidate_comparison.gif` | `delay_minus50ps` observed truth vs nominal-source `r=7.8 mm` candidate | 48 | `1550x560` | 255 | 39.70 |
| `figures/amp_high10_truth_vs_nominal_r7p0_z91_candidate_comparison.gif` | `amp_high10` observed truth vs nominal-source `z=91 mm, r=7.0 mm` candidate | 48 | `1550x560` | 255 | 39.70 |

Generated residual back-propagation animations:

| Animation | Scientific role | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/fc_high10_nominal_r7p8_muted_residual_backprop.gif` | muted residual back-propagation for `fc_high10` truth minus nominal high-radius candidate | 48 | `1000x600` | 255 | 32.39 |
| `figures/delay_minus50ps_nominal_r7p8_muted_residual_backprop.gif` | muted residual back-propagation for `delay_minus50ps` truth minus nominal high-radius candidate | 48 | `1000x600` | 255 | 32.76 |
| `figures/amp_high10_nominal_r7p0_z91_muted_residual_backprop.gif` | muted residual back-propagation for `amp_high10` truth minus nominal `z=91 mm, r=7.0 mm` candidate | 48 | `1000x600` | 255 | 33.59 |

Interpretation:

Experiment 052 is the most useful previous-folder diagnostic because it shows
what goes wrong without source profiling. The exact nominal case recovers the
true 6.0 mm radius, but unmodelled source perturbations push the best nominal
candidate to high-radius branches: `fc_high10` and `delay_minus50ps` choose
`r=7.8 mm`, while `amp_high10` chooses `z=91 mm, r=7.0 mm`. The comparison
GIFs are source-aware: the true panel uses the perturbed observed wavelet, and
the candidate panel uses the nominal modeled wavelet that caused the original
misfit. The residual GIFs are labelled residual back-propagation, not physical
receive waves.

## Implementation Update

I extended `run_wavefield_comparison_animation.py` so true and candidate
panels can use separate source frequency scale, time shift, and amplitude. The
old common-source options still work, but source-mismatch experiments can now
be visualized without pretending truth and candidate used the same wavelet.
I also extended `run_wavefield_animation.py` with guarded single-rebar material
overrides for material-tradeoff animations.

Validation:

```text
tests/test_wavefield_animation.py: 9 passed
full test suite: 127 passed in 23.57 s
git diff --check: passed
```
