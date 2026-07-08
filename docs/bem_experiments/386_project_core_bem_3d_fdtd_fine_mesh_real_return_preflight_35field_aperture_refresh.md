# BEM Experiment 386: Fine-Mesh Real-Return Preflight 35-Field Aperture Refresh

Date: 2026-06-29

## Purpose

Refresh the preferred nine-frequency external FDTD return preflight so it uses
the 35-field aperture-aware metadata template from runs `383-385`.

This run does not stage returned FDTD data, run BEM/FDTD comparison, make a 3D
validation claim, use field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/386_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh
```

## Result

```text
expected frequencies:                     9
expected receivers:                       31
expected rows per frequency file:         279
full metadata fields:                     35
required metadata fields:                 34
blocking metadata fields:                 34
fine-mesh addendum fields:                5
receiver-aperture addendum fields:        5
preflight checks:                         10
blocking failures:                        10
target file present:                      false
background file present:                  false
metadata file present:                    false
BEM reference export ready:               true
synthetic sensitivity behaves expected:   true
receiver-aperture metadata required:      true
receiver-aperture operator required:      true
real return preflight ready:              false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
```

The refreshed preflight fails closed because the current pending return folder
does not contain the required target frequency file, background frequency file,
or metadata ledger. The metadata failure now expects 34 required keys,
including the five receiver-aperture fields.

## Decision

Use run `386` as the current preferred nine-bin real-return gate. Real BEM/FDTD
comparison and 3D validation remain blocked until all target, background, and
aperture-aware metadata checks pass.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh.py
3 passed
```

Figure check:

```text
2680x846, dynamic range=255
```
