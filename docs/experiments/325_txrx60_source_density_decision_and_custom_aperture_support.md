# Experiment 325: Tx/Rx=60 Source-Density Decision and Custom Aperture Support

## Purpose

This is the compact decision synthesis requested after completing the
target-specific Tx/Rx=60 ringdown025 source-density branch. It consolidates
runs 754-756 and 783-791, records the implementation change needed for custom
aperture tests, and defines the next GPU experiment.

No numbered output folder is created for this document because it is not a new
physical inversion run. The next physical output will be the custom-aperture
GPU run.

## Evidence Matrix

All rows use the seed89 source-mismatch/ringdown025/noise10 stress with
Tx/Rx=60 mm, nearest receiver sampling, exact initial geometry, and the same
12-candidate local z/radius grid for the target under update.

| Target | Sources | Run | Scan x positions mm | Base margin | Ratio to 5-source row | Confidence |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 0 | 5 | 756 | 50, 146, 250, 346, 450 | 5.193087e-04 | 1.000 | moderate |
| 0 | 7 | 784 | 50, 114, 178, 250, 314, 378, 450 | 5.677174e-04 | 1.093 | moderate |
| 0 | 8 | 789 | 50, 106, 162, 218, 274, 330, 386, 450 | 5.899921e-04 | 1.136 | moderate |
| 0 | 9 | 788 | 50, 98, 146, 194, 250, 298, 346, 394, 450 | 4.631165e-04 | 0.892 | weak |
| 1 | 5 | 754 | 50, 146, 250, 346, 450 | 5.319351e-04 | 1.000 | moderate |
| 1 | 7 | 785 | 50, 114, 178, 250, 314, 378, 450 | 3.489046e-04 | 0.656 | weak |
| 1 | 8 | 790 | 50, 106, 162, 218, 274, 330, 386, 450 | 4.999206e-04 | 0.940 | weak |
| 1 | 9 | 786 | 50, 98, 146, 194, 250, 298, 346, 394, 450 | 5.181917e-04 | 0.974 | moderate |
| 2 | 5 | 755 | 50, 146, 250, 346, 450 | 4.318875e-04 | 1.000 | weak |
| 2 | 7 | 783 | 50, 114, 178, 250, 314, 378, 450 | 5.100529e-04 | 1.181 | moderate |
| 2 | 8 | 791 | 50, 106, 162, 218, 274, 330, 386, 450 | 5.243427e-04 | 1.214 | moderate |
| 2 | 9 | 787 | 50, 98, 146, 194, 250, 298, 346, 394, 450 | 5.780025e-04 | 1.338 | moderate |

## Interpretation

No tested uniform source count is globally reliable for all three targets.
Five sources misses target 2, seven sources misses target 1, eight sources
keeps target 1 just below the moderate cutoff, and nine sources misses target
0. This is not a monotonic source-density effect. It is an aperture-layout
effect coupled to target position, Tx/Rx offset, and source-profile fitting.

The best target-specific rows are:

```text
target 0: 8 sources, run 789, margin 5.899921e-04, moderate
target 1: 5 sources or 9 sources, run 754/run 786, moderate
target 2: 9 sources, run 787, margin 5.780025e-04, moderate
```

The next hypothesis is that a custom aperture can preserve the strong
8-source target-0 behavior while adding an exact center shot that helps the
target-1 row. The first candidate aperture is the 8-source layout plus x=250
mm:

```text
custom scan x positions: [50, 106, 162, 218, 250, 274, 330, 386, 450] mm
```

This is intentionally not the uniform 9-source layout. It avoids the uniform
9-source spacing that made target 0 weak, while adding the center sample that
the 8-source layout lacked.

## Implementation

Added custom aperture support to the shared scan-position helper and coordinate
optimizer CLI:

```text
run_multi_rebar_common_radius_profile.py
  build_scan_positions(..., scan_x_values_m=None)

run_multi_rebar_coordinate_optimizer.py
  --scan-x-values-mm 50,106,162,218,250,274,330,386,450
```

When `--scan-x-values-mm` is provided, the optimizer uses those positions
instead of the uniform `--sources` grid. The summary records the actual scan
length as `sources`, so custom runs remain comparable in downstream tables.

Validation rules for custom apertures:

```text
positions must be finite
positions must be strictly increasing
positions must remain inside the configured scan domain
nearest and linear receiver sampling both continue to use the same Tx/Rx offset logic
```

## Tests

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_multi_rebar_local_geometry_profile.py tests/test_multi_rebar_coordinate_optimizer.py -q
34 passed in 0.32 s

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
300 passed in 24.71 s
```

## Next GPU Run

Run target 1 first with the custom aperture because target 1 is the row that
the 8-source layout nearly but not quite rescued. If target 1 becomes
moderate, run target 0 and target 2 with the same custom aperture to test
whether this layout can give all three targets moderate rows.

Planned command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --scan-x-values-mm 50,106,162,218,250,274,330,386,450 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_custom8pluscenter_txrx60_ringdown025_objectives
```
