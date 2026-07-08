# BEM Experiment 004: Bempp Rebar Receiver Response Probe

Date: 2026-06-23

## Purpose

Convert the direct finite-rebar Bempp smoke from run `003` into a sampled
receiver-line response. This creates a concrete data contract for a later
BEM/FDTD comparison: receiver coordinates, complex incident field, complex
scattered field, scattered norm, and total-field norm.

This is still a homogeneous PEC frequency-domain probe. It does not model
layered concrete/air physics, a broadband GPR pulse, antenna coupling,
measured field data, inversion, or FDTD validation.

## Output

```text
outputs/bem_experiments/004_bempp_rebar_receiver_response_probe
```

Key artifacts:

```text
data/bempp_rebar_receiver_response.csv
data/bempp_rebar_receiver_response_summary.json
docs/BEMPP_REBAR_RECEIVER_RESPONSE_PROBE.md
run_manifest.json
```

## Result

```text
python:                                      outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python
bempp-cl version:                            0.4.2
length:                                      0.5 m
radius:                                      0.025 m
mesh triangles:                              120
RWG DOFs:                                    180
wavenumber:                                  8.0 rad/m
receiver count:                              41
receiver span:                               0.3 m along y
receiver height:                             0.15 m
solution norm:                               10.787448040121925
max scattered norm:                          0.027575913303849516
min scattered norm:                          0.024732863613964377
mean scattered norm:                         0.0265692019903684
peak receiver index:                         10
peak receiver y:                             -0.075 m
receiver-line symmetry error:                8.994780900757268e-05
finite response:                             true
response contract ready:                     true
homogeneous BEM/FDTD comparison design ready: true
layered GPR forward model ready:             false
BEM-FWI ready:                               false
```

## Interpretation

The BEM track now emits a receiver-style response table rather than only a
solver norm. This makes the next validation step concrete: reproduce the same
simple finite-rebar geometry and receiver line in an FDTD reference, then
compare the narrowband response quantity.

The result is not a physical field GPR claim. It is a homogeneous PEC
time-harmonic scattering sample with a plane-wave excitation.

## Decision

Use this response CSV format as the first BEM/FDTD comparison contract.

Do not escalate to layered GPR modeling, inversion, or field-data usage until a
small FDTD reference case can be defined and compared against the same
geometry/receiver response.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bempp_rebar_receiver_response_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python -m py_compile run_bempp_rebar_receiver_response_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python run_bempp_rebar_receiver_response_probe.py --outdir outputs/bem_experiments/004_bempp_rebar_receiver_response_probe
```

## Next Action

Design the smallest FDTD reference case that can produce a compatible
narrowband receiver response for the same homogeneous PEC finite-cylinder
geometry.
