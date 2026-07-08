# BEM Experiment 001: Repository Landscape

Date: 2026-06-23

## Purpose

Open a separate BEM research track and assess the three repositories proposed
for lifting verified 2D GPR-BEM work toward 3D:

```text
https://github.com/homerreid/scuff-EM
https://github.com/bempp/bempp-cl
https://github.com/shash-sharma/OpenBEM
```

This run is a repository and environment-readiness audit. It does not run GPR
FDTD, FWI, field FWI, 3D/HPC field work, or neural-network training.

## Output

```text
outputs/bem_experiments/001_bem_repository_landscape
```

Key artifacts:

```text
data/bem_repository_landscape.csv
data/bem_repository_probe_status.csv
data/bem_repository_landscape_summary.json
docs/BEM_REPOSITORY_LANDSCAPE.md
run_manifest.json
openbem_build/
```

The external repository snapshots are stored locally under:

```text
outputs/bem_experiments/_external_repos/
```

They are intentionally ignored by Git.

## Repository Snapshots

| Repository | Local commit | Local size | License | Current role |
| --- | --- | ---: | --- | --- |
| `bempp-cl` | `a1eaaef9f96b9dd3d7c56b076740e06852a6e1c0` | 173541 KB | MIT | Primary Python prototype candidate. |
| `scuff-em` | `9c6d0cb7695463af803dee8d04cdae939740cdcc` | 122319 KB | GPL-2.0/GPL-3.0 | Mature external EM-BEM reference/tool. |
| `OpenBEM` | `edf98d17a4cad886c8ecda06d90e1919c92b06aa` | 25921 KB | GPL-3.0-or-later | Low-level RWG formulation reference. |

## Result

```text
repository count:                     3
candidate primary backend:            bempp-cl
candidate reference framework:        OpenBEM
external mature tool reference:       SCUFF-EM
bempp import ready:                   false
bempp missing dependencies:           numba;meshio
OpenBEM CMake configure ready:        true
OpenBEM ex01 build/run ready:         true
OpenBEM ex01 relative error:          2.44438 %
OpenBEM ex02 build/run ready:         true
OpenBEM ex02 relative error:          0.00412125 %
SCUFF-EM build attempted:             false
internal BEM prototype ready:         false
3D GPR-BEM claim ready:               false
BEM/FDTD cross-validation ready:      false
BEM-FWI ready:                        false
```

## Applicability

`bempp-cl` is the most applicable first backend. It is Python-first, MIT
licensed, and includes Maxwell/Helmholtz operators plus Maxwell examples for
PEC screens and dielectric scatterers. The current project environment simply
does not yet include its required `numba` and `meshio` dependencies.

`OpenBEM` is technically strong for low-level electromagnetic BEM research. It
has RWG-based TEFIE/NMFIE/TMFIE/NMFIE components, Gmsh mesh handling, plane-wave
excitations, and near/far-field projection. It built and ran its sphere PEC
examples locally. However, it is not a turnkey solver, has no Python bindings
yet, and is GPL-3+, so it should be treated as a formulation reference unless
licensing is approved.

`SCUFF-EM` is a mature external EM-BEM suite with scattering/RF/wire-antenna
examples and command-line applications. Its technical scope is relevant, but
the GPL license and heavier Autotools/C++ integration path make it a reference
and benchmark tool rather than the first code dependency.

## Decision

Start the BEM track in parallel with FDTD:

```text
BEM first target:       bempp-cl environment and minimal Maxwell smoke.
BEM reference target:   OpenBEM RWG/PEC formulation notes.
External benchmark:     SCUFF-EM examples after licensing/tooling review.
Validation anchor:      existing FDTD 2D/3D cases.
```

Do not claim a 3D GPR-BEM capability, BEM/FDTD agreement, or BEM-driven
inversion yet. The next defensible step is environment prep and a minimal
bempp-cl Maxwell reproduction.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bem_repository_landscape.py
conda run -n gpr-fdtd-fwi python run_bem_repository_landscape.py --outdir outputs/bem_experiments/001_bem_repository_landscape --run-openbem-smoke
```

OpenBEM smoke:

```text
ex01: TEFIE vs NMFIE RCS maximum relative error = 2.44438 %
ex02: CFIE vs TEFIE RCS maximum relative error = 0.00412125 %
```

## Next Action

Create BEM experiment `002` for a bempp-cl environment/installability probe.
If dependencies install cleanly, reproduce a minimal Maxwell example and save a
small numerical/figure artifact. If not, isolate the BEM environment from the
existing `gpr-fdtd-fwi` environment rather than destabilizing the current FDTD
workflow.
