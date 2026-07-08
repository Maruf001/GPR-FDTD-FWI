# BEM Experiment 225: Half-Space Green-Function Objective Audit

Date: 2026-06-28

## Purpose

Turn the open half-space Green-function gap into a concrete BEM objective
contract.

This run joins the guarded 2D tabulated-surface scaling policy, the 2D-to-3D
alignment audit, the 3D BEM frequency/receiver reference export, and the
optional `scarep` GPU MFS priority audit. It defines what the next half-space
BEM branch must prove before any inversion-scale or 3D validation claim is
allowed.

It does not implement a new half-space kernel, run FDTD, compare against field
data, launch GPU/HPC work, run field FWI, or promote 3D validation.

## Output

```text
outputs/bem_experiments/225_project_core_bem_halfspace_green_function_objective_audit
```

Key artifacts:

```text
data/project_core_bem_halfspace_green_function_objective_rows.csv
data/project_core_bem_halfspace_green_function_objective_stages.csv
data/project_core_bem_halfspace_green_function_candidate_budget.csv
data/project_core_bem_halfspace_green_function_objective_audit_summary.json
figures/project_core_bem_halfspace_green_function_objective_audit.png
docs/PROJECT_CORE_BEM_HALFSPACE_GREEN_FUNCTION_OBJECTIVE_AUDIT.md
```

## Result

```text
objective items:                         11
ready or not-blocking items:             6
half-space objective blockers:           5
objective stages:                        5
candidate budget scenarios:              5
surface policy:                          grid_15mm_only
support mode:                            outer_shell_11mm_binary
samples per candidate:                   13
frequency count:                         9
receiver count:                          31
surface samples for 1000 candidates:     13000
kernel evaluation floor for 1000:        3627000
tabulated scaling policy ready:          true
external 3D request ready:               true
homogeneous 3D BEM reference ready:      true
GPU MFS fix priority:                    low
half-space objective defined:            true
half-space kernel validated:             false
inversion-scale half-space ready:        false
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
field transfer ready:                    false
GPU work ready:                          false
field FWI ready:                         false
```

The current BEM track has ready inputs:

| Ready input | Value |
| --- | --- |
| guarded surface policy | `grid_15mm_only` |
| guarded support mode | `outer_shell_11mm_binary` |
| surface samples per candidate | 13 |
| frequency bins | 9 |
| receivers | 31 |
| external 3D FDTD request gate | ready |
| optional `scarep` GPU MFS repair | low priority |

The blockers are now explicit:

| Blocker | Why it matters |
| --- | --- |
| half-space Green kernel missing | no validated air/concrete interface Green function exists yet |
| source/receiver interface contract missing | source side, receiver side, and component conventions must be fixed |
| homogeneous-limit and interface sanity checks missing | the kernel needs smoke tests before rebar coupling |
| time/frequency observable bridge partial | frequency-domain work must remain separate from field time-domain claims |
| inversion-scale kernel cost unknown | sample count is known, but half-space kernel assembly/solve cost is not measured |

## Interpretation

The BEM path has a guarded local 2D surface-sampling policy and a homogeneous
3D frequency/receiver schema. That is enough to define the next half-space
objective, but not enough to claim a half-space solver.

For 1000 candidate geometries, the current 13-sample policy already implies
13,000 surface samples and a floor of 3,627,000 frequency-receiver-sample
kernel evaluations before dense-matrix assembly or solve overhead. This makes
the half-space kernel itself the next decision-changing piece.

## Decision

Use run `225` to define the next BEM objective: a CPU half-space Green-kernel
smoke with homogeneous-limit recovery and single-interface sanity checks. Do
not promote inversion-scale half-space BEM, real BEM/FDTD comparison, 3D
validation, field transfer, GPU/HPC work, or field FWI until that kernel
objective passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_green_function_objective_audit.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_green_function_objective_audit.py: pass
tests/test_project_core_bem_halfspace_green_function_objective_audit.py: pass
```

Figure check:

```text
project_core_bem_halfspace_green_function_objective_audit.png
3257x891, dynamic range=255
```
