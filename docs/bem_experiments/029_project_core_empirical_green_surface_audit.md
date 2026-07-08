# BEM Experiment 029: Project-Core Empirical Green Surface Audit

Date: 2026-06-25

## Purpose

Test whether the project-core FDTD direct wave is better represented as an
empirical finite-domain source/offset Green surface than as a continuous
homogeneous analytic Green function.

This run reuses the saved no-target direct-wave sweep from run `023`. It does
not run new FDTD simulations, use field data, launch GPU work, run FWI, or
touch the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/029_project_core_empirical_green_surface_audit
```

Key artifacts:

```text
data/project_core_empirical_green_surface_models.csv
data/project_core_empirical_green_surface_offsets.csv
data/project_core_empirical_green_surface_rank1_frequency.csv
data/project_core_empirical_green_surface_summary.json
figures/project_core_empirical_green_surface_audit.png
docs/PROJECT_CORE_EMPIRICAL_GREEN_SURFACE_AUDIT.md
```

## Result

```text
source run:                         outputs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit
source count:                       9
offset count:                       27
pair count:                         243
frequency count:                    17
coarse validation pair count:       173
analytic Green L2:                  1.6206668574552767
offset-mean empirical L2:           0.3347857456839478
leave-one-source empirical L2:      0.3764644678142781
rank-1 empirical L2:                0.25970063183964165
rank-1 mean energy fraction:        0.938023042083028
rank-1 minimum energy fraction:     0.8494667777038681
coarse-grid validation L2:          0.13204235679778975
empirical Green surface ready:      true
```

## Interpretation

This is the first positive project-core bridge result after the failed analytic
direct-wave sequence. The continuous homogeneous Green function fails badly on
the direct wave, but the project-core direct-wave response is smooth as an
empirical source/offset surface.

The important distinction:

```text
Analytic Green function:      not a transferable direct-wave model.
Empirical FDTD Green surface: transferable inside the sampled source/offset range.
```

The result does not make BEM/FDTD target scattering ready by itself. It says
the next bridge attempt should stop forcing an analytic continuous-space Green
function onto the project-core solver and should instead use a measured
finite-domain direct-wave baseline.

## Decision

Use this run as the current BEM/project-core direct-wave checkpoint. The next
defensible BEM work is a controlled scattered-field ladder built on this
empirical baseline:

```text
no target
weak dielectric cylinder
stronger dielectric cylinder
PEC cylinder
```

Do not yet compare BEM to the historical `outputs/experiments` archive as a
claim. Do not escalate to field FWI, 3D inversion, or heavy GPU work from this
run.

## Validation

```text
python -m py_compile run_project_core_empirical_green_surface_audit.py
python run_project_core_empirical_green_surface_audit.py
```

Figure check:

```text
project_core_empirical_green_surface_audit.png: 2356x752, dynamic range=255
```
