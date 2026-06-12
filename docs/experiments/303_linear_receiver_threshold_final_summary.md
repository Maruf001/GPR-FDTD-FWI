# Experiment 303: Final Linear Receiver Target-2 Threshold Summary

## Purpose

Run 770 closes the seed89 target-2 linear receiver-sampling threshold branch by
including the final Tx/Rx=50.0390625 mm bisection row.

## 770: Final Linear Receiver Threshold Summary

Output:

```text
outputs/experiments/770_linear_receiver_threshold_final_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_linear_receiver_threshold_summary.py \
  nearest50=outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives \
  linear50p0390625=outputs/experiments/769_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p0390625_linear_receiver_ringdown025_objectives \
  linear50p078125=outputs/experiments/767_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p078125_linear_receiver_ringdown025_objectives \
  linear50p15625=outputs/experiments/766_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p15625_linear_receiver_ringdown025_objectives \
  linear50p3125=outputs/experiments/765_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives \
  nearest51=outputs/experiments/763_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p625_ringdown025_objectives \
  --run-name linear_receiver_threshold_final_summary
```

## Results

| Run | Label | Sampling | Tx/Rx mm | Offset delta cells | Base margin | Confidence | Ratio to baseline |
| ---: | --- | --- | ---: | ---: | ---: | --- | ---: |
| 745 | nearest50 | nearest | 50.000000 | 0.000000 | 9.935884e-04 | moderate | 1.000 |
| 769 | linear50p0390625 | linear | 50.039062 | 0.039063 | 4.775098e-04 | weak | 0.481 |
| 767 | linear50p078125 | linear | 50.078125 | 0.078125 | 4.774322e-04 | weak | 0.481 |
| 766 | linear50p15625 | linear | 50.156250 | 0.156250 | 4.772734e-04 | weak | 0.480 |
| 765 | linear50p3125 | linear | 50.312500 | 0.312500 | 4.769427e-04 | weak | 0.480 |
| 763 | nearest51 | nearest | 50.625000 | 1.000000 | 4.752760e-04 | weak | 0.478 |

## Interpretation

The branch-level conclusion is closed for this target/case: every tested
nonzero linear receiver perturbation is exact/weak, even at 0.0390625 cells
from the Tx/Rx=50 baseline. The target-2 radius confidence drop is therefore
effectively immediate once the receiver sample is perturbed away from the
integer-cell Tx/Rx=50 baseline.

## Validation

```text
focused pytest: tests/test_linear_receiver_threshold_summary.py -> 4 passed
full pytest: 292 passed in 24.77s
JSON parse: linear_receiver_threshold_summary.json passes
CSV rows: threshold rows=6
figure validation: both PNGs are 1481x835 with dynamic range 255
visual inspection: both final summary plots are readable after label polish
figure notes: figures/FIGURE_NOTES.md present
```

## Next Decision

Stop linear Tx/Rx bisection for seed89 target 2. Move to a different
experimental factor rather than spending more GPU time below 0.0390625 cells.
