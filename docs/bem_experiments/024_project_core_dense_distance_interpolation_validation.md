# BEM Experiment 024: Project-Core Dense Distance Interpolation Validation

Date: 2026-06-24

## Purpose

Validate whether the dense direct-wave calibration grid from run `023` can
interpolate source scales across Tx/Rx offset.

This run does not launch a new FDTD solve. It reads run `023`, fits complex
source scales by offset and frequency, and tests held-out offset interpolation.

## Output

```text
outputs/bem_experiments/024_project_core_dense_distance_interpolation_validation
```

Key artifacts:

```text
data/dense_distance_interpolation_summary.json
data/dense_distance_interpolation_offset_metrics.csv
data/dense_distance_interpolation_arrays.npz
figures/dense_distance_interpolation_offset_validation.png
figures/dense_distance_interpolation_scale_surface.png
docs/DENSE_DISTANCE_INTERPOLATION_VALIDATION.md
```

## Result

```text
offset count:                       27
frequency count:                    17
measured table symmetric L2:        0.3347857456839477
leave-one-offset all symmetric L2:  0.42922906860192656
leave-one-offset interior L2:       0.3421182084222686
even/odd train symmetric L2:        0.32997023386089186
even/odd validation symmetric L2:   0.34190295352453876
max even/odd holdout offset L2:     0.4395462783553787
dense interpolation ready:          true
```

## Interpretation

Dense 10 mm direct-wave sampling makes distance-aware interpolation viable
inside the sampled offset range. Endpoint extrapolation remains unreliable,
but interior held-out offsets validate at about the same error level as the
measured per-offset table.

## Decision

Use this dense direct-wave calibration only for interpolation inside the
sampled offset range. Do not extrapolate. The next valid target-side test is a
replay of the homogeneous dielectric target from run `019`.

## Validation

```text
python -m py_compile run_project_core_dense_distance_interpolation_validation.py
conda run -n gpr-fdtd-fwi python run_project_core_dense_distance_interpolation_validation.py
```

Figure check:

```text
2 PNG figures, nonblank dynamic range, dimensions from 1271x759 to 1844x740
```
