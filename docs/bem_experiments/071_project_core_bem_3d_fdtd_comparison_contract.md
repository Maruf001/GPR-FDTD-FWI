# BEM Experiment 071: 3D FDTD Comparison Contract

Date: 2026-06-25

## Purpose

Convert the run `070` Bempp finite-rebar receiver table into a matched 3D FDTD
comparison contract.

This run is a design/acceptance artifact. It does not launch 3D FDTD, field
FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/071_project_core_bem_3d_fdtd_comparison_contract
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_comparison_contract.csv
data/project_core_bem_3d_fdtd_comparison_contract_summary.json
figures/project_core_bem_3d_fdtd_comparison_contract.png
docs/PROJECT_CORE_BEM_3D_FDTD_COMPARISON_CONTRACT.md
```

## Result

```text
contract items:                      10
ready items:                         7
partial items:                       1
blocked items:                       2
launch blockers:                     3
frequencies:                         0.5, 1.0, 1.5, 3.0 GHz
receiver count:                      31
matched FDTD contract ready:         true
plane-wave source mismatch:          true
plane-wave FDTD design ready:        true
GPR-like FDTD design ready:          false
3D FDTD launch ready:                false
3D validation claim ready:           false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

Run `070` is sufficient to define a fair backend comparison, but it is not yet a
GPR-like source/receiver comparison. The Bempp reference uses a homogeneous PEC
finite cylinder with a y-polarized plane wave, `Ey = exp(i k z)`.

The first fair 3D FDTD comparison must therefore either:

```text
1. implement the same plane-wave/narrowband incident field in FDTD, or
2. create a new Bempp point/small-dipole source run before comparing to a
   GPR-like FDTD source.
```

The contract also requires target/background FDTD manifests and complex
scattered-field subtraction before any validation claim.

## Decision

Use this as the 3D comparison checklist. Do not launch or claim 3D FDTD
validation until the incident-field convention, scattered-field subtraction,
and paired-run manifests are implemented.

## Validation

Figure check:

```text
2500x808, dynamic range=255
```
