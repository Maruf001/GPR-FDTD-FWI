# Experiment 25: Rebar LS Versus W2 Local Landscape

## Goal

Test whether the trace-level Softplus/Sinkhorn W2 behavior from Experiment 24
helps the actual single-rebar radius/depth objective.

Question:

```text
On the same local x/z/r candidate grid, does W2 improve the true-radius basin
or margin compared with the existing normalized L2 objective?
```

This is a gate before any optimizer integration.

## Code Changes

Added:

```text
run_single_rebar_w2_landscape.py
tests/test_single_rebar_w2_landscape.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_single_rebar_w2_landscape.py \
  tests/test_trace_wasserstein.py -q
8 passed
```

## Planned Exact Matrix

Candidate grid:

```text
x:      250.0 mm
z:      90.0, 90.5, 91.0, 91.5 mm
radius: 5.4-7.8 mm in 0.2 mm steps
```

Objective comparison:

```text
LS: normalized existing waveform objective
W2: Softplus/Sinkhorn divergence, beta=8, epsilon=0.02, downsample=16
```

The W2 calculation is intentionally windowed by the existing mute and
downsampled before Sinkhorn. This is a diagnostic landscape, not a final
production objective.

## Run Log

### 050_w2_landscape_exact_beta8_ds16

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_w2_landscape.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --beta 8 \
  --epsilon 0.02 \
  --downsample 16 \
  --run-name w2_landscape_exact_beta8_ds16
```

Output:

```text
outputs/experiments/050_w2_landscape_exact_beta8_ds16
```

Plot validation:

```text
w2_radius_profiles.png: 1889x801 px, dynamic range 255
```

Margin comparison:

| Objective | Best r [mm] | Next r [mm] | Margin |
| --- | ---: | ---: | ---: |
| LS | 6.0 | 6.2 | 1.037e-03 |
| W2 beta=8 ds=16 | 6.0 | 6.2 | 1.060e-07 |

Top candidate comparison:

```text
LS top:
  r=6.0, z=90.0/90.5, J=0
  r=6.2, z=90.0/90.5, J=1.037e-03
  r=6.8, z=91.0, J=2.083e-03

W2 top:
  r=6.0, z=90.0/90.5, J=0
  r=6.2, z=90.0/90.5, J=1.060e-07
  r=6.0, z=91.0, J=4.634e-07
```

## Interpretation After First Landscape

The trace-level W2 convexity benefit from Experiment 24 does not automatically
help radius selection. With Softplus normalization and downsample=16, W2 nearly
flattens the radius evidence. It still identifies the exact synthetic truth as
the best candidate, but the margin against r=6.2 is about four orders of
magnitude smaller than LS.

This is consistent with the risk noted in the paper notes:

```text
Softplus mass normalization can suppress amplitude information.
```

For this single-rebar problem, radius is strongly tied to scattering amplitude
and local waveform detail, not just transport/shift. A W2-only geometry
optimizer would likely be a poor final radius estimator.

## Next Decision

Run one sensitivity check with less aggressive downsampling. If W2 remains
weak at downsample=8, do not integrate W2 as a radius-selection objective.
Keep it as a possible basin/cycle-skipping diagnostic only.

### 051_w2_landscape_exact_beta8_ds8

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_w2_landscape.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --beta 8 \
  --epsilon 0.02 \
  --downsample 8 \
  --run-name w2_landscape_exact_beta8_ds8
```

Output:

```text
outputs/experiments/051_w2_landscape_exact_beta8_ds8
```

Plot validation:

```text
w2_radius_profiles.png: 1889x801 px, dynamic range 255
```

Sensitivity comparison:

| Run | W2 downsample | LS margin | W2 margin |
| --- | ---: | ---: | ---: |
| 050 | 16 | 1.037e-03 | 1.060e-07 |
| 051 | 8 | 1.037e-03 | 1.033e-07 |

The top W2 candidates remained:

```text
r=6.0, z=90.0/90.5: J=0
r=6.2, z=90.0/90.5: J=1.033e-07
r=6.0, z=91.0:      J=4.594e-07
```

## W2 Landscape Decision

Reject Softplus/Sinkhorn W2 as a final radius-selection objective for the
current single-rebar geometry pipeline.

Reason:

```text
The W2 trace test improves shift convexity, but the rebar radius problem is
not primarily a large-shift problem. Radius evidence is amplitude/detail-heavy.
Softplus mass normalization removes too much of that evidence.
```

What remains useful:

```text
W2 may still be useful as a basin/cycle-skipping diagnostic in field-data or
poor-initial-model cases.
For the current synthetic single-rebar radius task, keep LS / weighted LS /
local radius profiling as the primary path.
```

Do not build a W2-Powell or W2-LS hybrid optimizer unless a future rough-seed
or field-data landscape shows W2 improves basin capture without destroying
radius separation.
