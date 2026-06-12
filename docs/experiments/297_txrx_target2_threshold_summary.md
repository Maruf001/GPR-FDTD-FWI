# Experiment 297: Target-2 Tx/Rx Threshold Summary

## Purpose

Run 764 summarizes the seed89 target-2 ringdown025 Tx/Rx branch after the
Tx/Rx=50.625 mm run exposed receiver-grid quantization. It combines only the
comparable 12-candidate target-2 coordinate-optimizer runs.

## 764: Tx/Rx Target-2 Threshold Summary

Output:

```text
outputs/experiments/764_txrx_target2_threshold_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_txrx_target2_threshold_summary.py \
  --run-name txrx_target2_threshold_summary
```

Final figure-polish regeneration:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_txrx_target2_threshold_summary.py \
  --run-name txrx_target2_threshold_summary \
  --outdir outputs/experiments/764_txrx_target2_threshold_summary
```

## Results

All rows keep the exact target-2 geometry at x=350 mm, z=120 mm, r=8 mm.

| Run | Tx/Rx mm | Effective receiver cells | Base margin | Confidence | Ratio to 50 mm | Best diagnostic |
| ---: | ---: | ---: | ---: | --- | ---: | --- |
| 745 | 50.000 | 50 | 9.935884e-04 | moderate | 1.000 | late_high |
| 763 | 50.625 | 51 | 4.752760e-04 | weak | 0.478 | late_high |
| 762 | 51.250 | 51 | 4.752760e-04 | weak | 0.478 | late_high |
| 761 | 52.500 | 52 | 4.724547e-04 | weak | 0.476 | late_high |
| 760 | 55.000 | 55 | 4.604568e-04 | weak | 0.463 | late_high |
| 755 | 60.000 | 60 | 4.318875e-04 | weak | 0.435 | late_high |

Receiver-layout result:

```text
unique receiver layouts: 5
duplicate layout: Tx/Rx=50.625 and 51.25 mm -> 51;51;51;51;49 cells
moderate-to-weak transition: +50 cells -> +51 cells
```

## Interpretation

The target-2 confidence degradation begins at the first tested offset that
changes the dominant receiver layout from +50 cells to +51 cells. Tx/Rx=50.625
and 51.25 mm are not independent physical samples under the current nearest
grid-index receiver model; they duplicate the same receiver layout and return
identical objective metrics.

This closes the fractional bisection branch for the current discrete receiver
model. A Tx/Rx=50.3125 mm GPU run is not justified because it maps to the same
layout as Tx/Rx=50 mm. Further sub-millimeter Tx/Rx work should first implement
or test interpolated receiver sampling.

## Validation

```text
focused pytest: tests/test_txrx_target2_threshold_summary.py -> 4 passed
JSON parse: txrx_target2_threshold_summary.json passes
CSV rows: threshold rows=6
figure validation: both PNGs are 1515x835 with dynamic range 255
visual inspection: requested-offset and receiver-cell plots are readable with no substantive label overlap
figure notes: figures/FIGURE_NOTES.md present
resources: CPU-only summary; GPU stayed idle at about 6%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Do not continue fractional Tx/Rx bisection on the current nearest-grid receiver
model. Move to either a non-duplicating acquisition design or an interpolated
receiver-sampling implementation with tests.
