# Experiment 17: Low-Band Seed Robustness Under Noise

## Goal

Test the practical workflow that survived Experiment 16 under controlled
observed-data noise:

```text
2 mm coarse seed
-> 1 mm low-band Powell objective, 0.2-0.8 GHz
-> full-band coarse grid polish
```

Experiment 16 showed that full-band Powell pulls the solution back toward the
high-radius basin, while full-band coarse polish can recover the true radius.
This experiment checks whether the same two-stage workflow is still useful when
the observed synthetic data contain noise.

## Plain Terms

- **Low-band seed**: Powell sees only the 0.2-0.8 GHz filtered traces.
- **Full-band polish**: the final deterministic local grid search uses the
  original full traces.
- **Controlled noise**: Gaussian noise is added to the observed synthetic data
  at a fixed RMS fraction and seed, so runs are repeatable.

## Baseline For Comparison

Earlier noisy full-band Powell plus coarse polish runs:

```text
020_single_rebar_grid1mm_noise05_coarsepolish
021_single_rebar_grid1mm_noise05_seed21_coarsepolish
022_single_rebar_grid1mm_noise10_coarsepolish
023_single_rebar_grid1mm_noise10_coarsepolish_topk
```

Those runs already showed that coarse polish can recover the true model at
5-10% noise in these controlled cases. The question here is whether the
paper-inspired low-band seed makes the path cheaper, cleaner, or more robust.

## Run Log

### 034 - 5% noise, low-band Powell seed

Purpose: repeat the Experiment 16 low-band seed stage with the same 5% noise
seed used by earlier baseline run 020.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 8 \
  --max-evals 35 \
  --run-name bandwidth_noise05_stage1_020_080_seed13 \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 13 \
  --objective-bandpass-ghz 0.2,0.8 \
  --objective-bandpass-taper-ghz 0.05
```

Output:

```text
outputs/experiments/034_bandwidth_noise05_stage1_020_080_seed13/
```

Result:

```text
recovered:       x=250.353 mm, z=90.527 mm, radius=6.999 mm
filtered J:      3.6113e-04
full-data NRMS:  5.092%
model NRMS:      1.345%
runtime:         185.4 s
NRCCC:           1.0
```

Interpretation: unlike the exact-data low-band run, the noisy low-band seed did
not reduce radius bias. It found an accurate location but stayed in the
high-radius basin.

### 035 - 5% noise, full-band coarse polish from low-band seed

Purpose: test whether full-band coarse polish still corrects the noisy low-band
seed.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name bandwidth_noise05_full_coarsepolish_from_lowband_seed13 \
  --init-x-mm 250.35318784626654 \
  --init-z-mm 90.52658779707531 \
  --init-radius-mm 6.998877393910328 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 13 \
  --grid-polish \
  --grid-polish-preset coarse \
  --polish-top-k 10
```

Output:

```text
outputs/experiments/035_bandwidth_noise05_full_coarsepolish_from_lowband_seed13/
```

Result:

```text
recovered:       x=250.000 mm, z=90.000 mm, radius=6.000 mm
best J:          5.8565e-02
full-data NRMS:  5.021%
model NRMS:      0
runtime:         216.7 s
polish evals:    40
NRCCC:           1.0
```

Top polish candidates:

```text
rank  J             x_mm   z_mm   radius_mm
1     5.8565e-02    250.0  90.0   6.0
2     5.8565e-02    250.0  90.5   6.0
3     5.9382e-02    250.0  90.0   6.2
4     5.9382e-02    250.0  90.5   6.2
5     6.0876e-02    250.0  91.0   6.8
6     6.1509e-02    250.0  91.0   7.0
```

Comparison with earlier run 020:

```text
020 full-band Powell + coarse polish:
  final = true model, total runtime = 490.5 s

034 + 035 low-band seed + full-band coarse polish:
  final = true model, combined runtime = 402.1 s
```

Interpretation: the low-band seed did not improve radius under this 5% noise
case, but it still produced a seed inside the same local polish window. The
two-stage workflow recovered the true model and was about 18% faster than the
earlier full-band Powell plus polish baseline for the same noise seed.

## Current Conclusion

The low-band seed is not reliably radius-correcting by itself under noise. Its
practical value is runtime reduction: it can replace the longer full-band
Powell stage before deterministic coarse polish.

For controlled 5% noise, the current best workflow is still:

```text
bounded coarse seed
-> short/local optimizer stage for x-z basin
-> full-band coarse polish with top-candidate reporting
```

The next useful test is the same two-stage workflow at 10% noise, because run
023 showed that radius margins become much tighter there.

### 036 - 10% noise, low-band Powell seed

Purpose: repeat the low-band seed stage at the harder 10% noise level used by
earlier run 023.

Output:

```text
outputs/experiments/036_bandwidth_noise10_stage1_020_080_seed13/
```

Result:

```text
recovered:       x=249.858 mm, z=90.769 mm, radius=6.927 mm
filtered J:      1.1884e-03
full-data NRMS:  10.046%
model NRMS:      1.345%
runtime:         186.0 s
NRCCC:           1.0
```

Interpretation: the 10% noisy low-band seed again finds the correct local x-z
region but stays in the high-radius basin.

### 037 - 10% noise, full-band coarse polish from low-band seed

Purpose: check whether the final full-band polish margin changes when the
polish starts from the 10% noisy low-band seed.

Output:

```text
outputs/experiments/037_bandwidth_noise10_full_coarsepolish_from_lowband_seed13/
```

Result:

```text
recovered:       x=250.000 mm, z=90.000 mm, radius=6.000 mm
best J:          1.9916e-01
full-data NRMS:  10.005%
model NRMS:      0
runtime:         217.5 s
polish evals:    40
```

Top polish candidates:

```text
rank  J             x_mm   z_mm   radius_mm
1     1.9916e-01    250.0  90.0   6.0
2     1.9916e-01    250.0  90.5   6.0
3     1.9972e-01    250.0  90.0   6.2
4     1.9972e-01    250.0  90.5   6.2
5     2.0142e-01    250.0  91.0   6.8
6     2.0183e-01    250.0  91.0   7.0
```

Comparison with earlier run 023:

```text
023 direct coarse polish from high-radius seed:
  final = true model, best J = 1.9916e-01, runtime = 224.3 s

036 + 037 low-band seed + full-band coarse polish:
  final = true model, best J = 1.9916e-01, combined runtime = 403.5 s
```

Interpretation: the final candidate ordering is effectively identical to run
023. The low-band stage does not improve the 10% noise radius margin and adds
about 186 s when the seed is already inside the coarse-polish window.

## Updated Conclusion

Noise changed the value of the PEBDD-style low-band stage:

```text
exact data:
  low-band Powell improves the radius seed from about 6.95 mm to 6.57 mm

5% noise:
  low-band Powell stays near 7.00 mm radius

10% noise:
  low-band Powell stays near 6.93 mm radius
```

Full-band coarse polish remains the reliable radius selector in these
controlled cases. The low-band objective is not yet a robust replacement for
polish and should not be treated as a radius-estimation solution by itself.

Practical recommendation after this experiment:

```text
If the current seed is already close enough for the coarse-polish window,
skip low-band Powell and run full-band coarse polish directly.

Use low-band Powell only when we need to move a rough seed into the local x-z
window before polish.
```

The next paper-backed direction should be cumulative frequency and
per-frequency misfit reporting, because the current bandpass schedule did not
explain which spectral components are driving the high-radius basin.
