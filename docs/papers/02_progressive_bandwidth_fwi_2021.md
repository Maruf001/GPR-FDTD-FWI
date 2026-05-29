# Progressively Expanded Bandwidth FWI 2021: Working Notes

Source PDF:

```text
paper/FWI_improvement_by_progressively expanded bandwidths of the data.pdf
```

Paper:

```text
Zhou, Klotzsche, Vereecken.
Improving crosshole ground-penetrating radar full-waveform inversion results
by using progressively expanded bandwidths of the data.
Near Surface Geophysics, 2021.
```

## Why This Paper Matters For Our Project

This paper is highly relevant because it addresses a practical FWI failure
mode: the starting model is not close enough, especially in high-contrast media.
Our single-rebar problem has a smaller parameter space, but the same symptom
appears: a waveform-fitting optimizer can settle into a nearby depth/radius
tradeoff that fits the B-scan well.

The paper's main idea is:

```text
Do not invert full-band data immediately.
Filter both observed and modeled data into a low-band problem first, then
progressively expand the bandwidth and use the result as a better starting
model for final full-band FWI.
```

This is more concrete than generic multi-frequency continuation because it
operates on the data bandwidth itself.

## Problem The Paper Solves

Standard GPR FWI needs a starting model that keeps modeled traces within about
half a wavelength or half a period of the measured traces. If this condition is
violated, least-squares waveform fitting can converge to a local minimum.

Ray-based starting models often help in crosshole GPR, but can fail in
high-contrast layered media. The authors therefore propose a way to improve the
starting model and the effective source wavelet before the final full-band
inversion.

## Method: PEBDD

The paper introduces progressively expanded bandwidths of the modeled and
observed data, abbreviated PEBDD.

The key difference from earlier work is that the filters are applied to both:

```text
1. observed data
2. effective source wavelet used to create modeled data
```

Earlier bandwidth-expansion work filtered only the modeled side through the
source wavelet while keeping observed data full-band. The authors found that
filtering both sides made the method more useful for experimental data.

## Algorithm In Plain Terms

1. Estimate or choose an initial effective source wavelet.
2. Build tapered bandpass filters.
3. Keep the low cut fixed.
4. Start with a low high-cut frequency.
5. Run a small number of FWI iterations on filtered observed and modeled data.
6. Expand the high cut by a fixed increment.
7. Repeat until the chosen maximum bandwidth is reached.
8. Use the resulting permittivity model as the new starting model.
9. Update the effective source wavelet using deconvolution.
10. Run full-band FWI.
11. Update the source wavelet again.
12. Run final full-band FWI.

In their examples:

```text
low cut:            about 12 MHz
high cut increment: 4 MHz
iterations/stage:   5
maximum high cut:   near the source-wavelet center frequency
```

The exact frequencies are crosshole-field-data specific, so we should not copy
the values directly. The pattern is what matters.

## Results

Synthetic case I used realistic stochastic aquifer models and ray-based
starting models. The best PEBDD result improved both model error and data
misfit compared with standard FWI.

Key numbers from the paper:

```text
standard FWI:
  permittivity MAE: 2.0056
  conductivity MAE: 2.2043
  data RMS:         6.9945e-7

PEBDD with second updated source wavelet:
  permittivity MAE: 1.7309
  conductivity MAE: 2.0351
  data RMS:         2.8996e-7
```

Synthetic case II deliberately used a starting permittivity model outside the
half-wavelength criterion. Standard FWI was trapped in a poor solution, while
PEBDD produced a much better reconstruction.

Key numbers from the paper:

```text
standard FWI from bad start:
  permittivity MAE: 3.6152
  conductivity MAE: 2.3394
  data RMS:         9.1843e-7

PEBDD with second updated source wavelet:
  permittivity MAE: 2.1027
  conductivity MAE: 2.0498
  data RMS:         3.6288e-7
```

The field-data test also improved data RMS for all four crosshole sections.
Independent cone penetration test comparisons were mostly better for the PEBDD
results, though not uniformly for every section.

## Important Technical Details

### Source Wavelet Matters

The paper repeatedly updates the effective source wavelet. This is essential
for field data, where the emitted wavelet and antenna coupling are not exactly
known.

Our synthetic current setup uses a known Ricker wavelet, so wavelet update is
not immediately required. But the paper warns us not to overfit synthetic
success: field data will need wavelet estimation or wavelet-robust objectives.

### Permittivity Starting Model Is More Useful Than Conductivity Starting Model

The paper tested using both permittivity and conductivity from the
bandwidth-expanded stage as starting models. The better practical result was to
carry forward the permittivity model and keep conductivity simpler.

For our geometric rebar inversion, this translates to:

```text
carry forward geometry/location from low-band stages;
do not add unnecessary material degrees of freedom before geometry is stable.
```

### Diagnostics Matter

The paper uses:

- data RMS curves,
- model MAE for synthetic cases,
- wavelet timing/shape,
- external validation for field data.

For our project, the analog diagnostics are:

- objective history,
- NRMS data,
- model NRMS,
- recovered x/z/r,
- grid-polish top candidates,
- trace-shift or cross-correlation diagnostics.

## Relevance To Our Current Codebase

Current code already generates time-domain FDTD traces and can synthesize data
at different Ricker center frequencies. That is useful, but it is not identical
to PEBDD.

What we currently have:

```text
different source center frequencies
simultaneous multi-frequency objective
stageable initial guesses through CLI arguments
```

What PEBDD adds:

```text
bandpass-filter the same observed and modeled traces
expand the bandwidth of the data progressively
use filtered stages to create a better starting model
run final full-band inversion after the model is close
```

The most faithful first adaptation is not to change the FDTD solver. It is to
add trace filtering inside the objective.

## Practical Ideas To Reuse First

### 1. Add Bandpass Filtering To The Objective

Add optional filtering of both `d_obs` and `d_syn` before residual computation.
This can be done in the time-domain pipeline using FFT-based bandpass filters.

Important rule from the paper:

```text
Filter both observed and modeled data in the same way.
```

### 2. Run A Progressive Bandwidth Schedule

For our 1.5 GHz synthetic Ricker setup, candidate stages could be expressed as
fractions of the useful spectrum, for example:

```text
stage 1: low-pass or bandpass up to 0.8 GHz
stage 2: expand to 1.1 GHz
stage 3: expand to 1.5 GHz
stage 4: full unfiltered trace
```

The exact values should be chosen after inspecting the Ricker spectrum and the
B-scan residual spectrum.

### 3. Compare Against Center-Frequency Continuation

We already have an older multi-scale frequency experiment. PEBDD is different
enough that it deserves a direct comparison:

```text
A. changing Ricker center frequency across stages
B. filtering the same observed/modeled data across stages
```

The second approach may preserve the final target data better.

### 4. Use PEBDD To Improve Radius Basin Before Polish

The current radius polish works, but it is a deterministic correction after
Powell. A better inversion should make the true-radius basin easier to enter
before polish.

Success criteria:

```text
Powell radius before polish moves closer to 6.0 mm,
or grid-polish top-candidate margin for radius=6.0 mm increases,
or the method remains correct under higher observed-noise seeds.
```

## Concrete Next Experiment

Implement:

```text
inversion/trace_filters.py
```

and add CLI/config support for:

```text
--objective-bandpass-ghz LOW,HIGH
```

Then add a small staged runner:

```text
run_single_rebar_bandwidth_schedule.py
```

Initial schedule:

```text
stage 1: 0.2,0.8 GHz
stage 2: 0.2,1.1 GHz
stage 3: 0.2,1.5 GHz
stage 4: full band
final:   coarse grid polish
```

This is intentionally a research branch. Before trusting it, inspect the actual
source spectrum and verify that filtering does not remove the rebar response.

## Reread Update For Current Project State

The paper's PEBDD method is more specific than a generic "try a lower
frequency" idea. The details that matter for the next plan are:

```text
filter observed data and modeled data consistently,
use tapered filters,
expand bandwidth in small stages,
carry forward the model from one stage to the next,
use the low-band result mainly as a better starting model,
then run full-band inversion/polish.
```

The paper also updates the effective source wavelet by deconvolution after the
PEBDD stage. Our synthetic setup uses a known Ricker wavelet, so wavelet update
is not required to validate the geometry idea. But it must be part of the
field-data plan.

### What Our Experiments Already Showed

Our first PEBDD-style adaptation was intentionally minimal:

```text
FFT bandpass inside the objective
same filter on observed and synthetic traces
0.2-0.8 GHz low-band stage
0.2-1.1 GHz expanded stage
full-band Powell / full-band coarse polish
```

Findings:

```text
exact data:
  low-band Powell improved radius seed from about 6.95 mm to about 6.57 mm.

5% and 10% noise:
  low-band Powell stayed near the high-radius basin around 6.9-7.0 mm.

full-band Powell:
  pulled the exact-data low-band seed back to the high-radius basin.

full-band coarse polish:
  remained the reliable final radius selector.
```

This does not invalidate PEBDD. It means our first adaptation was incomplete:

```text
we did not yet tune band edges from spectra,
we did not test multiple band increments,
we did not update or perturb source wavelets,
we did not combine PEBDD with W2/OT objectives,
and we tested only a local single-rebar geometry parameterization.
```

### No-Shortcut PEBDD Work Still Needed

The next PEBDD pass should be more faithful:

1. Plot and save source, observed, residual, and candidate spectra.
2. Select band edges from those spectra, not by guess.
3. Test several high-cut increments and taper widths.
4. Compare low-pass, bandpass, and cumulative high-cut schedules.
5. Run exact, 5% noise, 10% noise, and seed-offset cases.
6. Report top-candidate radius margins, not just recovered radius.
7. Add wavelet perturbation tests to simulate field-data mismatch.

The core question is:

```text
Can a carefully chosen PEBDD schedule move rough seeds into the correct local
window more cheaply or reliably than full-band Powell?
```

It should not be judged by whether low-band Powell alone returns the exact
radius. The paper uses PEBDD to improve the starting model and source wavelet
before final full-band inversion.
