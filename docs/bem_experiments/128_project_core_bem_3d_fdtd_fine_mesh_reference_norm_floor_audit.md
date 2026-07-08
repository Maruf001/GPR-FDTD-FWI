# BEM Experiment 128: Fine-Mesh Reference Norm Floor Audit

Date: 2026-06-27

## Purpose

Audit the fine-mesh BEM scattered-reference norms used by the preferred
nine-frequency BEM/FDTD comparator.

Runs `126` and `127` tested comparator mismatch behavior and threshold
boundaries. This run checks whether any scattered-reference rows have
near-zero norms that would make the per-row relative-L2 metric numerically
unstable.

This is a BEM-side numerical-stability audit. It does not install real FDTD
returns, run local 3D FDTD, make a 3D validation claim, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/128_project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_reference_norm_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_reference_norm_frequency_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_REFERENCE_NORM_FLOOR_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
reference rows:                         279
frequency count:                        9
receiver count:                         31
reference norm floor:                   1e-08
min reference scattered norm:           8.80585591190322
median reference scattered norm:        532.4901521301958
max reference scattered norm:           3175.0846927061107
low-norm row count:                     0
max background/scatter ratio:           107.16891488389032
median background/scatter ratio:        11.043776398231369
background bias fraction at threshold:  0.0009331063966481576
relative metric numerically stable:     true
real FDTD data ready:                   false
real BEM/FDTD comparison ready:         false
3D validation claim ready:              false
gpu/hpc ready:                          false
```

Frequency summary:

| Frequency Hz | Min reference norm | Max background/scatter ratio | Low-norm rows |
| ---: | ---: | ---: | ---: |
| 400000000.0 | 8.80585591190322 | 107.16891488389032 | 0 |
| 500000000.0 | 20.2083311038556 | 53.3506611239595 | 0 |
| 750000000.0 | 86.81887365482504 | 20.59304145432981 | 0 |
| 1000000000.0 | 221.859517354709 | 14.204880006851845 | 0 |
| 1250000000.0 | 413.3685479166413 | 12.549887369123097 | 0 |
| 1500000000.0 | 645.0627116872431 | 12.103522829489215 | 0 |
| 2000000000.0 | 1362.2199167809101 | 10.925919666503319 | 0 |
| 2500000000.0 | 2085.531393070759 | 13.909859882068472 | 0 |
| 3000000000.0 | 2512.0420015598343 | 14.670445864464646 | 0 |

## Interpretation

The fine-mesh scattered-reference rows are safely above the numerical norm
floor. The per-row relative-L2 comparator is therefore not being dominated by
near-zero reference vectors.

The maximum background/scatter ratio is about `107`, concentrated at the lowest
frequency. This explains why run `127` found that a background-only incident
field bias of roughly `0.001` can trip the strict `0.1` relative-L2 threshold.

## Decision

Keep the preferred comparator threshold usable as an investigation gate for
future returned FDTD files. Real comparison and 3D validation remain blocked
until those files pass the real preflight.

## Validation

Focused test:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit.png
2860x845, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit.py
sha256=3d2ff04dad89e3ce791d78575fe50c2bd877385885f3d19fb7fc2445f44fffcc

tests/test_project_core_bem_3d_fdtd_fine_mesh_reference_norm_floor_audit.py
sha256=77de4222d703799e97687ac2346cdf5707d14eadd942164c0699d6d35b81365e
```
