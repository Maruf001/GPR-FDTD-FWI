# BEM Experiment 309: Bempp Fine-Mesh FDTD Archive Proxy Comparator Anatomy Audit

Date: 2026-06-28

## Purpose

Audit where the guarded run `306-308` proxy-comparator mismatch lives across
frequency, receiver offset, and 3D BEM vector components.

This run uses saved artifacts only. It does not run FDTD, run a new BEM solve,
calibrate amplitude agreement, accept run `293` evidence, validate 3D physics,
transfer to field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/309_project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_anatomy_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_frequency_anatomy.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_receiver_anatomy.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_anatomy_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_anatomy_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                         9
receiver anatomy rows:                   279
shape-marker pass count:                 7
shape-marker failure count:              2
shape-failure frequencies:               0.4 GHz, 3.0 GHz
minimum shape correlation:               0.398760
median shape correlation:                0.786798
scale-factor span:                       135.996093
maximum edge/center residual ratio:      6.949773
minimum dominant component fraction:     0.798881
mean dominant component fraction:        0.842630
scale-only explanation supported:        false
scalar proxy vector limit detected:      true
component-aware source/operator audit:   true
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
field FWI ready:                         false
```

Per-frequency anatomy:

| Frequency GHz | Fit L2 | Shape correlation | Edge/center residual | Dominant component | Dominant fraction | Diagnostic class |
| ---: | ---: | ---: | ---: | --- | ---: | --- |
| 0.4 | 0.3700 | 0.4457 | 2.4294 | Ey | 0.8361 | receiver shape mismatch |
| 0.5 | 0.0963 | 0.8865 | 1.0863 | Ey | 0.8491 | shape marker pass |
| 0.75 | 0.1106 | 0.7868 | 2.6381 | Ey | 0.8602 | shape marker pass |
| 1.0 | 0.0651 | 0.8925 | 2.4404 | Ey | 0.8607 | shape marker pass |
| 1.25 | 0.0955 | 0.6206 | 0.7744 | Ey | 0.8544 | shape marker pass |
| 1.5 | 0.1051 | 0.3988 | 1.1082 | Ey | 0.8416 | shape marker pass |
| 2.0 | 0.0889 | 0.4317 | 1.4985 | Ey | 0.8428 | shape marker pass |
| 2.5 | 0.1335 | 0.9135 | 2.3988 | Ey | 0.8399 | shape marker pass |
| 3.0 | 0.1814 | 0.8160 | 6.9498 | Ey | 0.7989 | receiver shape mismatch |

## Interpretation

The mismatch is not explained by one global scale. The proxy branch still has
two frequency-local shape failures, a scale-factor span of about `136x`, and a
3D Bempp scattered field that is mostly `Ey` but still has a meaningful
non-`Ey` vector component contribution. The `3.0 GHz` failure is especially
edge-localized.

This points toward a source/operator/component mismatch rather than a simple
scalar rescaling problem.

## Decision

Use run `309` to motivate a component-aware source/operator diagnostic before
any calibrated BEM/FDTD agreement claim. Keep real BEM/FDTD comparison, 3D
validation, field transfer, GPU/HPC readiness, and field FWI blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_proxy_comparator_anatomy_audit.py
4 passed
```

Figure validation:

```text
2850x1523, dynamic range=255
```
