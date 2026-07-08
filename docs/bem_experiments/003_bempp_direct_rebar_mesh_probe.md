# BEM Experiment 003: Bempp Direct Rebar Mesh Probe

Date: 2026-06-23

## Purpose

Close the first geometry blocker from run `002` without installing system
Gmsh: construct a finite rebar-like triangular cylinder directly in Python and
solve a minimal time-harmonic Maxwell boundary-integral problem with
`bempp-cl`.

This is a homogeneous PEC-cylinder smoke test. It does not model the
air/concrete interface, concrete dielectric contrast, finite-bandwidth GPR
pulse, antenna coupling, measured field data, inversion, or FDTD
cross-validation.

## Output

```text
outputs/bem_experiments/003_bempp_direct_rebar_mesh_probe
```

Key artifacts:

```text
data/bempp_direct_rebar_mesh_metrics.csv
data/bempp_direct_rebar_mesh.obj
data/bempp_direct_rebar_mesh_probe_summary.json
docs/BEMPP_DIRECT_REBAR_MESH_PROBE.md
run_manifest.json
```

## Result

```text
python:                                  outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python
bempp-cl version:                        0.4.2
length:                                  0.5 m
radius:                                  0.025 m
axial segments:                          4
radial segments:                         12
mesh vertices:                           62
mesh triangles:                          120
unique edges:                            180
boundary edges:                          0
nonmanifold edges:                       0
outward orientation fraction:            1.0
wavenumber:                              8.0 rad/m
RWG DOFs:                                180
coefficient count:                       180
solution norm:                           10.787448040121925
finite solution norm:                    true
direct mesh ready:                       true
Gmsh required:                           false
homogeneous PEC rebar prototype ready:   true
layered GPR forward model ready:         false
BEM/FDTD cross-validation ready:         false
BEM-FWI ready:                           false
```

## Interpretation

The BEM track now has a concrete 3D rebar-like geometry path that does not
depend on Gmsh. `bempp-cl` can assemble and solve a Maxwell RWG system on a
closed finite-cylinder surface mesh generated directly by the project runner.

This changes the blocker from "can we make a 3D rebar mesh?" to "can we make a
physically meaningful GPR forward model and validate it?" The missing pieces
are still substantial: dielectric/background modeling, antenna/source
representation, broadband/time-domain handling, and FDTD cross-validation.

## Decision

Use the direct mesh path for the first homogeneous 3D PEC rebar forward-model
prototype.

Do not treat run `003` as a GPR result, BEM/FDTD validation, or inversion
result. It is only the first geometry-plus-Maxwell assembly proof for the new
BEM track.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bempp_direct_rebar_mesh_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python -m py_compile run_bempp_direct_rebar_mesh_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python run_bempp_direct_rebar_mesh_probe.py --outdir outputs/bem_experiments/003_bempp_direct_rebar_mesh_probe
```

## Next Action

Create the first physics-facing BEM prototype: homogeneous-background PEC
finite rebar scattering with a documented frequency choice and a response
quantity that can later be matched against a small FDTD reference case.
