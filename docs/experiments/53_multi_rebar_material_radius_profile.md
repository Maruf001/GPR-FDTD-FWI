# Experiment 53: Multi-Rebar Material-Profiled Radius Evidence

## Goal

Test whether the remaining coupled source-shape center-radius ambiguity is
actually a material-parameter ambiguity.

The target is the known weakest row from experiment 52:

```text
center target, true x/z state, source_mismatch_ringdown025_noise10_seed55,
best r=6.0 mm, next r=6.2 mm, base margin about 1.006e-04
```

The experiment profiles over a small concrete-permittivity and effective
steel-conductivity grid at fixed true x/z and fixed true neighbor radii.

## Implementation

Added a material-aware multi-rebar radius-profile runner:

```text
run_multi_rebar_material_radius_profile.py
```

Extended the shared multi-rebar local-profile model builder so it can accept
material overrides while preserving existing defaults:

```text
run_multi_rebar_local_geometry_profile.py
```

Focused validation:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_multi_rebar_material_radius_profile.py \
  tests/test_multi_rebar_local_geometry_profile.py \
  tests/test_multi_rebar_coordinate_optimizer.py

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_multi_rebar_material_radius_profile.py \
  run_multi_rebar_local_geometry_profile.py \
  run_multi_rebar_coordinate_optimizer.py
```

Result:

```text
34 passed in 0.36 s
py_compile passed
```

## 449: CPU Smoke

Output:

```text
outputs/experiments/449_multi_rebar_material_radius_cpu_smoke
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_material_radius_profile.py \
  --backend cpu \
  --grid-step-mm 20 \
  --sources 1 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 250 \
  --target-z-values-mm 90 \
  --target-radius-values-mm 6.0,6.2 \
  --concrete-epsr-values 6.0 \
  --rebar-log10-sigma-values 7 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --source-frequency-scales 1.1 \
  --source-time-shift-ps-values=-50 \
  --fit-ringdown-coefficient \
  --progress-every 1 \
  --top-k 2 \
  --run-name multi_rebar_material_radius_cpu_smoke
```

Smoke result:

```text
2 candidates
coarse 20 mm grid
best r=6.0 mm, next r=6.2 mm, margin=0.0
```

Plot validation:

```text
multi_rebar_material_profiled_radius.png:
1515x903 px, dynamic range 255, grayscale std 32.8676
```

Interpretation:

```text
This run is not scientific because the 20 mm grid aliases both radii. It only
validates CLI, CSV, summary, figure, and figure-note generation.
```

## 450: Center True-State Material Radius Profile

Output:

```text
outputs/experiments/450_multi_rebar_center_material_radius_profile_seed55_true_state
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_material_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 250 \
  --target-z-values-mm 90 \
  --target-radius-values-mm 5.8:6.2:0.2 \
  --concrete-epsr-values 5.8,6.0,6.2 \
  --rebar-log10-sigma-values 5,7 \
  --replication-cases 'source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8' \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --progress-every 1 \
  --top-k 12 \
  --run-name multi_rebar_center_material_radius_profile_seed55_true_state
```

Runtime and count:

```text
582.5 s
18 candidates
3 target radii: 5.8, 6.0, 6.2 mm
3 concrete epsr values: 5.8, 6.0, 6.2
2 rebar conductivity values: 1e5 and 1e7 S/m
```

Case summary:

| Case | Best x/z/r [mm] | Next radius [mm] | Margin | Relative margin | Best epsr | Best log10 sigma |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| source_mismatch_ringdown025_noise10_seed55 | 250 / 90 / 6.0 | 6.2 | 1.019e-04 | 1.606e-03 | 6.0 | 5.0 |

Top candidates:

| Rank | Radius [mm] | Concrete epsr | Rebar log10 sigma | Misfit |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 6.0 | 6.0 | 5.0 | 0.0634533681252 |
| 2 | 6.0 | 6.0 | 7.0 | 0.0634546925178 |
| 3 | 6.2 | 6.0 | 7.0 | 0.0635553024155 |
| 4 | 6.2 | 6.0 | 5.0 | 0.0635554239174 |
| 5 | 5.8 | 6.0 | 5.0 | 0.0657230630969 |
| 6 | 5.8 | 6.0 | 7.0 | 0.0657277359505 |

Best by radius after material profiling:

| Radius [mm] | Best epsr | Best log10 sigma | Misfit |
| ---: | ---: | ---: | ---: |
| 5.8 | 6.0 | 5.0 | 0.0657230630969 |
| 6.0 | 6.0 | 5.0 | 0.0634533681252 |
| 6.2 | 6.0 | 7.0 | 0.0635553024155 |

Plot validation:

```text
multi_rebar_material_profiled_radius.png:
1515x903 px, dynamic range 255, grayscale std 31.9821
```

Figure notes:

```text
outputs/experiments/450_multi_rebar_center_material_radius_profile_seed55_true_state/figures/FIGURE_NOTES.md
```

## Interpretation

Material profiling does not explain away the weak 6.0-6.2 mm center-radius
interval.

Concrete relative permittivity is not free in this setup:

```text
epsr=6.0 dominates the top candidates, while epsr=5.8 and 6.2 have much larger
objectives.
```

Effective steel conductivity is saturated:

```text
1e5 and 1e7 S/m are nearly interchangeable near the true radius. The best row
uses log10 sigma=5, but it beats log10 sigma=7 by only 1.324e-06.
```

The radius conclusion is unchanged:

```text
r=6.0 remains the best point, r=6.2 remains the adjacent weak competitor, and
the profiled material margin is 1.019e-04, essentially the same as experiment
447's base margin of 1.006e-04.
```

## Decision

Do not add concrete epsr or rebar conductivity as free production optimizer
parameters for this branch. They do not collapse the center-radius ambiguity,
and free material parameters would add degrees of freedom without improving the
radius decision.

The source-shape/material branch should now be reported as:

```text
point-correct for the tested coupled coordinate states,
but center radius remains interval-supported at 6.0-6.2 mm in the weakest
source-mismatch/ringdown/noise row.
```

Next useful work should move away from this local source/material ambiguity and
pick an uncovered multi-rebar branch, such as a staged variable-radius geometry
or a different acquisition/material stress with a clear decision gate.
