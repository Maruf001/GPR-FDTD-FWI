# Experiment 26: Wavelet Mismatch Radius Sensitivity

## Goal

Test whether radius selection is stable when the observed source wavelet differs
from the modeled inversion wavelet.

This follows the PEBDD paper warning that field-data FWI depends strongly on
the effective source wavelet.

Question:

```text
If the observed data use a slightly different Ricker center frequency, time
shift, or amplitude, does the local radius grid still select r=6.0 mm?
```

## Code Changes

Added:

```text
run_single_rebar_wavelet_mismatch.py
tests/test_wavelet_mismatch_runner.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_wavelet_mismatch_runner.py -q
3 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile run_single_rebar_wavelet_mismatch.py
passed
```

## Planned Matrix

Candidate grid:

```text
x:      250.0 mm
z:      90.0, 90.5, 91.0, 91.5 mm
radius: 5.4-7.8 mm in 0.2 mm steps
```

Modeled inversion wavelet:

```text
nominal 1.5 GHz Ricker
```

Observed wavelet cases:

```text
nominal
center frequency -10%
center frequency +10%
time shift +50 ps
time shift -50 ps
amplitude -10%
amplitude +10%
```

The synthetic candidate B-scans use the nominal inversion wavelet. Only the
observed truth B-scan changes by case.

## Run Log

### 052_wavelet_mismatch_radius_exact

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_wavelet_mismatch.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --run-name wavelet_mismatch_radius_exact
```

Output:

```text
outputs/experiments/052_wavelet_mismatch_radius_exact
```

Plot validation:

```text
wavelet_mismatch_radius_profiles.png: 1583x903 px, dynamic range 255
```

Margin table:

| Observed wavelet case | Best r [mm] | Next r [mm] | Margin | Interpretation |
| --- | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 1.037e-03 | correct |
| fc_low10 | 5.4 | 5.6 | 0.000e+00 | biased to lower grid bound |
| fc_high10 | 7.8 | 7.4 | 2.128e-02 | biased to upper grid bound |
| delay_plus50ps | 5.4 | 5.6 | 0.000e+00 | biased to lower grid bound |
| delay_minus50ps | 7.8 | 7.4 | 1.109e-02 | biased to upper grid bound |
| amp_low10 | 6.0 | 5.8 | 2.146e-03 | correct radius, changed margin |
| amp_high10 | 7.0 | 6.8 | 2.624e-04 | biased high |

## Interpretation After Raw Mismatch Matrix

Wavelet mismatch is a first-class risk for radius estimation.

The nominal synthetic case is stable, but modest source mismatch creates
geometry bias:

```text
lower observed center frequency or later observed wavelet:
  radius moves to the lower tested bound

higher observed center frequency or earlier observed wavelet:
  radius moves to the upper tested bound

higher observed amplitude:
  radius shifts high to 7.0 mm
```

This explains why a pipeline that looks strong on perfectly matched synthetic
data can still fail on field data. Radius is trading against source timing,
bandwidth, and amplitude.

## Next Decision

Add a minimal source-update control: fit one scalar amplitude per candidate and
observed case before computing the residual. This will not solve timing or
frequency mismatch, but it should tell us whether amplitude mismatch alone can
be separated from radius.

### 053_wavelet_mismatch_radius_amplitude_fit

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_wavelet_mismatch.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --fit-amplitude \
  --run-name wavelet_mismatch_radius_amplitude_fit
```

Output:

```text
outputs/experiments/053_wavelet_mismatch_radius_amplitude_fit
```

Plot validation:

```text
wavelet_mismatch_radius_profiles.png: 1583x903 px, dynamic range 255
```

Amplitude-fit margin table:

| Observed wavelet case | Best r [mm] | Next r [mm] | Margin | Change from raw |
| --- | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | still correct |
| fc_low10 | 5.4 | 5.6 | 0.000e+00 | still wrong |
| fc_high10 | 7.8 | 7.4 | 2.033e-02 | still wrong |
| delay_plus50ps | 5.4 | 5.6 | 0.000e+00 | still wrong |
| delay_minus50ps | 7.8 | 7.4 | 1.191e-02 | still wrong |
| amp_low10 | 6.0 | 6.2 | 9.815e-04 | fixed |
| amp_high10 | 6.0 | 6.2 | 9.815e-04 | fixed |

## Interpretation After Amplitude Fit

Scalar source-amplitude fitting cleanly separates pure amplitude mismatch from
radius. The +10% amplitude case previously biased the radius to 7.0 mm; after
fitting one scalar, it returns to r=6.0 mm with the same margin as the nominal
case.

This does not solve timing or bandwidth mismatch:

```text
center-frequency mismatch:
  still drives radius to low/high bounds

time-shift mismatch:
  still drives radius to low/high bounds
```

## Next Decision

Add a global source time-shift fit over a small shift grid. If that fixes the
delay cases without damaging the nominal/amplitude cases, source timing should
be included in the pre-field-data inversion plan. Center-frequency mismatch
will still need either PEBDD-style wavelet update or a bandwidth/frequency
parameter fit.

### 054_wavelet_mismatch_radius_amp_timefit

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_wavelet_mismatch.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --fit-amplitude \
  --fit-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --run-name wavelet_mismatch_radius_amp_timefit
```

Output:

```text
outputs/experiments/054_wavelet_mismatch_radius_amp_timefit
```

Plot validation:

```text
wavelet_mismatch_radius_profiles.png: 1583x903 px, dynamic range 255
```

Raw versus amplitude-fit versus amplitude+time-fit:

| Case | Raw best r | Amp-fit best r | Amp+time-fit best r | Amp+time margin |
| --- | ---: | ---: | ---: | ---: |
| nominal | 6.0 | 6.0 | 6.0 | 9.815e-04 |
| fc_low10 | 5.4 | 5.4 | 6.2 | 5.618e-04 |
| fc_high10 | 7.8 | 7.8 | 7.4 | 0.000e+00 |
| delay_plus50ps | 5.4 | 5.4 | 6.0 | 8.796e-04 |
| delay_minus50ps | 7.8 | 7.8 | 6.0 | 9.616e-04 |
| amp_low10 | 6.0 | 6.0 | 6.0 | 9.815e-04 |
| amp_high10 | 7.0 | 6.0 | 6.0 | 9.815e-04 |

## Interpretation After Time-Shift Fit

A small global source time-shift grid fixes the pure delay mismatch cases
without damaging nominal or amplitude-scaled cases.

The remaining failure is center-frequency/bandwidth mismatch:

```text
fc_low10:
  improved from the low radius bound to r=6.2 mm, but still not exact

fc_high10:
  remains badly high, with a flat high-radius top candidate set
```

This is now strong evidence that source handling must include:

```text
amplitude update,
time-zero/source-delay update,
bandwidth or center-frequency update.
```

## Next Decision

Profile over modeled center-frequency scale values 0.9, 1.0, and 1.1 in
addition to amplitude and time shift. This is more expensive because it needs
candidate FDTD simulations for each modeled wavelet scale, but it directly
tests whether the remaining center-frequency failures are recoverable by a
low-dimensional source update.

### 055_wavelet_mismatch_radius_amp_time_freqfit

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_wavelet_mismatch.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --fit-amplitude \
  --fit-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --fit-frequency-scales 0.9,1.0,1.1 \
  --run-name wavelet_mismatch_radius_amp_time_freqfit
```

Output:

```text
outputs/experiments/055_wavelet_mismatch_radius_amp_time_freqfit
```

Plot validation:

```text
wavelet_mismatch_radius_profiles.png: 1583x903 px, dynamic range 255
```

Full source-profile result:

| Case | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| nominal | 6.0 | 6.2 | 9.815e-04 |
| fc_low10 | 6.0 | 6.2 | 4.552e-04 |
| fc_high10 | 6.0 | 6.2 | 1.201e-03 |
| delay_plus50ps | 6.0 | 6.2 | 8.796e-04 |
| delay_minus50ps | 6.0 | 6.2 | 9.616e-04 |
| amp_low10 | 6.0 | 6.2 | 9.815e-04 |
| amp_high10 | 6.0 | 6.2 | 9.815e-04 |

## Day 7 Conclusion

The source-wavelet update branch is critical.

Raw LS radius selection is fragile under source mismatch:

```text
center-frequency mismatch and source delay can push radius to grid bounds
pure amplitude mismatch can bias radius high
```

Low-dimensional source profiling fixes the controlled synthetic mismatch cases:

```text
scalar amplitude fit:
  fixes amplitude mismatch

amplitude + global time-shift fit:
  fixes delay mismatch

amplitude + global time-shift + center-frequency scale fit:
  fixes all tested cases
```

Recommendation:

```text
Do not move toward field data with a fixed source wavelet.
Add source amplitude, time-zero, and center-frequency/bandwidth profiling or
update steps around the final radius-profile stage.
```

This is more important for field robustness than W2 in the current single-rebar
problem.
