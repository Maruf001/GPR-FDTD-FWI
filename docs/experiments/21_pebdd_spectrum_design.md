# Experiment 21: Spectrum-Driven PEBDD Setup

## Goal

Choose PEBDD objective bands from actual spectra instead of guessing band edges.

The previous first-pass PEBDD schedule used:

```text
0.2-0.8 GHz
0.2-1.1 GHz
0.2-1.5 GHz
full band
```

This experiment checks whether those bands contain the spectral energy that
actually distinguishes radius candidates.

## Code Changes

Added:

```text
inversion/spectrum_analysis.py
visualization/plot_spectrum.py
run_single_rebar_spectrum_design.py
tests/test_spectrum_analysis.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_spectrum_analysis.py -q
3 passed
```

## Run Log

### 043 - exact-data spectrum design

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_spectrum_design.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name pebd_spectrum_design_exact
```

Output:

```text
outputs/experiments/043_pebd_spectrum_design_exact/
```

Key spectra:

```text
source wavelet 5-95% energy band:
  0.750-2.500 GHz, peak 1.500 GHz

observed muted B-scan 5-95% energy band:
  0.375-2.750 GHz, peak 0.750 GHz

near-radius residual, r=6.2:
  5-95% band 1.000-2.875 GHz, peak 2.000 GHz

high-radius residual, r≈6.95:
  5-95% band 1.000-2.875 GHz, peak 1.750 GHz
```

Residual energy captured by candidate bands:

```text
near-radius residual, r=6.2:
  0.20-0.80 GHz: 2.1%
  0.35-1.10 GHz: 5.5%
  0.35-1.50 GHz: 22.5%
  0.35-2.00 GHz: 60.4%
  0.35-2.50 GHz: 89.7%
  0.75-2.50 GHz: 87.6%
  1.00-2.80 GHz: 89.1%

high-radius residual, r≈6.95:
  0.20-0.80 GHz: 3.7%
  0.35-1.10 GHz: 7.8%
  0.35-1.50 GHz: 27.5%
  0.35-2.00 GHz: 61.4%
  0.35-2.50 GHz: 88.3%
  0.75-2.50 GHz: 84.6%
  1.00-2.80 GHz: 86.2%
```

Interpretation:

```text
The old 0.2-0.8 GHz stage contains almost none of the radius-discriminating
residual energy. It can be useful for x-z basin finding, but it should not be
expected to fix radius.

Radius discrimination in this synthetic setup mostly lives above 1.0 GHz and
extends to about 2.5-2.9 GHz.
```

### 044 - 10% noise spectrum design

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_spectrum_design.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --run-name pebd_spectrum_design_noise10_seed13
```

Output:

```text
outputs/experiments/044_pebd_spectrum_design_noise10_seed13/
```

Key result:

```text
The current Gaussian observed-noise model is broadband/white in time samples.
It dominates residual spectra at very high numerical frequencies, far above the
source wavelet band.
```

Interpretation:

```text
The existing controlled-noise tests are useful stress tests, but the noise is
not a realistic band-limited GPR noise model. For PEBDD band design, exact/clean
candidate residual spectra are more informative than white-noise residual
spectra.
```

## Pondered Decision

The next PEBDD schedule should not repeat the old `0.2-0.8 -> 0.2-1.1` design
as if it were a radius-refinement schedule.

Recommended PEBDD bands for the next schedule test:

```text
stage 1, basin/location:
  0.35-1.10 GHz

stage 2, add first radius-sensitive content:
  0.35-1.50 GHz

stage 3, radius-sensitive:
  0.35-2.00 GHz

stage 4, near full useful source band:
  0.35-2.50 GHz

final:
  full-band coarse polish
```

Also recommended:

```text
Add a band-limited noise option before making strong claims about noisy PEBDD
behavior.
```

Next action:

```text
Experiment 22: faithful PEBDD schedule runner using spectrum-derived bands.
```
