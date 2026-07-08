# BEM Experiment 009: SCUFF-EM Feasibility Probe

Date: 2026-06-23

## Purpose

Assess whether SCUFF-EM can be promoted from an external reference repository
to a locally buildable BEM tool in the current project environment.

This is a build/configuration feasibility probe. It does not run SCUFF-EM
physics examples, GPR modeling, FDTD validation, inversion, field processing,
or heavy GPU work.

## Output

```text
outputs/bem_experiments/009_scuff_em_feasibility_probe
```

Key artifacts:

```text
data/scuff_em_feasibility_checks.csv
data/scuff_em_feasibility_summary.json
docs/SCUFF_EM_FEASIBILITY_PROBE.md
run_manifest.json
```

## Result

```text
repo present:                         true
git head:                             9c6d0cb7695463af803dee8d04cdae939740cdcc
scuff-scatter application present:    true
scuff-rf application present:         true
WireAntenna example present:          true
autogen/configure attempted:          true
autogen/configure ready:              false
missing core tools:                   libtoolize, gfortran
pkg-config BLAS ready:                false
pkg-config LAPACK ready:              false
pkg-config HDF5 ready:                false
SCUFF external reference applicable:  true
SCUFF internal toolchain ready:       false
GPR-BEM dependency ready:             false
```

The conservative autogen/configure smoke used:

```text
sh autogen.sh --prefix=<run-output>/scuff_install --without-hdf5 --without-python --without-openmp
```

It failed before a usable build because the local Autotools/libtool chain is
incomplete and package-discovery evidence for BLAS/LAPACK/HDF5 is missing.

## Interpretation

SCUFF-EM is still applicable to the project as a mature external EM-BEM
reference suite, especially for scattering/RF workflows and examples such as
wire antennas and 2D cylinders.

It should not be added as an internal dependency in the current environment.
The practical blockers are:

```text
1. copyleft licensing review is required;
2. local build tools are incomplete;
3. BLAS/LAPACK/HDF5 discovery is not ready;
4. Gmsh is absent, which limits practical example/mesh workflows.
```

## Decision

Keep SCUFF-EM as an external benchmark/reference tool. Do not make it the first
internal 3D GPR-BEM backend.

`bempp-cl` remains the primary prototype backend. OpenBEM remains the low-level
RWG/PEC formulation reference.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_scuff_em_feasibility_probe.py
python -m py_compile run_scuff_em_feasibility_probe.py
conda run -n gpr-fdtd-fwi python run_scuff_em_feasibility_probe.py --outdir outputs/bem_experiments/009_scuff_em_feasibility_probe
```

## Next Action

Only revisit SCUFF-EM build integration after licensing review and after the
system has `libtoolize`, a Fortran compiler, discoverable BLAS/LAPACK, and a
decided Gmsh/mesh workflow.
