# Experiment 22: Faithful Spectrum-Derived PEBDD Schedule

## Goal

Run a PEBDD-style staged objective schedule using bands chosen from Experiment
21 spectra instead of the earlier guessed low bands.

Spectrum-derived schedule:

```text
stage 1: 0.35-1.10 GHz
stage 2: 0.35-1.50 GHz
stage 3: 0.35-2.00 GHz
stage 4: 0.35-2.50 GHz
final:   full-band coarse polish
```

## Code Changes

Added:

```text
run_single_rebar_bandwidth_schedule.py
tests/test_bandwidth_schedule_runner.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_bandwidth_schedule_runner.py -q
3 passed
```

## Run Log

### 045_pebd_spectrum_bands_exact

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_bandwidth_schedule.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --bands-ghz '0.35,1.10|0.35,1.50|0.35,2.00|0.35,2.50' \
  --stage-max-iter 8 \
  --stage-max-evals 35 \
  --final-polish \
  --polish-top-k 10 \
  --run-name pebd_spectrum_bands_exact
```

Output:

```text
outputs/experiments/045_pebd_spectrum_bands_exact
```

Stage summary:

| Stage | Band | x [mm] | z [mm] | r [mm] | J | Runtime [s] |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| stage01 | 0.35-1.10 GHz | 249.599 | 90.617 | 6.864 | 8.598e-05 | 192.1 |
| stage02 | 0.35-1.50 GHz | 249.684 | 90.588 | 6.865 | 1.763e-04 | 149.6 |
| stage03 | 0.35-2.00 GHz | 249.757 | 90.581 | 6.896 | 4.823e-04 | 133.4 |
| stage04 | 0.35-2.50 GHz | 249.786 | 90.640 | 6.930 | 1.124e-03 | 138.9 |
| final polish | full band | 250.000 | 90.000 | 6.000 | 0.000e+00 | 224.2 |

Final full-band grid-polish top candidates:

| Rank | x [mm] | z [mm] | r [mm] | J |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 250.0 | 90.0 | 6.0 | 0.000e+00 |
| 2 | 250.0 | 90.5 | 6.0 | 0.000e+00 |
| 3 | 250.0 | 90.0 | 6.2 | 1.037e-03 |
| 4 | 250.0 | 90.5 | 6.2 | 1.037e-03 |
| 5 | 250.0 | 91.0 | 6.8 | 2.083e-03 |

Figure validation:

All generated stage and final figures passed the saved-image dynamic-range
check. The repaired templates produced nonblank B-scans, compact convergence
plots, and non-overlapping model-comparison colorbars.

## Interpretation

The spectrum-derived PEBDD schedule did what it is expected to do for the
large-scale basin: it kept the candidate near the correct lateral position and
cover depth. It did not solve the radius bias. The staged Powell result moved
from r=6.864 mm to r=6.930 mm as bandwidth expanded, so the high-radius basin
remained attractive even when the band reached 2.5 GHz.

The final full-band local grid polish recovered the exact synthetic truth:
x=250.0 mm, z=90.0 mm, r=6.0 mm. The best distinct-radius margin was the same
known exact-data margin from the single-frequency polish: r=6.0 beats r=6.2 by
1.037e-03. This means the radius information is present in the data, but the
continuous local Powell objective is not reliably descending into that discrete
radius basin.

## Next Decision

Do not spend the next run on another Powell-only PEBDD schedule. The next
paper-aligned step is the WRI/cumulative-frequency branch: quantify whether
frequency weighting improves or dilutes radius margins on the same local
x/z/r candidate grid. This directly tests the paper warning that blindly
averaging frequencies can weaken the parameter evidence we care about.
