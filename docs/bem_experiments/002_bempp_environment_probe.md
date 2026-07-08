# BEM Experiment 002: Bempp Environment Probe

Date: 2026-06-23

## Purpose

Create an isolated `bempp-cl` environment without changing the existing
`gpr-fdtd-fwi` conda environment, then test whether the preferred Python BEM
backend can run a minimal Maxwell solve.

This is a backend readiness probe. It does not run GPR FDTD, FWI, field FWI,
3D/HPC field work, or neural-network training.

## Output

```text
outputs/bem_experiments/002_bempp_environment_probe
```

Key artifacts:

```text
data/bempp_environment_checks.csv
data/bempp_environment_probe_summary.json
docs/BEMPP_ENVIRONMENT_PROBE.md
run_manifest.json
```

The isolated virtual environment is local and ignored:

```text
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312
```

## Result

```text
python:                                  outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python
bempp-cl version:                        0.4.2
numpy version:                           2.4.6
scipy version:                           1.18.0
numba version:                           0.65.1
meshio version:                          5.3.5
import ready:                            true
Gmsh-backed screen mesh ready:           false
Gmsh blocker:                            RuntimeError: Gmsh is not found. Cannot generate mesh
Maxwell regular-sphere smoke ready:      true
regular sphere elements:                 32
regular sphere vertices:                 18
RWG DOFs:                                48
coefficient count:                       48
solution norm:                           7.7408573921293
minimal bempp forward prototype ready:   true
custom GPR geometry ready:               false
BEM/FDTD cross-validation ready:         false
BEM-FWI ready:                           false
```

## Interpretation

The Python BEM backend is viable in isolation. The main project conda
environment is still untouched, while the ignored venv can import `bempp-cl`
and run a small time-harmonic Maxwell solve using the built-in
`regular_sphere` mesh.

The immediate blocker is geometry. Bempp's built-in `screen` and other
Gmsh-backed shape generators cannot run here because no Gmsh binary/module is
available, and the pip `gmsh` wheel is not available for this ARM/aarch64
environment.

This means the next BEM experiment should not be inversion or FDTD comparison.
It should close mesh generation/import first.

## Decision

Use the isolated bempp-cl environment as the current Python BEM sandbox.

Do not attach Bempp to GPR validation or inversion until one of these geometry
paths is working:

```text
1. install a system Gmsh binary/package visible to the BEM venv;
2. generate cylinder/rebar meshes externally and import them through meshio;
3. create minimal triangle meshes directly for simple canonical shapes.
```

## Validation

Commands run:

```text
python -m venv outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python -m pip install outputs/bem_experiments/_external_repos/bempp-cl
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python -m py_compile run_bempp_environment_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python run_bempp_environment_probe.py --outdir outputs/bem_experiments/002_bempp_environment_probe
```

## Next Action

Create BEM experiment `003` for mesh geometry closure. The cleanest path is to
probe system-package Gmsh availability first. If system Gmsh is not acceptable,
use mesh import or direct triangle mesh construction for the first finite-rebar
prototype.
