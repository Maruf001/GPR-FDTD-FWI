# Experiment 50: Field-Like Source Shape Calibration

## Goal

Stress the accepted source-profiled radius workflow with a source-shape error
that is closer to field or lab behavior than the previous scalar Ricker
perturbations.

The previous source-profile branch handled:

```text
source amplitude scale
source time shift
source center-frequency scale
```

This experiment adds a delayed secondary pulse, or simple source ringdown, to
the observed wavelet. The modeled candidate grid initially remains the old
amplitude/time/frequency profile. This asks whether the current source-profile
model is enough, not whether a richer source model could fix the case.

Paper link:

```text
The PEBDD paper notes that field-data FWI needs effective source-wavelet
handling. Our controlled Ricker profiling is a necessary minimum, but it is not
the same as estimating a shaped source wavelet from field data.
```

## Code Change

Extended `run_single_rebar_source_profiled_polish.py`:

```text
observed_wavelet(..., ringdown_scale, ringdown_delay_ps,
                 ringdown_frequency_scale)
```

The default `ringdown_scale=0.0` preserves the old wavelet exactly.

Extended `run_single_rebar_source_profiled_replication.py` so replication cases
can use either the original five-value format:

```text
label:frequency_scale,time_shift_ps,amplitude_scale,noise_fraction,noise_seed
```

or an eight-value source-shape format:

```text
label:frequency_scale,time_shift_ps,amplitude_scale,noise_fraction,noise_seed,
      ringdown_scale,ringdown_delay_ps,ringdown_frequency_scale
```

Focused validation:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_source_profiled_polish_runner.py \
  tests/test_source_profiled_replication_runner.py \
  tests/test_source_profile.py

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_single_rebar_source_profiled_polish.py \
  run_single_rebar_source_profiled_replication.py
```

Result:

```text
20 passed in 0.33 s
py_compile passed
```

## 421: Ringdown Stress, Existing Source Profile

Output:

```text
outputs/experiments/421_source_shape_ringdown_profiled_replication
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|source_mismatch:1.1,-50.0,1.1,0.0,13|ringdown025:1.0,0.0,1.0,0.0,13,0.25,180.0,0.8|ringdown025_noise05_seed13:1.0,0.0,1.0,0.05,13,0.25,180.0,0.8' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 4 \
  --run-name source_shape_ringdown_profiled_replication
```

Runtime and count:

```text
52 candidates
4 observed cases
841.78 s
```

Result:

| Case | Best r [mm] | Next r [mm] | Margin | Best source profile | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.000 | correct |
| source_mismatch | 6.0 | 6.2 | 1.146e-03 | fc=1.1, shift=-50 ps, amp=1.100 | correct controlled mismatch recovery |
| ringdown025 | 7.8 | 7.4 | 1.237e-03 | fc=1.1, shift=80 ps, amp=0.767 | wrong high-radius branch |
| ringdown025_noise05_seed13 | 7.8 | 7.4 | 1.309e-03 | fc=1.1, shift=80 ps, amp=0.767 | wrong high-radius branch |

Plot validation:

```text
source_profiled_replication_radius_profiles.png:
1651x937 px, dynamic range 255, grayscale std 30.9025
```

Figure notes:

```text
outputs/experiments/421_source_shape_ringdown_profiled_replication/figures/FIGURE_NOTES.md
```

## Interpretation

The existing source-profiled radius stage is robust to the controlled
frequency/time/amplitude mismatch, but not to delayed source-shape error.

The failure is not just weak confidence. The ringdown cases choose the upper
tested radius bound, 7.8 mm, with a positive margin over the next radius. The
best fitted nuisance profile tries to compensate with high center-frequency
scale, late modeled trace shift, and lower amplitude:

```text
fc scale = 1.1
time shift = 80 ps
amplitude = about 0.767
```

That is a warning for field/lab use. A source model that only changes
frequency, timing, and amplitude can still convert source ringing into a
geometry/radius bias.

## Next Decision

Run a mitigation diagnostic before scaling to multi-rebar:

```text
allow the modeled source grid to include a small set of ringdown amplitudes,
then rerun the same 421 cases. Promote only if the ringdown cases return to
r=6.0 mm without damaging nominal/source-mismatch recovery.
```

## 422: Ringdown Stress, Modeled Ringdown Profile

Output:

```text
outputs/experiments/422_source_shape_ringdown_modeled_profile_replication
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|source_mismatch:1.1,-50.0,1.1,0.0,13|ringdown025:1.0,0.0,1.0,0.0,13,0.25,180.0,0.8|ringdown025_noise05_seed13:1.0,0.0,1.0,0.05,13,0.25,180.0,0.8' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-scales 0.0,0.25 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 4 \
  --run-name source_shape_ringdown_modeled_profile_replication
```

Runtime and count:

```text
52 candidates
4 observed cases
3 modeled center-frequency scales
2 modeled ringdown scales
1686.33 s
```

Result:

| Case | Best r [mm] | Next r [mm] | Margin | Best source profile | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.000, ringdown=0.0 | unchanged correct case |
| source_mismatch | 6.0 | 6.2 | 1.146e-03 | fc=1.1, shift=-50 ps, amp=1.100, ringdown=0.0 | unchanged controlled mismatch recovery |
| ringdown025 | 6.0 | 6.2 | 6.247e-04 | fc=1.0, shift=0 ps, amp=1.000, ringdown=0.25 | recovered true radius |
| ringdown025_noise05_seed13 | 6.0 | 6.2 | 4.728e-04 | fc=1.0, shift=0 ps, amp=0.998, ringdown=0.25 | recovered true radius with smaller noisy margin |

Plot validation:

```text
source_profiled_replication_radius_profiles.png:
1651x937 px, dynamic range 255, grayscale std 31.8741
```

Figure notes:

```text
outputs/experiments/422_source_shape_ringdown_modeled_profile_replication/figures/FIGURE_NOTES.md
```

## Mitigation Interpretation

The modeled ringdown basis fixes the failure from experiment 421.

The important comparison is:

| Case | 421 existing profile | 422 modeled ringdown profile |
| --- | --- | --- |
| nominal | r=6.0 | r=6.0 |
| source mismatch | r=6.0 | r=6.0 |
| ringdown025 | r=7.8 wrong | r=6.0 correct |
| ringdown025_noise05_seed13 | r=7.8 wrong | r=6.0 correct |

This does not mean the production optimizer should always carry a large
free-form source model. It means the field/lab branch needs a source-shape
calibration option before trusting radius. A small physically interpretable
basis can prevent source ringing from being mistaken for a larger bar.

## Branch Decision

Promote modeled source-shape profiling as a diagnostic branch, not as the
default production path yet.

Next scaling gates:

```text
1. replicate ringdown-scale cases across at least two noise seeds,
2. test one mismatched ringdown amplitude, such as observed 0.20 or 0.30 with
   modeled grid 0.0,0.25,
3. only after that, try the source-shape profile on a small multi-rebar local
   geometry case.
```

## 423: Ringdown Amplitude/Noise/Source-Mismatch Matrix

Output:

```text
outputs/experiments/423_source_shape_ringdown_modeled_seed_amplitude_matrix
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown030:1.0,0.0,1.0,0.0,13,0.30,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|ringdown025_noise10_seed13:1.0,0.0,1.0,0.10,13,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8|source_mismatch_ringdown025_noise05_seed21:1.1,-50.0,1.1,0.05,21,0.25,180.0,0.8' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-scales 0.0,0.25 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 4 \
  --run-name source_shape_ringdown_modeled_seed_amplitude_matrix
```

Runtime and count:

```text
52 candidates
7 observed cases
3 modeled center-frequency scales
2 modeled ringdown scales
1701.49 s
```

Result:

| Case | Best r [mm] | Next r [mm] | Margin | Best source profile | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | fc=1.0, shift=0 ps, amp=1.000, ringdown=0.0 | correct |
| ringdown020 | 7.8 | 6.8 | 4.400e-04 | fc=1.0, shift=0 ps, amp=0.867, ringdown=0.25 | wrong high-radius branch |
| ringdown030 | 6.0 | 6.2 | 6.766e-04 | fc=1.0, shift=0 ps, amp=1.095, ringdown=0.25 | correct |
| ringdown025_noise05_seed21 | 6.0 | 6.2 | 4.754e-04 | fc=1.0, shift=0 ps, amp=1.000, ringdown=0.25 | correct |
| ringdown025_noise10_seed13 | 6.0 | 6.2 | 3.099e-04 | fc=1.0, shift=0 ps, amp=0.997, ringdown=0.25 | correct but weaker |
| source_mismatch_ringdown025 | 6.0 | 6.2 | 7.469e-04 | fc=1.1, shift=-50 ps, amp=1.100, ringdown=0.25 | correct |
| source_mismatch_ringdown025_noise05_seed21 | 6.0 | 6.2 | 6.539e-04 | fc=1.1, shift=-50 ps, amp=1.101, ringdown=0.25 | correct |

Plot validation:

```text
source_profiled_replication_radius_profiles.png:
1651x937 px, dynamic range 255, grayscale std 36.0666
```

Figure notes:

```text
outputs/experiments/423_source_shape_ringdown_modeled_seed_amplitude_matrix/figures/FIGURE_NOTES.md
```

## 423 Interpretation

The modeled ringdown grid is useful but brittle.

It passes:

```text
observed ringdown 0.25 with 5% and 10% noise,
observed ringdown 0.30,
source frequency/time/amplitude mismatch plus ringdown 0.25,
source mismatch plus ringdown 0.25 and 5% noise.
```

It fails:

```text
observed ringdown 0.20 with modeled grid only 0.0 and 0.25.
```

The failure mode is physically interpretable. The runner can scale the whole
modeled wavelet amplitude, but it cannot independently fit the primary pulse
and delayed ringdown pulse. For observed ringdown 0.20, choosing modeled 0.25
plus a smaller global amplitude changes the primary pulse too much, and the
objective again compensates by selecting a larger bar.

Next mitigation:

```text
fit primary and delayed-ringdown source-basis coefficients by least squares,
then report the inferred ringdown coefficient. This should avoid growing a
large discrete ringdown grid.
```

## 424: Ringdown Basis-Coefficient Fit

Output:

```text
outputs/experiments/424_source_shape_ringdown_basis_fit_matrix
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,13|ringdown020:1.0,0.0,1.0,0.0,13,0.20,180.0,0.8|ringdown030:1.0,0.0,1.0,0.0,13,0.30,180.0,0.8|ringdown025_noise05_seed21:1.0,0.0,1.0,0.05,21,0.25,180.0,0.8|ringdown025_noise10_seed13:1.0,0.0,1.0,0.10,13,0.25,180.0,0.8|source_mismatch_ringdown025:1.1,-50.0,1.1,0.0,13,0.25,180.0,0.8|source_mismatch_ringdown025_noise05_seed21:1.1,-50.0,1.1,0.05,21,0.25,180.0,0.8' \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --fit-ringdown-coefficient \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 4 \
  --run-name source_shape_ringdown_basis_fit_matrix
```

Runtime and count:

```text
52 candidates
7 observed cases
3 modeled center-frequency scales
primary + ringdown source bases per frequency scale
1709.48 s
```

Result:

| Case | Best r [mm] | Next r [mm] | Margin | Fitted source profile | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
| nominal | 6.0 | 6.2 | 9.561e-04 | fc=1.0, shift=0 ps, primary=1.000, ringdown=0.000 | correct |
| ringdown020 | 6.0 | 6.2 | 7.591e-04 | fc=1.0, shift=0 ps, primary=1.000, ringdown=0.200 | recovered former failure |
| ringdown030 | 6.0 | 6.2 | 5.052e-04 | fc=1.0, shift=0 ps, primary=1.000, ringdown=0.300 | correct |
| ringdown025_noise05_seed21 | 6.0 | 6.2 | 4.721e-04 | fc=1.0, shift=0 ps, primary=0.998, ringdown=0.251 | correct |
| ringdown025_noise10_seed13 | 6.0 | 6.2 | 3.128e-04 | fc=1.0, shift=0 ps, primary=0.999, ringdown=0.249 | correct but weakest margin |
| source_mismatch_ringdown025 | 6.0 | 6.2 | 7.442e-04 | fc=1.1, shift=-50 ps, primary=1.100, ringdown=0.250 | correct combined mismatch |
| source_mismatch_ringdown025_noise05_seed21 | 6.0 | 6.2 | 6.490e-04 | fc=1.1, shift=-50 ps, primary=1.102, ringdown=0.250 | correct combined noisy mismatch |

Plot validation:

```text
source_profiled_replication_radius_profiles.png:
1651x937 px, dynamic range 255, grayscale std 35.5835
```

Figure notes:

```text
outputs/experiments/424_source_shape_ringdown_basis_fit_matrix/figures/FIGURE_NOTES.md
```

## Source-Shape Branch Decision

The basis-coefficient source profile closes the first field-like source-shape
stress at the single-rebar level.

Progression:

```text
421: no modeled ringdown -> ringdown cases fail at r=7.8 mm
422: discrete modeled ringdown 0.0/0.25 -> exact 0.25 ringdown fixed
423: same discrete grid -> observed 0.20 ringdown fails at r=7.8 mm
424: primary/ringdown coefficient fit -> all tested rows recover r=6.0 mm
```

Decision:

```text
Promote source-basis coefficient fitting as the source-shape calibration
diagnostic. Do not scale the discrete ringdown-grid version. Before field/lab
claims, report fitted primary/ringdown coefficients and radius margins.
```

Next scale gate:

```text
Apply the coefficient-fit source profile to one small multi-rebar local
geometry case, but only after keeping the candidate window narrow enough to
avoid a broad GPU sweep.
```
