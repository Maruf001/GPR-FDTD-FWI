# BEM Experiment 230: Half-Space Green-Kernel Smoke Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `229` scalar half-space Green-kernel smoke validator.

This run checks whether the validator accepts the exact run `228` smoke result
and rejects controlled damage to kernel shape, homogeneous-limit recovery,
interface trend, finite concrete field, smoke readiness, source objective
readiness, and downstream promotion flags.

It does not implement full 3D Maxwell BEM, compare against FDTD returns,
launch GPU/HPC work, run field FWI, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/230_project_core_bem_halfspace_green_kernel_smoke_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_kernel_smoke_sensitivity_scenarios.csv
data/project_core_bem_halfspace_green_kernel_smoke_sensitivity_summary.json
figures/project_core_bem_halfspace_green_kernel_smoke_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_KERNEL_SMOKE_SENSITIVITY.md
```

## Result

```text
scenarios:                         20
expected pass scenarios:           1
expected failure scenarios:        19
observed pass scenarios:           1
observed failure scenarios:        19
unexpected outcomes:               0
sensitivity ready:                 true
ready for half-space rebar smoke:  true
kernel validated for inversion:    false
inversion-scale half-space ready:  false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The exact smoke result passes. Damaged variants fail as expected:

| Damage family | Example failure modes |
| --- | --- |
| kernel shape | surface sample count drift, proxy count drift |
| homogeneous limit | relative L2 too large, pass flag false |
| interface sanity | permittivity sequence drift, monotonic flag false, transmission magnitude increase |
| concrete field | nonfinite field, zero field norm |
| smoke boundary | smoke not ready, rebar-smoke not ready, inversion promotion |
| source guard | source objective sensitivity not ready |
| downstream states | real BEM/FDTD, 3D validation, field transfer, GPU work, or field FWI marked ready |

## Interpretation

The scalar kernel-smoke validator is guarded against the main ways the smoke
result could drift. It preserves the intended boundary: the scalar half-space
kernel smoke is ready for finite-rebar smoke design, but not for inversion-scale
or 3D validation claims.

## Decision

Use runs `228-230` as the guarded scalar half-space Green-kernel smoke package.
The next BEM task can attempt finite-rebar half-space coupling; inversion-scale
half-space BEM, real BEM/FDTD comparison, 3D validation, field transfer,
GPU/HPC, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_kernel_smoke_sensitivity.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_kernel_smoke_sensitivity.py: pass
tests/test_project_core_bem_halfspace_green_kernel_smoke_sensitivity.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_kernel_smoke_sensitivity.png
3131x894, dynamic range=255
```
