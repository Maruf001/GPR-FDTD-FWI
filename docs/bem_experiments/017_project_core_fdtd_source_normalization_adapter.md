# BEM Experiment 017: Project-Core FDTD Source Normalization Adapter

Date: 2026-06-24

## Purpose

Test whether the in-repo project-core 2D TMz FDTD solver can be placed on
the same observable scale as the BEM-owned half-space PEC ladder.

This run uses the project FDTD grid, Ricker source, air/concrete interface,
and single-rebar geometry. It then calibrates the BEM source factor from the
background/direct response only and applies that same source factor to the
BEM rebar-scattered response.

This is a BEM-track bridge gate. It is not a normal `outputs/experiments`
synthetic run, not a field run, and not a field-FWI result.

## Output

```text
outputs/bem_experiments/017_project_core_fdtd_source_normalization_adapter
```

Key artifacts:

```text
data/project_core_fdtd_source_normalization_summary.json
data/project_core_fdtd_source_normalization_frequency_metrics.csv
data/project_core_fdtd_source_normalization_scan_summary.csv
data/project_core_fdtd_source_normalization_arrays.npz
figures/project_core_fdtd_bem_adapter_geometry.png
figures/project_core_fdtd_bem_frequency_diagnostics.png
figures/project_core_fdtd_bem_bscan_comparison.png
figures/project_core_fdtd_bem_mid_trace.png
docs/PROJECT_CORE_FDTD_SOURCE_NORMALIZATION_ADAPTER.md
```

## Result

```text
scan positions:                         7
selected frequency bins:                17
frequency range:                        624772413.7942328 to 2998907586.212318 Hz
BEM panels:                             32
project dx:                             0.002 m
project dt:                             4.245577806149432e-12 s
project NT:                             1885
direct/background relative L2:          0.03170696405248453
scattered spectral symmetric L2:        1.394365162631044
scattered time symmetric L2:            1.3943651626310445
residual best scale |beta|:             0.03133343445177433
project-core FDTD adapter ready:        false
```

The direct/background source calibration is good, but it does not transfer to
the rebar-scattered field. A residual scale of about `0.031` would still be
needed after direct-wave calibration, and even that residual rescale leaves the
time-domain scattered relative L2 near `1.0`.

## Interpretation

The mismatch is not just a source-amplitude problem. The remaining gap likely
comes from one or more of:

- project soft-source injection convention;
- finite-domain/CPML behavior;
- source coupling through the air/concrete interface;
- high-conductivity rebar rasterization on the 2 mm project grid;
- residual convention differences between project FDTD and the scalar BEM
  Green function.

## Decision

Do not promote project-core FDTD/BEM comparison to the older
`outputs/experiments` archive yet. Keep runs `014`-`016` as the validated
BEM-owned 2D ladder and use this run as the project-core bridge gate.

The next useful marathon branch is a factorized project-core diagnostic
ladder: homogeneous dielectric cylinder, homogeneous PEC cylinder, then
half-space PEC with controlled source injection.

## Validation

```text
python -m py_compile run_project_core_fdtd_source_normalization_adapter.py
conda run -n gpr-fdtd-fwi python run_project_core_fdtd_source_normalization_adapter.py
```

Figure check:

```text
4 PNG figures, nonblank dynamic range, dimensions from 1167x731 to 2176x740
```
