# BEM Experiment 228: Half-Space Green-Kernel Smoke

Date: 2026-06-28

## Purpose

Run the first executable half-space Green-function smoke from the guarded
objective package in runs `225-227`.

This run uses the existing scalar two-layer Sommerfeld-style helper to check
two basic mathematical properties:

```text
1. The two-layer formulation recovers the homogeneous limit when both media match.
2. The normal-incidence transmission magnitude decreases as lower half-space permittivity increases.
```

It does not implement full 3D Maxwell BEM, compare against FDTD returns,
launch GPU/HPC work, run field FWI, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/228_project_core_bem_halfspace_green_kernel_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_kernel_homogeneous_limit.csv
data/project_core_bem_halfspace_green_kernel_interface_sanity.csv
data/project_core_bem_halfspace_green_kernel_shape.csv
data/project_core_bem_halfspace_green_kernel_smoke_arrays.npz
data/project_core_bem_halfspace_green_kernel_smoke_summary.json
figures/project_core_bem_halfspace_green_kernel_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_KERNEL_SMOKE.md
```

## Result

```text
source objective sensitivity ready:       true
surface samples:                          13
target points:                            31
frequency count:                          9
kernel evaluation floor proxy:            3627
homogeneous limit relative L2:            1.3693101062433268e-16
homogeneous limit pass:                   true
interface transmission monotonic:         true
concrete field finite:                    true
concrete field norm:                      435.4965107539862
half-space kernel smoke ready:            true
ready for half-space rebar smoke:         true
kernel validated for inversion:           false
inversion-scale half-space ready:         false
real BEM/FDTD comparison ready:           false
3D validation ready:                      false
field transfer ready:                     false
GPU work ready:                           false
field FWI ready:                          false
```

Homogeneous-limit recovery:

| Quantity | Value |
| --- | ---: |
| relative L2 | `1.3693101062433268e-16` |
| maximum absolute difference | `5.178925639311149e-15` |
| pass threshold | `1e-10` |

Single-interface sanity:

| Lower relative permittivity | Mean normal-incidence transmission magnitude |
| ---: | ---: |
| 1 | 1.0 |
| 4 | 0.6666666666666666 |
| 6 | 0.5797958971132713 |
| 9 | 0.5 |

## Interpretation

The scalar half-space kernel smoke passes the basic mathematical checks. The
two-layer formulation recovers the homogeneous limit to numerical precision,
the interface transmission trend is physically ordered, and the concrete
half-space field is finite and nonzero.

This is an important BEM step because it moves the half-space branch from
objective definition to executable kernel evidence. It remains scalar
two-layer evidence, not full 3D Maxwell BEM validation.

## Decision

Use run `228` as a scalar kernel smoke. The next BEM task can couple this
half-space incident field to a finite-rebar smoke. Keep inversion-scale
half-space BEM, real BEM/FDTD comparison, 3D validation, field transfer,
GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_kernel_smoke.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_kernel_smoke.py: pass
tests/test_project_core_bem_halfspace_green_kernel_smoke.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_kernel_smoke.png
2967x845, dynamic range=255
```
