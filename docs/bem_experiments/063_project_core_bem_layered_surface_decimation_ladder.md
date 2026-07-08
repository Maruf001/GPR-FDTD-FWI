# BEM Experiment 063: Layered Surface Decimation Ladder

Date: 2026-06-25

## Purpose

Use the run `061` layered dense-surface cache to test how much x-sampling is
needed to keep the layered tabulated-surface replay gate closed.

This run does not rerun FDTD. It loads the cached `19x533x17` layered surface
and evaluates several x-sampling policies through the same leave-one-scan
interpolation gate.

## Output

```text
outputs/bem_experiments/063_project_core_bem_layered_surface_decimation_ladder
```

Key artifacts:

```text
data/project_core_bem_layered_surface_decimation_ladder.csv
data/project_core_bem_layered_surface_decimation_ladder_summary.json
figures/project_core_bem_layered_surface_decimation_ladder.png
docs/PROJECT_CORE_BEM_LAYERED_SURFACE_DECIMATION_LADDER.md
```

## Result

```text
policies checked:                   6
ready policies:                     3
minimum ready sample count:         7
best policy:                        full_10mm_cache
best leave-one-scan L2:             0.697021169360853
```

Policy results:

| Policy | Samples | Holdout extrapolated points | LOO L2 | Ready |
| --- | ---: | ---: | ---: | --- |
| exact_source_receiver_only | 10 | 4 | 1.1770012780031571 | false |
| 30mm_grid_only | 7 | 0 | 0.704323503677739 | true |
| 20mm_grid_only | 10 | 0 | 0.9966470335819086 | false |
| 20mm_grid_plus_exact | 14 | 0 | 0.886148899794942 | false |
| center_dense_10mm | 15 | 2 | 0.7091434697819765 | true |
| full_10mm_cache | 19 | 0 | 0.697021169360853 | true |

## Interpretation

The layered cache can be decimated, but sample placement matters more than raw
sample count. The 7-sample `30mm_grid_only` policy passes, while the 10-sample
`20mm_grid_only` policy fails.

The exact source/receiver-only policy reproduces the run `046` sparse failure
because held-out edge scans force extrapolation. The full 10 mm cache remains
the best current policy.

## Decision

Use the full 10 mm cache as the conservative default. Use `30mm_grid_only` only
as a candidate for a future fresh layered stress test, not as a general layered
sampling rule.

This is a tabulated 2D project-core result, not an analytic layered BEM
replacement, measured-field claim, 3D claim, FWI launch gate, or GPU/HPC
escalation.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_surface_decimation_ladder.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_surface_decimation_ladder.py
pass
```

Figure check:

```text
project_core_bem_layered_surface_decimation_ladder.png
2140x842, dynamic range=255
```
