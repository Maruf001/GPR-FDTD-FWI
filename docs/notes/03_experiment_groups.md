# Experiment Groups: Figures and Numbers per Slide

For each experiment family I list:
- the experiments that belong to the group,
- the *single* figure I would put on the deck slide,
- alternates if the primary doesn't fit,
- the key numbers/text the slide should carry.

All paths are repo-relative.

---

## A. Plumbing slide (optional / single line in another slide)

| Experiment | Tracker | Figure |
| --- | --- | --- |
| 042 | `19_plotting_and_baseline_infrastructure.md` | n/a — infrastructure |
| baseline matrix | `20_baseline_result_matrix.md` | use the CSV inline as a small table; no figure |

Recommendation: do not give this its own slide. Mention once as a footnote
that all later runs were measured with a fixed plotting template and a
machine-readable baseline matrix.

---

## B. Trace-shift diagnostics (OT paper hypothesis)

Experiments: 024, 025, 026, 027.

**Primary figure for the slide:** there isn't a single chart — the result is
a table of NRCCC values. Use a small inline table on the slide:

```text
candidate              J            NRCCC   median RCCC   radius
polished true          0            1.000   0.000         6.000 mm
Powell high-radius     2.08e-3      1.000   0.003         6.955 mm
023 top-1 (noise 10%)  1.99e-1      1.000   0.000         6.000 mm
023 top-2              1.99e-1      1.000   0.000         6.000 mm
023 high-radius        2.01e-1      1.000   0.003         6.991 mm
```

**Headline.** NRCCC = 1.0 for every candidate ⇒ the half-period switching
criterion is saturated ⇒ this is not a cycle-skipping problem.

Slide call: "OT branch ruled out for this problem (kept as diagnostic for
field data)."

---

## C. PEBDD bandwidth schedule and spectrum design (PEBDD paper hypothesis)

Experiments: 028–037 (first-pass), 043–045 (spectrum-driven).

**Primary figure 1 — why first-pass low band missed the issue.** Use the
residual spectra from spectrum design:

```text
outputs/experiments/043_pebd_spectrum_design_exact/figures/residual_spectra.png
outputs/experiments/043_pebd_spectrum_design_exact/figures/signal_spectra.png
outputs/experiments/043_pebd_spectrum_design_exact/figures/source_spectrum.png
```

*Caveat:* these plots use an x-axis up to ~250 GHz (the FDTD Nyquist) but
the action is at 0–3 GHz. They will read better if cropped for the slide.
Either re-plot from the saved npz/CSV data, or apply a matplotlib re-render
step in the slide generator. Either is acceptable.

Headline numbers from the summary text:

```text
near-radius residual energy by band:
  0.20–0.80 GHz:  2.1%
  0.35–1.10 GHz:  5.5%
  0.35–1.50 GHz: 22.5%
  0.35–2.00 GHz: 60.4%
  0.35–2.50 GHz: 89.7%
```

**Primary figure 2 — the faithful schedule's recovered model.** Use the
final-polish model comparison from run 045:

```text
outputs/experiments/045_pebd_spectrum_bands_exact/final_fullband_coarse_polish/figures/single_rebar_model_comparison.png
```

Headline stage numbers (already in `22_faithful_pebdd_schedule.md`):

```text
stage01 0.35–1.10:  r=6.864 mm
stage02 0.35–1.50:  r=6.865 mm
stage03 0.35–2.00:  r=6.896 mm
stage04 0.35–2.50:  r=6.930 mm
final polish:       r=6.000 mm, model NRMS=0
```

Slide call: "Bandwidth scheduling is a seed builder; the polish is still the
radius selector."

---

## D. Frequency weighting (WRI cumulative-frequency idea, our adaptation)

Experiments: 038, 039, 040, 041, 046, 047, 049.

**Primary figure.** The exact-data radius-margin curves under five weight
schemes:

```text
outputs/experiments/046_frequency_weight_radius_margin_exact/figures/frequency_weight_radius_profiles.png
```

This single figure carries the whole story: `low_only` is nearly flat,
`onepointfive_only` has the deepest valley at r=6.0 mm,
`unweighted` cuts the margin roughly in half, and `carry_low_25` is the
best compromise.

If a noise version is helpful as a second figure (e.g. to show stability),
use:

```text
outputs/experiments/047_frequency_weight_radius_margin_noise10_seed13/figures/frequency_weight_radius_profiles.png
```

Headline margin numbers (`r=6.0` vs `r=6.2`):

```text
weight set         exact         5% noise       10% noise
low_only           3.56e-5       3.32e-5        3.05e-5
onepointfive_only  1.04e-3       1.10e-3        1.04e-3
unweighted         5.36e-4       5.68e-4        5.38e-4
carry_low_25       8.37e-4       8.88e-4        8.42e-4
carry_low_50       7.03e-4       7.46e-4        7.07e-4
```

Slide call: "Unweighted multi-frequency averaging dilutes radius evidence;
use 1.5 GHz only or carry_low_25."

---

## E. Trace W2 convexity (W2 paper gate 1)

Experiment: 048.

**Primary figure.**

```text
outputs/experiments/048_trace_wasserstein_convexity_smoke/figures/trace_w2_convexity.png
```

Two panels side by side: L2 vs Softplus/Sinkhorn W2 over -28..28 sample
shifts. L2 has the classic Ricker-shift cancellation (24 monotonicity
violations); W2 is smooth and monotonic.

Slide call: "W2 convexity claim reproduced on shifted Ricker traces."

---

## F. W2 rebar landscape (W2 paper gate 2 — the reject result)

Experiments: 050, 051.

**Primary figure.**

```text
outputs/experiments/050_w2_landscape_exact_beta8_ds16/figures/w2_radius_profiles.png
```

Two side-by-side panels: LS shows the familiar deep V at r=6.0 mm; W2 is
nearly flat across the radius axis (note its y-axis is in units of 1e-5).

Headline margin numbers:

```text
LS margin (r=6.0 vs 6.2):   1.037e-3
W2 margin (r=6.0 vs 6.2):   1.060e-7  (downsample 16)
W2 margin                   1.033e-7  (downsample 8)
```

Slide call: "Softplus normalization removes the amplitude information that
radius depends on. Reject W2 as the final radius objective for this problem."

---

## G. Material tradeoff (small slide)

Experiment: 056.

**Primary figure.**

```text
outputs/experiments/056_material_tradeoff_fixed_xz_exact/figures/material_profiled_radius.png
```

A single curve: best objective over the material grid as a function of
radius, with a clean minimum at r=6.0 mm.

Headline numbers (top three):

```text
rank  r [mm]  εr   σ [S/m]   J
1     6.0     6.0  1e7       0
2     6.0     6.0  1e6       3.18e-10
3     6.0     6.0  1e5       3.85e-8
4     6.2     6.0  any       1.04e-3
```

Slide call: "At the correct x/z, material parameters do not explain radius
bias. εr is well-identified; rebar σ saturates."

---

## H. Wavelet mismatch — the key new finding

Experiments: 052, 053, 054, 055.

**Primary figure 1 — raw mismatch.**

```text
outputs/experiments/052_wavelet_mismatch_radius_exact/figures/wavelet_mismatch_radius_profiles.png
```

Seven coloured curves, only `nominal` and `amp_*` near zero — the rest are
pushed far away from r=6.0 mm.

**Primary figure 2 — with full source profile.**

```text
outputs/experiments/055_wavelet_mismatch_radius_amp_time_freqfit/figures/wavelet_mismatch_radius_profiles.png
```

All seven curves collapse onto the same V at r=6.0 mm.

**Headline table (best radius per case):**

```text
case           raw    amp-fit   amp+time   amp+time+freq
nominal        6.0    6.0       6.0        6.0
fc_low10       5.4    5.4       6.2        6.0
fc_high10      7.8    7.8       7.4        6.0
delay_+50 ps   5.4    5.4       6.0        6.0
delay_-50 ps   7.8    7.8       6.0        6.0
amp_low10      6.0    6.0       6.0        6.0
amp_high10    7.0    6.0       6.0        6.0
```

Slide call: "Source-wavelet mismatch can drive radius to the grid bound.
A small structured source profile (amplitude + time-shift + center-frequency
scale) recovers radius in every tested case."

This is the single most important new contribution of this arc. Consider
*two* slides: one for the failure (raw 052), one for the fix (055), each
with one of the figures above.

---

## I. Source-profiled radius polish (the synthesis)

Experiments: 057 (nominal), 058 (combined mismatch).

**Primary figure 1 — nominal.**

```text
outputs/experiments/057_source_profiled_polish_nominal_smoke/figures/source_profiled_radius_profile.png
```

**Primary figure 2 — combined mismatch.**

```text
outputs/experiments/058_source_profiled_polish_combined_mismatch/figures/source_profiled_radius_profile.png
```

**Headline tables.** For 057:

```text
rank  x      z     r    J          fc    shift   amp
1     250.0  90.0  6.0  0.000e0    1.0   0       1.000
2     250.0  90.0  6.2  9.815e-4   1.0   0       0.993
```

For 058 (injected fc=1.1, shift=-50 ps, amp=1.1):

```text
rank  x      z     r    J          fc    shift   amp
1     250.0  90.0  6.0  1.295e-5   1.1   -50     1.100
2     250.0  90.5  6.0  1.295e-5   1.1   -50     1.100
3     250.0  90.0  6.2  1.159e-3   1.1   -50     1.092
```

Slide call: "Production source-profiled polish recovers the true radius and
the injected source parameters together."

---

## J. Deferred branches (one shared slide)

WRI feasibility (`28_wri_feasibility.md`) and IFWI feasibility
(`29_ifwi_feasibility.md`).

No figure. Use a two-column comparison:

```text
WRI                                IFWI
needs new freq-domain operator    flexible neural residual field
complex sparse solves              risk of absorbing radius bias
adjoint redesign                   needs guardrails (held-out sources)
deferred: cost vs current gain     deferred: not the right tool yet
```

Slide call: "Both reserved for later — when single-rebar source handling is
mature and multi-rebar / field cases create a genuine residual the explicit
nuisance parameters cannot explain."

---

## K. Recommended pipeline / what's next

No figure. A clean five-step pipeline (copy from `30_two_week_research_summary.md`):

```text
1. get x/z into basin (existing staged / PEBDD path)
2. final radius from 1.5 GHz-only LS or carry_low_25
3. local radius profiling / grid polish (not Powell-only)
4. profile source amplitude / time / frequency-scale at final radius
5. report top-k candidates and distinct-radius margin
```

Plus a brief "next experiments" pointer: replicate source-profiled polish
across noise/source-mismatch seeds; offset x/z/r seeds; then extend to
two or three rebars.

---

## Total slide budget estimate

- 1 title
- 5 paper slides
- 1 trace-shift / OT-ruling-out slide (group B)
- 2 PEBDD slides (group C: spectrum + result)
- 1 frequency-weighting slide (group D)
- 1 W2 trace convexity slide (group E)
- 1 W2 rebar landscape slide (group F)
- 1 material-tradeoff slide (group G)
- 2 wavelet-mismatch slides (group H: failure + fix)
- 1 source-profiled polish slide (group I)
- 1 deferred-branches slide (group J)
- 1 recommended-pipeline / what's-next slide (group K)

= **~17–18 slides**, with the option to compress wavelet-mismatch into one
slide if a tighter deck is preferred.
