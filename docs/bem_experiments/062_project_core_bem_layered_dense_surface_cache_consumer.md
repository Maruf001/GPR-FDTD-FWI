# BEM Experiment 062: Layered Dense Surface Cache Consumer

Date: 2026-06-25

## Purpose

Smoke-test the run `061` layered dense-surface cache as a reusable input for
future layered BEM experiments.

This run loads the cached surface and replays the layered interpolation gate
without rerunning FDTD background field recording.

## Output

```text
outputs/bem_experiments/062_project_core_bem_layered_dense_surface_cache_consumer
```

Key artifacts:

```text
data/project_core_bem_layered_dense_surface_cache_consumer.csv
data/project_core_bem_layered_dense_surface_cache_consumer_summary.json
figures/project_core_bem_layered_dense_surface_cache_consumer.png
docs/PROJECT_CORE_BEM_LAYERED_DENSE_SURFACE_CACHE_CONSUMER.md
```

## Result

```text
cache validation findings:          0
cache load seconds:                 0.01241654809564352
surface shape:                      19x533x17
best all-scan L2:                   0.5220233499204818
best exact-surface LOO L2:          0.619762715748986
best interpolated-surface LOO L2:   0.697021169360853
edge extrapolated points:           0
cache replay ready:                 true
```

## Interpretation

The run `061` layered dense-surface cache loads cleanly and reproduces the
layered interpolated replay gate without rerunning FDTD field recording.

This gives the layered branch a reusable tabulated-surface consumer path. It
does not solve the missing analytic layered Green function problem, but it does
make future layered diagnostics cheaper and less error-prone.

## Decision

Use the cache consumer path for future layered tabulated-surface experiments.

This remains a 2D project-core surrogate path, not a field, 3D, FWI, GPU, or
historical `outputs/experiments` archive claim.

## Validation

Focused tests:

```text
tests/test_bem_layered_surface_cache.py
3 passed
```

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile bem_layered_surface_cache.py run_project_core_bem_layered_dense_surface_cache_consumer.py tests/test_bem_layered_surface_cache.py
pass
```

Figure check:

```text
project_core_bem_layered_dense_surface_cache_consumer.png
1924x792, dynamic range=255
```
