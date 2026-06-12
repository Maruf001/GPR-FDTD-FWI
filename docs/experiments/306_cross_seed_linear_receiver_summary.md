# Experiment 306: Cross-Seed Linear Receiver Summary

## Purpose

Run 773 summarizes the seed89 and seed21 target-2 linear receiver-sampling
branches. It was created after runs 771 and 772 showed that seed21 remains
exact/moderate at nonzero linear receiver offsets where seed89 is exact/weak.

## 773: Cross-Seed Linear Receiver Summary

Output:

```text
outputs/experiments/773_cross_seed_linear_receiver_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_cross_seed_linear_receiver_summary.py \
  --run-name cross_seed_linear_receiver_summary
```

Input runs:

```text
741 seed21 nearest Tx/Rx=50
771 seed21 linear Tx/Rx=50.0390625
772 seed21 linear Tx/Rx=50.3125
745 seed89 nearest Tx/Rx=50
769 seed89 linear Tx/Rx=50.0390625
765 seed89 linear Tx/Rx=50.3125
```

## Artifacts

```text
README.md
data/cross_seed_linear_receiver_rows.csv
data/cross_seed_linear_receiver_summary.json
figures/cross_seed_linear_base_margin_by_delta.png
figures/cross_seed_linear_margin_ratio_by_delta.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

| Seed | Condition | Base margin | Ratio to same-seed Tx/Rx=50 | Confidence |
| --- | --- | ---: | ---: | --- |
| seed21 | nearest Tx/Rx=50 | 8.000475e-04 | 1.000 | moderate |
| seed21 | linear Tx/Rx=50.0390625 | 5.770182e-04 | 0.721 | moderate |
| seed21 | linear Tx/Rx=50.3125 | 5.779376e-04 | 0.722 | moderate |
| seed89 | nearest Tx/Rx=50 | 9.935884e-04 | 1.000 | moderate |
| seed89 | linear Tx/Rx=50.0390625 | 4.775098e-04 | 0.481 | weak |
| seed89 | linear Tx/Rx=50.3125 | 4.769427e-04 | 0.480 | weak |

Summary JSON:

```text
rows: 6
seed count: 2
confidence labels: moderate=4, weak=2
best truth-preserving objective: late_high for all 6 rows
seed21 nonzero linear rows: all moderate
seed89 nonzero linear rows: all weak
```

## Interpretation

The target-2 linear receiver effect is real but not seed-universal in
classification. Seed89 has a weak nonzero-linear plateau at about 0.480x its
own nearest-grid baseline. Seed21 has a moderate nonzero-linear plateau at
about 0.721-0.722x its own nearest-grid baseline.

This resolves the immediate contradiction from run 771: a nonzero linear
receiver perturbation does not automatically imply weak confidence. The
correct branch statement is seed-sensitive degradation. Further bisection is
not warranted; a third-seed replication at Tx/Rx=50.3125 is the right next GPU
question if the archive has a comparable fitted-ringdown target-2 baseline.

## Validation

```text
focused tests after script addition: 7 passed
full pytest after script addition: 295 passed in 24.84 s
focused tests after annotation update: 3 passed
JSON parse: run_manifest.json and cross_seed_linear_receiver_summary.json pass
figure validation: both PNGs are 1617x886 with dynamic range 255
visual inspection: both figures are readable after label-offset adjustment
figure notes: figures/FIGURE_NOTES.md present
```

## Next Decision

Inspect the archive for an existing seed13, seed34, or seed55 target-2
nearest-grid fitted-ringdown baseline. If a comparable baseline exists, run one
third-seed target-2 linear Tx/Rx=50.3125 GPU replication with the same
12-candidate grid.
