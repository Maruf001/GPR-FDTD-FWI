# Experiment 301: Linear Receiver Target-2 Threshold Summary

## Purpose

Run 768 packages the target-2 linear receiver-sampling threshold branch after
runs 765-767 showed weak confidence at three nonzero sub-grid offsets.

## 768: Linear Receiver Threshold Summary

Output:

```text
outputs/experiments/768_linear_receiver_threshold_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_linear_receiver_threshold_summary.py \
  --run-name linear_receiver_threshold_summary
```

Final figure-polish regeneration:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_linear_receiver_threshold_summary.py \
  --run-name linear_receiver_threshold_summary \
  --outdir outputs/experiments/768_linear_receiver_threshold_summary
```

## Results

| Run | Label | Sampling | Tx/Rx mm | Offset delta cells | Base margin | Confidence | Ratio to baseline |
| ---: | --- | --- | ---: | ---: | ---: | --- | ---: |
| 745 | nearest50 | nearest | 50.000000 | 0.000000 | 9.935884e-04 | moderate | 1.000 |
| 767 | linear50p078125 | linear | 50.078125 | 0.078125 | 4.774322e-04 | weak | 0.481 |
| 766 | linear50p15625 | linear | 50.156250 | 0.156250 | 4.772734e-04 | weak | 0.480 |
| 765 | linear50p3125 | linear | 50.312500 | 0.312500 | 4.769427e-04 | weak | 0.480 |
| 763 | nearest51 | nearest | 50.625000 | 1.000000 | 4.752760e-04 | weak | 0.478 |

## Interpretation

All three nonzero linear receiver offsets are exact/weak and nearly equal to
the nearest-grid +51 weak layout. The smallest tested nonzero perturbation,
0.078125 cells, already has only 0.4805x the Tx/Rx=50 baseline margin.

The linear receiver branch is therefore exact-but-weak for every tested
nonzero +51 contribution. A final Tx/Rx=50.0390625 GPU run would only refine
the transition onset below 0.078125 cells.

## Validation

```text
focused pytest: tests/test_linear_receiver_threshold_summary.py -> 4 passed
full pytest: 292 passed in 24.68s
JSON parse: linear_receiver_threshold_summary.json passes
CSV rows: threshold rows=5
figure validation: both PNGs are 1481x835 with dynamic range 255
visual inspection: both summary plots are readable after label polish
figure notes: figures/FIGURE_NOTES.md present
```

## Next Decision

Use Tx/Rx=50.0390625 linear receiver sampling only if a final lower-bound
bisection is worth the GPU time. The branch-level claim is already clear:
target 2 weakens for all tested nonzero linear perturbations away from the
Tx/Rx=50 integer-cell baseline.
