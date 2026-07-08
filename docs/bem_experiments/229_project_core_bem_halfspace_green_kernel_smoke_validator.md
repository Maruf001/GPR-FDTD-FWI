# BEM Experiment 229: Half-Space Green-Kernel Smoke Validator

Date: 2026-06-28

## Purpose

Validate the run `228` scalar half-space Green-kernel smoke from a consumer
perspective.

This run checks whether the smoke result has the expected 13-by-31-by-9 shape,
passes the homogeneous-limit threshold, preserves the interface transmission
trend, keeps the concrete half-space field finite and nonzero, and maintains
the boundary between smoke readiness and inversion/3D readiness.

It does not implement full 3D Maxwell BEM, compare against FDTD returns,
launch GPU/HPC work, run field FWI, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/229_project_core_bem_halfspace_green_kernel_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_kernel_smoke_validation_checks.csv
data/project_core_bem_halfspace_green_kernel_smoke_validator_summary.json
figures/project_core_bem_halfspace_green_kernel_smoke_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_KERNEL_SMOKE_VALIDATOR.md
```

## Result

```text
validation checks:                  7
validation passes:                  7
blocking failures:                  0
validation ready:                   true
kernel evaluation floor proxy:      3627
homogeneous limit relative L2:      1.3693101062433268e-16
ready for half-space rebar smoke:   true
kernel validated for inversion:     false
inversion-scale half-space ready:   false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms:

| Check | Result |
| --- | --- |
| kernel shape matches the objective contract | pass |
| homogeneous-limit relative L2 is below `1e-10` | pass |
| interface transmission decreases across `epsr=1,4,6,9` | pass |
| concrete half-space field is finite and nonzero | pass |
| smoke readiness does not promote inversion readiness | pass |
| source objective guard is ready | pass |
| real comparison, 3D, field transfer, GPU, and field FWI remain blocked | pass |

## Interpretation

The scalar half-space kernel smoke is internally consistent. Shape,
homogeneous-limit recovery, interface trend, finite concrete field, and
downstream no-go states all agree with the run `228` summary.

## Decision

Use run `229` as the consumer validator for the scalar kernel smoke.
Sensitivity remains required before treating the smoke result as guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_kernel_smoke_validator.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_kernel_smoke_validator.py: pass
tests/test_project_core_bem_halfspace_green_kernel_smoke_validator.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_kernel_smoke_validator.png
2465x840, dynamic range=255
```
