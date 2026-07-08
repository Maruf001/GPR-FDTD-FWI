# BEM Experiment 306: Bempp Fine-Mesh FDTD Archive Paired Proxy Comparator Smoke

Date: 2026-06-28

## Purpose

Compare the guarded 2D scalar proxy scattered amplitudes from run `303` with
the 3D Bempp scattered-reference vector norms from run `117` as a
plumbing-only diagnostic.

This run tests receiver/frequency alignment and shape-comparison plumbing. It
does not create calibrated amplitude agreement, accepted run `293` evidence,
real BEM/FDTD comparison, 3D validation, field transfer, GPU/HPC readiness, or
field FWI readiness.

## Output

```text
outputs/bem_experiments/306_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_receiver_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_frequency_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_PAIRED_PROXY_COMPARATOR_SMOKE.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
receiver comparison rows:             279
frequency rows:                       9
scale factor min:                     6.386344e+13
scale factor max:                     8.685178e+15
scale factor span:                    135.996
scale-fit relative L2 min:            0.0651004
scale-fit relative L2 max:            0.370017
scale-fit relative L2 mean:           0.138495
shape marker frequency count:         7 / 9
proxy comparator smoke ready:         true
raw amplitude comparison ready:       false
scale calibration ready:              false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
field FWI ready:                      false
```

## Interpretation

The proxy pair can exercise comparator plumbing and receiver/frequency
alignment. After per-frequency scale fitting, seven of nine frequencies are
below the 0.15 diagnostic shape marker. The 0.4 GHz and 3.0 GHz bins remain
above that marker.

The raw amplitude scale is not comparable. The best-fit scale factor is very
large and frequency dependent, spanning about 136x across the nine frequency
bins. This confirms that the result is a diagnostic proxy-comparator smoke, not
a calibrated physical BEM/FDTD comparison.

## Decision

Use run `306` as a proxy-comparator smoke only. It supports a future validator
and sensitivity test for the diagnostic path, while accepted run `293`
evidence, real BEM/FDTD comparison, 3D validation, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_smoke.py
3 passed
```

Figure validation:

```text
3184x880, dynamic range=255
```
