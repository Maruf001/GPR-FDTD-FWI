# BEM Experiment 226: Half-Space Green-Function Objective Validator

Date: 2026-06-28

## Purpose

Validate the run `225` half-space Green-function objective audit from a
consumer perspective.

This run checks whether the objective contract has the right counts, guarded
inputs, explicit kernel blockers, first executable stage, candidate-sweep cost
proxy, and downstream no-go states.

It does not implement a new half-space kernel, run FDTD, compare against field
data, launch GPU/HPC work, run field FWI, or promote 3D validation.

## Output

```text
outputs/bem_experiments/226_project_core_bem_halfspace_green_function_objective_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_function_objective_validation_checks.csv
data/project_core_bem_halfspace_green_function_objective_validator_summary.json
figures/project_core_bem_halfspace_green_function_objective_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_FUNCTION_OBJECTIVE_VALIDATOR.md
```

## Result

```text
validation checks:                       8
validation passes:                       8
blocking failures:                       0
validation ready:                        true
objective items:                         11
half-space blockers:                     5
1000-candidate kernel floor proxy:       3627000
half-space kernel validated:             false
inversion-scale half-space ready:        false
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
field transfer ready:                    false
GPU work ready:                          false
field FWI ready:                         false
```

The validator confirms:

| Check | Result |
| --- | --- |
| objective counts match the run `225` summary | pass |
| guarded 2D policy, 3D request, and homogeneous BEM reference are ready | pass |
| kernel, source-contract, and sanity-check blockers are explicit | pass |
| homogeneous-limit kernel smoke is the first executable stage | pass |
| 1000-candidate proxy cost is 3,627,000 kernel evaluations | pass |
| objective is defined while kernel and inversion-scale readiness remain false | pass |
| optional `scarep` GPU MFS repair remains low priority | pass |
| real comparison, 3D validation, field transfer, and field FWI remain blocked | pass |

## Interpretation

The half-space objective contract is internally consistent. It defines the next
kernel-smoke stage and preserves the five blocking gaps that prevent
inversion-scale half-space BEM or 3D validation.

## Decision

Use run `226` as the consumer validator for run `225`. Sensitivity remains
required before treating the half-space objective contract as guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_function_objective_validator.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_function_objective_validator.py: pass
tests/test_project_core_bem_halfspace_green_function_objective_validator.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_function_objective_validator.png
2645x841, dynamic range=255
```
