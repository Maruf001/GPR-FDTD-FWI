# BEM Experiment 070: Bempp Minimal 3D Reference Probe

Date: 2026-06-25

## Purpose

Adapt the existing Gmsh-free Bempp finite-cylinder backend to the run `069`
minimal 3D reference geometry.

This run uses the isolated Bempp Python environment for Maxwell solves and the
project environment for tables and figures. It is a homogeneous PEC backend
probe, not a 3D FDTD validation run.

## Output

```text
outputs/bem_experiments/070_project_core_bem_bempp_minimal_3d_reference_probe
```

Key artifacts:

```text
data/project_core_bem_bempp_minimal_3d_reference_frequency_summary.csv
data/project_core_bem_bempp_minimal_3d_reference_receivers.csv
data/project_core_bem_bempp_minimal_3d_reference_mesh_metrics.csv
data/project_core_bem_bempp_minimal_3d_reference_probe_summary.json
figures/project_core_bem_bempp_minimal_3d_reference_probe.png
docs/PROJECT_CORE_BEM_BEMPP_MINIMAL_3D_REFERENCE_PROBE.md
```

## Result

```text
length:                              0.12 m
radius:                              0.01 m
mesh vertices:                       114
mesh elements:                       224
mesh closed:                         true
RWG DOFs:                            336
receiver count:                      31
frequencies checked:                 4
finite all responses:                true
backend reference ready:             true
3D FDTD validation ready:            false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Frequency sweep:

| Frequency GHz | Wavenumber rad/m | Max scattered norm | Mean scattered norm | Finite |
| ---: | ---: | ---: | ---: | --- |
| 0.5 | 25.668754418669145 | 0.021301951596338742 | 0.019743783055616266 | true |
| 1.0 | 51.33750883733829 | 0.09772153342048626 | 0.07775462592604523 | true |
| 1.5 | 77.00626325600741 | 0.19236148010432405 | 0.15292845343367442 | true |
| 3.0 | 154.01252651201483 | 0.307962597331565 | 0.24822098467980308 | true |

## Interpretation

Bempp can solve the run `069` finite-rebar geometry over the selected
concrete-effective wavenumbers and emit a receiver-line response table. This
closes the backend-specific geometry smoke for the proposed 3D reference.

## Decision

Use this as the Bempp-side backend input for a future matched 3D FDTD
comparison.

Do not claim 3D validation, layered 3D GPR readiness, field FWI readiness, or
GPU/HPC readiness until matched gates exist.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_bempp_minimal_3d_reference_probe.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_bempp_minimal_3d_reference_probe.py
pass
```

Figure check:

```text
project_core_bem_bempp_minimal_3d_reference_probe.png
2104x845, dynamic range=255
```
