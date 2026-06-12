# Experiment 311: Seed89 All-Target Linear Receiver Summary

## Purpose

Run 778 summarizes the all-target seed89 linear receiver-sampling package at
Tx/Rx=50.3125 mm. It compares targets 0, 1, and 2 against their own
nearest-grid Tx/Rx=50 baselines.

## 778: Seed89 Target Linear Receiver Summary

Output:

```text
outputs/experiments/778_seed89_target_linear_receiver_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_seed89_target_linear_receiver_summary.py \
  --run-name seed89_target_linear_receiver_summary
```

## Artifacts

```text
README.md
data/seed89_target_linear_receiver_rows.csv
data/seed89_target_linear_receiver_summary.json
figures/seed89_linear_ratio_by_target.png
figures/seed89_margin_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

| Target | Nearest Tx/Rx=50 margin | Linear Tx/Rx=50.3125 margin | Ratio | Linear confidence |
| --- | ---: | ---: | ---: | --- |
| target 0 | 5.798369e-04 | 5.789458e-04 | 0.998 | moderate |
| target 1 | 5.982895e-04 | 5.985570e-04 | 1.000 | moderate |
| target 2 | 9.935884e-04 | 4.769427e-04 | 0.480 | weak |

Summary JSON:

```text
rows: 6
target count: 3
linear confidence labels: moderate=2, weak=1
weak linear targets: [2]
moderate linear targets: [0, 1]
best truth-preserving objective counts: veryhigh=2, late_high=4
```

## Interpretation

Run 778 shows that the seed89 target-2 weak plateau is target-specific. The
same linear Tx/Rx=50.3125 receiver perturbation leaves targets 0 and 1
moderate and essentially unchanged from their nearest-grid baselines, while
target 2 drops to 0.480x and becomes weak.

This pairs with run 775's cross-seed result: the effect is not universal across
seeds and not universal across targets. Treat it as a specific deep-target
sensitivity under seed89 until another acquisition/source condition reproduces
it.

## Validation

```text
focused target-summary tests: 6 passed
regenerated after annotation fix: focused tests 2 passed
figure validation: both PNGs are 1515x835 with dynamic range 255
visual inspection: both figures are readable after annotation fix
JSON parse: run_manifest.json and seed89_target_linear_receiver_summary.json pass
figure notes: figures/FIGURE_NOTES.md present
```

## Next Decision

Move to a different acquisition/source factor for target 2 rather than another
sub-grid Tx/Rx bisection.
