# Experiment 24: Softplus Sinkhorn W2 Trace Convexity

## Goal

Start the quadratic-Wasserstein paper branch with a small trace-level test
before connecting anything to FDTD inversion.

Question:

```text
Does Softplus-normalized Sinkhorn W2 behave more smoothly than pointwise L2
for shifted oscillatory traces?
```

## Code Changes

Added:

```text
inversion/trace_wasserstein.py
tests/test_trace_wasserstein.py
run_trace_wasserstein_convexity.py
tests/test_trace_wasserstein_convexity_runner.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_trace_wasserstein.py \
  tests/test_trace_wasserstein_convexity_runner.py -q
9 passed
```

The implementation is deliberately isolated. It is not wired into the rebar
optimizer yet.

## Run Log

### 048_trace_wasserstein_convexity_smoke

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_trace_wasserstein_convexity.py \
  --shift-min -28 \
  --shift-max 28 \
  --length 192 \
  --beta-values 4,8,12 \
  --epsilon 0.02 \
  --downsample 1 \
  --run-name trace_wasserstein_convexity_smoke
```

Output:

```text
outputs/experiments/048_trace_wasserstein_convexity_smoke
```

Files:

```text
data/trace_w2_convexity_summary.json
data/trace_w2_convexity.csv
figures/trace_w2_convexity.png
```

Plot validation:

```text
trace_w2_convexity.png: 1804x784 px, dynamic range 255
```

Selected values:

| Shift [samples] | L2 | W2 beta=8 |
| ---: | ---: | ---: |
| 0 | 0.000e+00 | 0.000e+00 |
| 4 | 5.674e-01 | 1.307e-04 |
| 8 | 1.836e+00 | 5.185e-04 |
| 16 | 3.232e+00 | 2.012e-03 |
| 28 | 1.905e+00 | 5.764e-03 |

Monotonicity check away from zero shift:

| Objective | Positive-side violations | Negative-side violations |
| --- | ---: | ---: |
| L2 | 12 | 12 |
| W2 beta=4 | 0 | 0 |
| W2 beta=8 | 0 | 0 |
| W2 beta=12 | 0 | 0 |

## Interpretation

This trace-only smoke test supports the paper's motivation. L2 is not
monotonic with shift for the oscillatory Ricker trace; after the main lobe
moves far enough, pointwise cancellation creates a misleading decrease. The
Softplus/Sinkhorn W2 curves increase smoothly over the tested shift range for
all tested beta values.

This is not yet evidence that W2 improves radius estimation. The current rebar
radius problem is not dominated by large trace shifts because earlier NRCCC
diagnostics were already saturated near 1.0 for the high-radius candidate.

## Next Decision

Do not wire W2 into Powell yet. The next W2 step should be a local rebar
radius/depth landscape comparison:

```text
L2 versus W2,
exact data first,
then 10% noise if exact landscapes are interpretable.
```

The landscape runner must window/downsample traces explicitly so Sinkhorn
runtime stays controlled.
