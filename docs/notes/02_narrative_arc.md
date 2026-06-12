# Narrative Arc: Single-Rebar FWI After The Baseline Pipeline

The earlier deck ended with a clean exact-synthetic recovery (`x=250 mm,
z≈90 mm, r=6 mm`, model NRMS = 0) and noise tolerance up to about 10% before
the radius margin became marginal. The story of experiments 024–058 is the
direct continuation of that result: *which assumption, if broken, would
actually move the radius answer?* Each branch below addresses one such
assumption, drawn from one of the five papers.

The branches are ordered the way the deck should tell them, not strictly
chronologically.

---

## 0. Plumbing: trustable plots and a baseline matrix

Before testing anything subtle, the plot infrastructure was rebuilt so the
later evidence couldn't be ambiguous: image-based B-scan rendering, dedicated
colorbar axes, validated dynamic-range checks on every saved figure, and a
machine-readable baseline matrix `outputs/summary_tables/single_rebar_baseline_matrix.csv`
indexing every saved run by recovered geometry, NRMS, and best/next radius
margin. This is mentioned briefly because every later slide depends on it,
but does not need its own slide.

Tracker: `docs/experiments/19_plotting_and_baseline_infrastructure.md`,
`20_baseline_result_matrix.md`.

---

## 1. Is the radius problem a cycle-skipping problem? (OT paper diagnostic)

**Hypothesis from the OT-LS paper.** If the high-radius Powell basin is a
cycle-skipping failure, then the trace-shift criterion (RCCC / NRCCC) should
register it as unsafe for least-squares, and a transport-based objective
would be the right tool.

**What we did.** Implemented `trace_distances.py` with RCCC and NRCCC.
Evaluated the known high-radius Powell candidate and every polish top
candidate (exact, 5%, 10% noise) against the paper's half-period switching
criterion.

**Result (exp 024–026).** Every candidate, including the wrong-radius ones,
has `NRCCC = 1.0`. The problem is not cycle skipping. The radius issue is
amplitude-and-detail, not transport.

**Why it goes in the deck.** This is the slide that rules out the OT branch
for the current problem. It is a *finding* about our data, not a negative
result about OT in general.

Tracker: `docs/experiments/15_trace_shift_diagnostics.md`.

---

## 2. Does progressive bandwidth help? (PEBDD paper)

**Hypothesis.** A staged bandpass objective that starts low and expands the
high cut should reduce the high-radius Powell bias before polish.

**What we did, attempt 1 (exp 028–037).** Built `trace_filters.py` and a
3-stage runner with guessed bands (0.2–0.8, 0.2–1.1, 0.2–1.5, full). On
exact data the low-band stage improved the radius seed from ~6.95 mm to
~6.57 mm, but full-band Powell pulled it back to the high-radius basin. Under
5% and 10% noise, even the low-band stage stayed in the high-radius basin.

**What we did, attempt 2 (exp 043–045).** Built a spectrum-design tool to
choose band edges from real spectra rather than guesses. Finding: the
0.2–0.8 GHz band contains ~2% of the radius-discriminating residual energy.
The radius-sensitive content lives between roughly 1.0 and 2.5 GHz. With
spectrum-driven bands (0.35–1.10 → 0.35–1.50 → 0.35–2.00 → 0.35–2.50 GHz)
the staged Powell still ended near r=6.93 mm; the full-band polish recovered
the exact model with the same margin we already had from the simpler pipeline.

**Bottom line.** PEBDD is a useful *seed builder* — it can move a rough
initial guess into the right x/z window. It is not a radius selector on its
own. The deck slide should make this distinction explicitly.

Trackers: `16_bandwidth_schedule.md`, `17_bandwidth_noise_robustness.md`,
`21_pebdd_spectrum_design.md`, `22_faithful_pebdd_schedule.md`.

---

## 3. Does multi-frequency averaging help? (WRI cumulative-frequency idea)

**Hypothesis.** Adding a second carrier frequency (say 1.0 GHz alongside
1.5 GHz) should help radius via complementary spectral information, as the
WRI paper's cumulative-frequency strategy implies.

**What we did (exp 038–041, 046, 047, 049).** Added per-frequency objective
contributions and a `--frequency-weights` CLI. Then a matrix that scans
radius from 5.4–7.8 mm at four depths, under 5 weight schemes:

```text
low_only:          1.0 GHz only
onepointfive_only: 1.5 GHz only
unweighted:        equal 1.0 + 1.5 GHz
carry_low_25:      25% 1.0 GHz + 1.0 weight on 1.5 GHz
carry_low_50:      50% 1.0 GHz + 1.0 weight on 1.5 GHz
```

**Result (consistent across exact / 5% / 10% noise).** The 1.0 GHz objective
alone has roughly 30× smaller radius margin than 1.5 GHz alone. Equal
averaging cuts radius margin nearly in half. `carry_low_25` keeps most of
the 1.5 GHz margin while still providing some low-frequency contribution
for basin continuity.

**Bottom line.** Multi-frequency stacking is *not neutral*. It dilutes the
useful radius evidence unless the lower band is carried at low weight. For
radius selection: prefer 1.5 GHz only or carry_low_25.

Trackers: `18_cumulative_frequency_diagnostics.md`,
`23_frequency_weighting_radius_margins.md`.

---

## 4. Does optimal-transport replace LS? (W2-GPR paper)

**Hypothesis.** The W2 / Sinkhorn objective with Softplus normalization
should be broader and less local-minimum-prone than LS.

**What we did, gate 1 (exp 048).** Built a standalone Softplus/Sinkhorn W2
module and replicated the convexity test on shifted Ricker traces. L2 had
24 monotonicity violations across the tested shift range; W2 had zero. The
paper's core claim transfers.

**What we did, gate 2 (exp 050, 051).** Ran the same W2 on the actual
single-rebar radius/depth landscape with two Sinkhorn downsamples (16 and 8).

**Result.** On the radius landscape, the LS margin between r=6.0 and r=6.2 is
1.04e-3. The W2 margin is 1.06e-7 — roughly four orders of magnitude smaller.
Softplus mass normalization removes amplitude content that radius depends on.

**Bottom line.** W2 is good at the transport problem it was designed for, but
the rebar radius problem is not a transport problem. Reject W2 as the final
radius objective. Keep it available as a basin-search diagnostic for future
poor-initial-model cases.

Trackers: `24_w2_distance_convexity.md`, `25_w2_rebar_landscape.md`.

---

## 5. Can material ambiguity explain the radius bias?

**Hypothesis.** At the correct x/z, maybe wrong radius can hide behind
different concrete εr or different effective rebar conductivity.

**What we did (exp 056).** A matrix at fixed (x=250, z=90) over
radius 5.4–7.8 mm × concrete εr {5.5, 6.0, 6.5} × rebar σ {1e5, 1e6, 1e7}
S/m.

**Result.** The best candidate is the true geometry with the true εr. εr is
strongly identifiable. Effective rebar σ saturates above ~1e5 S/m and is
indistinguishable across the tested decades. The distinct-radius margin
remains 1.037e-3.

**Bottom line.** Material parameters do not explain the radius bias at the
correct location. Don't add them to the radius optimizer yet.

Tracker: `docs/experiments/27_geometry_material_tradeoff.md`.

---

## 6. Source-wavelet mismatch — the biggest newly exposed risk

**Hypothesis.** Field data don't have a perfectly known source. If the
observed wavelet differs from the modeled wavelet in amplitude, time-zero,
or center frequency, does radius selection survive?

**What we did, raw test (exp 052).** Built a wavelet-mismatch runner. Held
the modeled wavelet at nominal 1.5 GHz Ricker; perturbed only the observed
wavelet across seven cases (`nominal`, `fc_low10`, `fc_high10`,
`delay_±50 ps`, `amp_±10%`). Same radius grid as the frequency-weighting
matrix.

**Raw result.** Modest source mismatch creates **large** radius bias:

```text
nominal:        r=6.0 mm  ✓
fc_low10:       r=5.4 mm  ✗  (pegs lower grid bound)
fc_high10:      r=7.8 mm  ✗  (pegs upper grid bound)
delay_+50 ps:   r=5.4 mm  ✗
delay_-50 ps:   r=7.8 mm  ✗
amp_low10:      r=6.0 mm  ✓  (correct radius, margin changes)
amp_high10:    r=7.0 mm  ✗
```

This is the kind of failure mode that would only show up after moving to
real data, so it is worth its own slide in the deck.

**What we did, incremental source fitting (exp 053, 054, 055).** Added
nuisance source profiling, one piece at a time:

- amplitude scalar (053) → fixes the amplitude cases; doesn't help fc/delay
- amplitude + global time shift (054) → also fixes the delay cases
- amplitude + time shift + center-frequency scale (055) → all seven cases
  recover r=6.0 mm

**Bottom line.** A small, structured source-profile (one amplitude scalar,
one time-shift grid, one frequency-scale grid) recovers radius even when the
modeled source is wrong. This is the most important new addition to the
pipeline.

Tracker: `docs/experiments/26_wavelet_mismatch_and_update.md`.

---

## 7. Why WRI / IFWI were deferred

Documented in `28_wri_feasibility.md` and `29_ifwi_feasibility.md`. Quick
reasons:

- **WRI** needs a frequency-domain Helmholtz/Maxwell operator, complex sparse
  solves, frequency-domain adjoint, and penalty continuation — essentially
  a new solver. The radius problem is already well explained by source
  handling and frequency weighting, so the cost is not justified at this
  stage.
- **IFWI** would let a neural field absorb material/geometry residuals.
  Without strong guardrails this risks hiding radius errors inside a flexible
  background correction. Deferred until single-rebar source handling is
  locked and either multi-rebar or field data exposes a genuine residual
  the explicit nuisance parameters cannot explain.

These deserve at most one shared "deferred branches" slide in the deck.

---

## 8. Synthesis: source-profiled radius polish (exp 057, 058)

Every surviving idea was assembled into one production-style runner:
`run_single_rebar_source_profiled_polish.py`. It evaluates a local
`(x, z, r)` grid and at each candidate profiles:

```text
center-frequency scale  {0.9, 1.0, 1.1}
global time shift       {-80, -50, -25, 0, +25, +50, +80} ps
amplitude scalar        (closed form per residual)
```

It reports top-k candidates and the distinct-radius margin.

Two validation runs:

- **057 nominal.** No injected source mismatch. Confirms the runner
  reproduces the exact-data behavior; best `r = 6.0 mm`, margin `9.815e-4`.
- **058 combined mismatch.** Injected `fc_scale = 1.1`, `time shift = -50 ps`,
  `amp scale = 1.1`. Best `r = 6.0 mm`, margin `1.146e-3`; the profiler
  also recovered the injected source parameters.

**Bottom line.** This converts the wavelet-mismatch finding from a
diagnostic into a reusable runner. It is the natural ending slide of the
deck — the staged source-profiled polish is the recommended pipeline going
forward.

Tracker: `docs/experiments/31_source_profiled_radius_polish.md`.

---

## 9. Headline result and the recommended pipeline

For controlled single-rebar synthetic data the recommendation is:

```text
1. Get x/z into the correct basin using the existing staged / PEBDD path.
2. Evaluate final radius with 1.5 GHz-only or carry_low_25 LS.
3. Use local radius profiling / grid polish, not continuous Powell radius
   alone.
4. If source mismatch is possible, profile source amplitude, time shift,
   and center-frequency scale during the final local radius stage.
5. Report top-k radius candidates and distinct-radius margin.
```

Explicitly **not** the next direction: another broad global search,
W2-Powell integration, free rebar conductivity, full WRI, full neural IFWI.

This is the framing the closing slide should land on.

(Quoted from `30_two_week_research_summary.md`, which is the canonical
source.)
