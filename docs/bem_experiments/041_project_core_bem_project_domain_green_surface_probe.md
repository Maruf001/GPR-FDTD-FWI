# BEM Experiment 041: Project-Domain Green Surface Probe

Date: 2026-06-25

## Purpose

Record project-core background fields at the actual target cells and test
whether a target-cell Green surface can predict held-out source/receiver scan
positions for the run `038` adapter gate.

This is a CPU-only background-field surface probe. It uses project-core FDTD to
record target-cell background fields, but it does not run new target FDTD, field
data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/041_project_core_bem_project_domain_green_surface_probe
```

Key artifacts:

```text
data/project_core_bem_project_domain_green_surface_probe.csv
data/project_core_bem_project_domain_green_surface_probe_summary.json
figures/project_core_bem_project_domain_green_surface_probe.png
docs/PROJECT_CORE_BEM_PROJECT_DOMAIN_GREEN_SURFACE_PROBE.md
```

## Result

```text
source run:                         outputs/bem_experiments/036_project_core_discrete_born_strength_ladder
cases checked:                      3
surface sample count:               10
target cell count:                  533
selected frequency count:           17
worst exact-surface LOO L2:         0.5621944558984743
worst interpolated-surface LOO L2:  0.5573625471027422
project-domain surface ready:       true
actual background recordings:       10
case recording references:          30
edge extrapolated point count:      4
gpu required:                       false
```

Metrics:

| epsr | Project-grid L2 | Exact surface LOO L2 | Interpolated surface LOO L2 | Best interpolated variant | Ready |
| ---: | ---: | ---: | ---: | --- | --- |
| 1.25 | 0.0989465314024021 | 0.1304685675829604 | 0.47485397997420115 | product_no_div | true |
| 2.0 | 0.23018542478328735 | 0.288343573486278 | 0.499489909063999 | product_div_source | true |
| 4.0 | 0.44601690298659386 | 0.5621944558984743 | 0.5573625471027422 | receiver_conjugate_div_source | true |

## Interpretation

A project-domain target-cell Green surface predicts held-out scan positions
inside the adapter gate. This is the first positive bridge after the
analytic-field failure in runs `039` and `040`.

The BEM-side target operator should couple to a finite-domain/project-grid
field surface rather than raw continuous free-space Green fields when comparing
against this project-core FDTD stream.

## Decision

Use the project-domain target-cell Green surface as the current BEM/project-core
bridge. The next branch should make the surface reusable and stress-test denser
positions, target shifts, and edge extrapolation before any field or 3D claim.

## Validation

```text
python -m py_compile run_project_core_bem_project_domain_green_surface_probe.py
python run_project_core_bem_project_domain_green_surface_probe.py
```

Figure check:

```text
project_core_bem_project_domain_green_surface_probe.png: 1925x769, dynamic range=255
```
