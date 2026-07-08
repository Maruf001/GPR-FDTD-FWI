# BEM Experiment 072: Bempp Dipole Source Probe

Date: 2026-06-25

## Purpose

Resolve the immediate source-convention blocker from run `071` by replacing the
run `070` plane-wave incident field with a GPR-like point/small-dipole proxy in
the Bempp finite-rebar backend.

This is still a homogeneous PEC frequency-domain backend probe. It does not run
3D FDTD, layered 3D GPR, field FWI, GPU/HPC work, or field-data validation.

## Output

```text
outputs/bem_experiments/072_project_core_bem_bempp_dipole_source_probe
```

Key artifacts:

```text
data/project_core_bem_bempp_dipole_source_frequency_summary.csv
data/project_core_bem_bempp_dipole_source_receivers.csv
data/project_core_bem_bempp_dipole_source_mesh_metrics.csv
data/project_core_bem_bempp_dipole_source_probe_summary.json
figures/project_core_bem_bempp_dipole_source_probe.png
docs/PROJECT_CORE_BEM_BEMPP_DIPOLE_SOURCE_PROBE.md
```

## Result

```text
source position:                     [-0.04, 0.0, 0.09] m
dipole moment:                       [0.0, 1.0, 0.0]
mesh vertices/elements:              114 / 224
RWG DOFs:                            336
receiver count:                      31
frequencies checked:                 4
finite all responses:                true
max incident norm range:             1536.7929707311778 to 46579.90809943536
max scattered norm range:            29.513832034532605 to 3373.3467929303047
max receiver-line symmetry error:    20.439382352569737
dipole Bempp reference ready:        true
GPR-like FDTD design ready:          true
3D FDTD validation ready:            false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Frequency sweep:

| Frequency GHz | Max incident norm | Max scattered norm | Peak receiver y | Symmetry error | Finite |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0.5 | 1536.7929707311778 | 29.513832034532605 | 0.0 | 0.0050518058485309325 | true |
| 1.0 | 4745.331274982029 | 331.60945799602325 | 0.0 | 0.026018095838651334 | true |
| 1.5 | 11227.348588335972 | 924.5136920602946 | 0.0 | 0.7236324565594714 | true |
| 3.0 | 46579.90809943536 | 3373.3467929303047 | 0.0 | 20.439382352569737 | true |

## Interpretation

Bempp can solve the finite-rebar reference with a y-oriented point-dipole
incident field and emit the same receiver-line complex response table shape as
the plane-wave run.

This removes the immediate BEM-side source-convention mismatch for a future
GPR-like 3D comparison design. The result is not yet FDTD validation because no
paired FDTD target/background manifests or scattered-field subtraction exist.

## Decision

Use run `072` as the Bempp-side source convention for the next GPR-like FDTD
comparison design.

Do not claim 3D FDTD validation, layered 3D GPR readiness, field FWI readiness,
or GPU/HPC readiness until paired FDTD target/background manifests exist.

## Validation

Figure check:

```text
2500x845, dynamic range=255
```
