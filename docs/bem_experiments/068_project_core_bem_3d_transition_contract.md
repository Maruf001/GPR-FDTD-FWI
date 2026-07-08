# BEM Experiment 068: 3D Transition Contract

Date: 2026-06-25

## Purpose

Define the gates required before the 2D BEM work can be lifted toward a
finite-rebar 3D BEM claim.

The run `067` replacement contract makes the 2D state clear. This run defines
what remains missing for 3D, field transfer, and any FWI/GPU/HPC escalation.

## Output

```text
outputs/bem_experiments/068_project_core_bem_3d_transition_contract
```

Key artifacts:

```text
data/project_core_bem_3d_transition_contract.csv
data/project_core_bem_3d_transition_contract_summary.json
figures/project_core_bem_3d_transition_contract.png
docs/PROJECT_CORE_BEM_3D_TRANSITION_CONTRACT.md
```

## Result

```text
requirements:                       10
partial requirements:               4
blocked requirements:               6
3D transition ready:                false
field transfer ready:               false
3D BEM claim ready:                 false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Blocked requirements include finite-rebar geometry, 3D Maxwell boundary
unknowns, source/receiver modeling, a matched 3D FDTD reference, field transfer
gate, and GPU/HPC policy.

Partial requirements include the layered background model, frequency-to-time
synthesis, backend selection, and numerical gate definition.

## Interpretation

The 2D BEM work is now strong enough to define a 3D transition contract, but
not to claim 3D readiness. The main missing pieces are finite-rebar geometry,
3D Maxwell unknowns, source/receiver modeling, and a matched 3D FDTD reference.

## Decision

Use this as the 3D lift checklist.

Do not launch 3D/FWI/GPU/HPC from the 2D BEM contract alone.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_3d_transition_contract.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_3d_transition_contract.py
pass
```

Figure check:

```text
project_core_bem_3d_transition_contract.png
1924x806, dynamic range=255
```
