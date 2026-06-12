# Experiment 308: Three-Seed Cross-Seed Linear Receiver Summary

## Purpose

Run 775 updates the cross-seed target-2 linear receiver-sampling summary after
the seed13 replication in run 774. It turns the prior two-seed comparison into
a three-seed classification package.

## 775: Three-Seed Cross-Seed Linear Receiver Summary

Output:

```text
outputs/experiments/775_three_seed_cross_seed_linear_receiver_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_cross_seed_linear_receiver_summary.py \
  --run-name three_seed_cross_seed_linear_receiver_summary
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
| seed13 | nearest Tx/Rx=50 | 8.105729e-04 | 1.000 | moderate |
| seed13 | linear Tx/Rx=50.3125 | 6.007860e-04 | 0.741 | moderate |
| seed21 | nearest Tx/Rx=50 | 8.000475e-04 | 1.000 | moderate |
| seed21 | linear Tx/Rx=50.0390625 | 5.770182e-04 | 0.721 | moderate |
| seed21 | linear Tx/Rx=50.3125 | 5.779376e-04 | 0.722 | moderate |
| seed89 | nearest Tx/Rx=50 | 9.935884e-04 | 1.000 | moderate |
| seed89 | linear Tx/Rx=50.0390625 | 4.775098e-04 | 0.481 | weak |
| seed89 | linear Tx/Rx=50.3125 | 4.769427e-04 | 0.480 | weak |

Summary JSON:

```text
rows: 8
seed count: 3
confidence labels: moderate=6, weak=2
best truth-preserving objective counts: late_high=7, late=1
seed13 nonzero linear rows: all moderate
seed21 nonzero linear rows: all moderate
seed89 nonzero linear rows: all weak
```

## Interpretation

Run 775 changes the branch conclusion from a two-seed split to a three-seed
pattern: seed13 and seed21 remain moderate under nonzero linear receiver
sampling, while seed89 is weak. The linear receiver effect is still real, but
the weak classification is seed-sensitive.

This closes the sub-grid receiver-offset branch for now. More bisection is not
informative because the tested nonzero offsets form flat plateaus within each
seed. A fourth seed would only estimate how often the seed89-like weak plateau
occurs.

## Validation

```text
focused cross-seed/linear summary tests: 7 passed
figure validation: both PNGs are 1617x886 with dynamic range 255
visual inspection: both figures are readable
JSON parse: run_manifest.json and cross_seed_linear_receiver_summary.json pass
figure notes: figures/FIGURE_NOTES.md present
```

## Next Decision

Move to a different factor rather than another sub-grid Tx/Rx bisection. A
reasonable next GPU branch is target-1 or target-0 linear receiver sensitivity,
or a different acquisition/source condition.
