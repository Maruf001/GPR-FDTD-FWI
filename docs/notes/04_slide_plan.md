# Slide Plan for the Next Deck

This is a slide-by-slide outline. The user's stated format:

- before each experiment slide, a short framing/description slide;
- the experiment slide itself is mostly just the chosen figure with a small
  caption / margin number;
- no timelines, no hours, no LOC stats.

The framing slide and the figure slide for an experiment can also be merged
into a single slide if a tighter deck is preferred — I will mark which ones
are good candidates.

Output target: `outputs/GPR_FDTD_FWI_SingleRebar_Next.pptx` (suggested name,
final name to be decided).

---

## Title

**Slide 1 — Title.** Recovering rebar radius from GPR B-scans, second arc.
Subtitle: stress-testing the baseline pipeline against five published FWI
strategies. Three highlight chips: *Source profiling*, *Frequency weighting*,
*W2 ruled out*.

---

## Five paper-summary slides

Each slide is short. Title, one-line core idea, what we kept, what we
rejected/deferred. No equations on the slide, but the speaker notes can
hold the formal pieces.

```text
Slide 2: Paper 1 — WRI 2022 (Feng et al., Remote Sensing)
Slide 3: Paper 2 — PEBDD 2021 (Zhou, Klotzsche, Vereecken, NSG)
Slide 4: Paper 3 — OT-LS 2025 (Hunziker, Meles, Linde, JAG)
Slide 5: Paper 4 — Quadratic W2 GPR 2024 (Lu et al., Remote Sensing)
Slide 6: Paper 5 — IFWI 2025 (Sun et al., GJI)
```

Each draws from `docs/notes/01_five_papers.md`. Reuse the "single line for
slides" sentence at the bottom of each, in amber.

---

## Trace-shift / OT diagnostic — rules out the OT branch

**Slide 7 — Framing.** Hypothesis (from OT-LS paper): high-radius Powell is
cycle-skipping; trace-shift criterion would flag it.

**Slide 8 — Result.** The single inline table from notes section B.
*Headline: NRCCC = 1.0 for every candidate, so the radius issue is not
transport.* Can be merged with slide 7 if space matters.

Source experiments: 024, 025, 026 (`docs/experiments/15_trace_shift_diagnostics.md`).

---

## PEBDD bandwidth + spectrum design

**Slide 9 — Framing.** Hypothesis (PEBDD paper): bandwidth scheduling
improves the Powell radius basin. First attempt used guessed bands.

**Slide 10 — Spectrum diagnostic.** Use either the residual_spectra.png or
the signal_spectra.png from `043_pebd_spectrum_design_exact/figures/`,
**re-rendered with x-axis cropped to 0–4 GHz so the relevant content is
readable** (the raw plot extends to ~250 GHz). Headline: 0.2–0.8 GHz contains
only ~2% of radius-discriminating residual energy; useful content is
1.0–2.5 GHz.

**Slide 11 — Faithful schedule result.** Stage table + final model
comparison from
`045_pebd_spectrum_bands_exact/final_fullband_coarse_polish/figures/single_rebar_model_comparison.png`.
Headline: each Powell stage stays in the high-radius basin; the polish is
still the radius selector.

---

## Frequency weighting

**Slide 12 — Framing.** Hypothesis: adding a 1.0 GHz frequency helps radius
via multi-frequency stacking.

**Slide 13 — Result.** Figure
`046_frequency_weight_radius_margin_exact/figures/frequency_weight_radius_profiles.png`.
Margin table beside or below. Headline: unweighted averaging cuts margin in
half; carry_low_25 is the best compromise.

---

## W2 trace convexity (gate 1)

**Slide 14 — Framing.** Hypothesis (W2-GPR paper): Softplus/Sinkhorn W2 has
broader basin and avoids cycle skipping. Test on shifted Ricker traces first.

**Slide 15 — Result.** Figure
`048_trace_wasserstein_convexity_smoke/figures/trace_w2_convexity.png`.
Headline: paper claim reproduced (L2 has 24 monotonicity violations; W2
has zero across tested β).

---

## W2 rebar landscape (gate 2 — the reject)

**Slide 16 — Framing.** Move W2 to the real rebar landscape. Same local
x/z/r grid as the LS landscape.

**Slide 17 — Result.** Figure
`050_w2_landscape_exact_beta8_ds16/figures/w2_radius_profiles.png`.
Note the y-axis scale on the W2 panel (1e-5 units). Headline: LS margin
1.04e-3 vs W2 margin 1.06e-7 → ≈ four orders of magnitude collapse.
Decision: reject W2 as the final radius objective.

---

## Material tradeoff (small slide)

**Slide 18 — Combined framing + result.** Question and figure on one slide.
Figure: `056_material_tradeoff_fixed_xz_exact/figures/material_profiled_radius.png`.
Headline: at the correct x/z, concrete εr is well-identified and effective
σ saturates — material does not explain radius bias.

---

## Wavelet mismatch — the new finding

**Slide 19 — Framing.** Hypothesis: source mismatch (amplitude, time-zero,
center frequency) drives radius bias.

**Slide 20 — Raw mismatch.** Figure
`052_wavelet_mismatch_radius_exact/figures/wavelet_mismatch_radius_profiles.png`.
Headline: pure delay or fc mismatch can peg radius to the grid bound.

**Slide 21 — Source-profile fix.** Figure
`055_wavelet_mismatch_radius_amp_time_freqfit/figures/wavelet_mismatch_radius_profiles.png`.
Headline: amplitude + time-shift + frequency-scale profile recovers r=6.0 mm
in all seven cases. Reference table from notes section H.

(If we need to compress, slides 20 and 21 can become a single
before/after split slide with two thumbnails.)

---

## Synthesis — source-profiled radius polish

**Slide 22 — Framing.** The surviving ideas assembled into one
production-style runner. List: 1 mm grid, LS objective, local x/z/r grid,
source amplitude + time-shift + frequency-scale profile, top-k reporting.

**Slide 23 — Nominal result.** Figure
`057_source_profiled_polish_nominal_smoke/figures/source_profiled_radius_profile.png`
plus the top-2 table.

**Slide 24 — Combined-mismatch result.** Figure
`058_source_profiled_polish_combined_mismatch/figures/source_profiled_radius_profile.png`
plus the top-3 table including recovered source parameters.

---

## Deferred branches

**Slide 25 — Deferred WRI + IFWI.** Two-column slide (text only) summarising
why each is reserved for later.

---

## What's next

**Slide 26 — Recommended pipeline.** Five-step pipeline (1.5 GHz-only / local
polish / source profile / top-k report) plus a short "next experiments"
list (replicate across noise/source seeds; offset x/z/r; multi-rebar).

---

## Notes on figure handling

1. **Spectrum plots (043).** The current x-axis extends to FDTD Nyquist
   (~250 GHz). For the deck, **re-render with the x-axis clipped to roughly
   0–4 GHz**. Either:
   - load `outputs/experiments/043_*/data/*.npz` and re-plot, or
   - re-run the spectrum-design script with an x-limit option (if one
     exists) or post-process the saved CSV. Either is acceptable in the
     slide generator.

2. **Multi-stage runs (045).** Use the final-stage figure for the recovery
   slide; if a per-stage progression visual is useful, render a small
   four-up of stage01..stage04 model comparisons.

3. **Wavelet mismatch (052 vs 055).** Both plots use the same axis style and
   look good side by side; the deck generator should respect that.

4. **All other figures** are slide-ready as-is (W2 convexity, W2 landscape,
   frequency weight, material profile, source-profiled polish).

5. **NRMS / margin numbers.** Pull values from the corresponding
   `data/*_summary.json` and `data/*.csv` rather than hard-coding —
   the slide generator should mirror the v1 generator's approach.

---

## Total

26 slides at the loose pacing; ~18–20 if framing and figure are combined for
the simpler groups. Either is acceptable. Default plan unless told
otherwise: the looser 26-slide version, since the user's stated preference
is "framing slide + figure slide" per experiment.
