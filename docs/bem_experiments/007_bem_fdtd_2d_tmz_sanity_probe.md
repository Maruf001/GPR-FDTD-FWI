# BEM Experiment 007: BEM/FDTD 2D TMz Sanity Probe

Date: 2026-06-23

## Purpose

Use the existing in-repo FDTD stack to emit a receiver-line scattered-field
response for a single conductive rebar cross-section.

This experiment is a response-extraction sanity check for the BEM research
track. It is not direct validation of the 3D finite-cylinder Bempp result from
run `004`.

## Output

```text
outputs/bem_experiments/007_bem_fdtd_2d_tmz_sanity_probe
```

Key artifacts:

```text
data/fdtd_2d_tmz_receiver_line_response.csv
data/fdtd_2d_tmz_scattered_traces.csv
data/fdtd_2d_tmz_traces.npz
data/fdtd_2d_tmz_sanity_probe_summary.json
docs/BEM_FDTD_2D_TMZ_SANITY_PROBE.md
run_manifest.json
```

## Result

```text
FDTD dimensionality:                    2D TMz
receiver count:                         21
receiver span x:                        0.3 m
source x:                               0.25 m
source z:                               0.038 m
receiver z:                             0.038 m
rebar x:                                0.25 m
rebar z:                                0.09 m
rebar radius:                           0.006 m
geometry mode:                          subcell
frequency:                              1.5 GHz
nearest FFT bin:                        1499453793.106159 Hz
max |scattered Ez|:                     0.00454917485993519
mean receiver max |scattered Ez|:       0.003235815428463019
peak receiver index:                    10
peak receiver x:                        0.25 m
receiver-line symmetry error:           9.754110195549573e-05
finite response:                        true
response extraction ready:              true
direct validation of 3D Bempp run 004:  false
3D BEM/FDTD validation ready:           false
layered BEM or field claim ready:       false
```

## Interpretation

The current FDTD stack can produce a finite scattered response table for a
single 2D conductive rebar cross-section. The response peaks at the centered
receiver in this symmetric setup, which is the expected basic sanity behavior.

This does not validate the 3D Bempp finite-cylinder result. The models differ
in dimensionality, source representation, background physics, and geometry:

```text
FDTD sanity: 2D TMz, air/concrete, Ricker pulse, circular cross-section.
Bempp run 004: 3D finite PEC cylinder, homogeneous background, plane-wave
               time-harmonic Maxwell response.
```

## Decision

Use run `007` only as an FDTD plumbing and response-extraction checkpoint.

The next validation-facing step is a separate small 3D FDTD reference design
for the run `004` finite-cylinder response contract, or a formally defined 2D
BEM/FDTD comparison problem that both solvers can represent.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bem_fdtd_2d_tmz_sanity_probe.py
python -m py_compile run_bem_fdtd_2d_tmz_sanity_probe.py
conda run -n gpr-fdtd-fwi python run_bem_fdtd_2d_tmz_sanity_probe.py --outdir outputs/bem_experiments/007_bem_fdtd_2d_tmz_sanity_probe
```

## Next Action

Design a true shared comparison problem. The two viable options are:

```text
1. 2D-compatible BEM/FDTD cross-section problem;
2. small 3D FDTD reference for the finite-cylinder Bempp contract.
```
