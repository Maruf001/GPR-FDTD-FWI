# BEM Experiment 227: Half-Space Green-Function Objective Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `226` half-space Green-function objective validator.

This run checks whether the validator accepts the exact run `225` objective
contract and rejects controlled damage to objective counts, blockers, the first
executable kernel-smoke stage, the candidate-sweep cost proxy, guarded input
readiness, GPU priority, and downstream promotion flags.

It does not implement a new half-space kernel, run FDTD, compare against field
data, launch GPU/HPC work, run field FWI, or promote 3D validation.

## Output

```text
outputs/bem_experiments/227_project_core_bem_halfspace_green_function_objective_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_function_objective_sensitivity_scenarios.csv
data/project_core_bem_halfspace_green_function_objective_sensitivity_summary.json
figures/project_core_bem_halfspace_green_function_objective_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_FUNCTION_OBJECTIVE_SENSITIVITY.md
```

## Result

```text
scenarios:                         28
expected pass scenarios:           1
expected failure scenarios:        27
observed pass scenarios:           1
observed failure scenarios:        27
unexpected outcomes:               0
sensitivity ready:                 true
half-space kernel validated:       false
inversion-scale half-space ready:  false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The exact objective contract passes. Damaged variants fail as expected:

| Damage family | Example failure modes |
| --- | --- |
| objective shape | item-count drift, blocker-count drift, stage-count drift, budget-count drift |
| blocker semantics | half-space kernel not blocking, kernel marked ready, source contract not blocking |
| first executable stage | homogeneous-limit smoke not executable, stage order drift |
| cost proxy | 1000-candidate surface-sample drift, kernel-evaluation proxy drift |
| false promotion | kernel validated, inversion-scale half-space ready |
| guarded inputs | sample count, frequency count, receiver count, policy readiness drift |
| GPU priority | optional GPU MFS priority changed or GPU work marked ready |
| downstream states | real BEM/FDTD comparison, 3D validation, field transfer, or field FWI marked ready |

## Interpretation

The half-space objective validator is guarded against the main ways the
objective contract could drift. It preserves the intended next step: validate a
CPU half-space Green-function kernel before any inversion-scale or 3D
validation promotion.

## Decision

Use runs `225-227` as the guarded BEM half-space Green-function objective
package. The next executable BEM task is a CPU half-space Green-kernel smoke;
inversion-scale half-space BEM, real BEM/FDTD comparison, 3D validation, field
transfer, GPU/HPC, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_function_objective_sensitivity.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_function_objective_sensitivity.py: pass
tests/test_project_core_bem_halfspace_green_function_objective_sensitivity.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_function_objective_sensitivity.png
3329x896, dynamic range=255
```
