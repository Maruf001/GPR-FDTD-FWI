# BEM Experiment 006: Bempp Rebar Frequency Sweep Probe

Date: 2026-06-23

## Purpose

Sweep the run `004` finite-rebar receiver response contract over multiple
wavenumbers to check basic stability of the homogeneous PEC `bempp-cl`
prototype.

This is a BEM-only stability checkpoint. It is not FDTD validation, layered GPR
modeling, broadband synthesis, field-data processing, inversion, or heavy GPU
work.

## Output

```text
outputs/bem_experiments/006_bempp_rebar_frequency_sweep_probe
```

Key artifacts:

```text
data/bempp_rebar_frequency_sweep_summary.csv
data/bempp_rebar_frequency_sweep_receivers.csv
data/bempp_rebar_frequency_sweep_probe_summary.json
docs/BEMPP_REBAR_FREQUENCY_SWEEP_PROBE.md
run_manifest.json
```

## Result

```text
mesh triangles:                    120
mesh vertices:                     62
mesh closed:                       true
receiver count:                    21
receiver span:                     0.3 m along y
receiver height:                   0.15 m
wavenumbers:                       4, 6, 8, 10, 12 rad/m
finite all:                        true
min max-scattered norm:            0.01916740428427016
max max-scattered norm:            0.05802136168763753
max-scattered norm ratio:          3.027084983815628
BEM-only frequency sweep ready:    true
BEM/FDTD validation ready:         false
layered GPR forward model ready:   false
BEM-FWI ready:                     false
```

Sweep table:

| k rad/m | Max scattered norm | Mean scattered norm | Peak y m | Finite |
| ---: | ---: | ---: | ---: | ---: |
| 4.0 | 0.01916740428427016 | 0.018212435653081994 | -0.045 | true |
| 6.0 | 0.02149345534049773 | 0.020382811652416434 | -0.09 | true |
| 8.0 | 0.027575913303849516 | 0.026520441953374572 | -0.075 | true |
| 10.0 | 0.039723694759844205 | 0.036527009738210846 | 0.0 | true |
| 12.0 | 0.05802136168763753 | 0.049477129402746144 | 0.0 | true |

## Interpretation

The direct finite-rebar Bempp response remains finite across the tested
wavenumber range. This supports continued BEM-only prototype development and
response-contract refinement.

The sweep does not validate the BEM result against FDTD. It also does not
address layered media, broadband GPR pulses, antenna/source coupling, field
data, or inversion.

## Decision

Keep run `006` as a BEM-only stability checkpoint. The next validation-facing
work remains:

```text
1. a clearly labeled 2D TMz FDTD sanity check;
2. a separate small 3D FDTD reference design for direct finite-cylinder validation.
```

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bempp_rebar_frequency_sweep_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python -m py_compile run_bempp_rebar_frequency_sweep_probe.py
outputs/bem_experiments/_venvs/bempp-cl-0.4.2-py312/bin/python run_bempp_rebar_frequency_sweep_probe.py --outdir outputs/bem_experiments/006_bempp_rebar_frequency_sweep_probe
```

## Next Action

Design the 2D TMz cross-section sanity check using the existing FDTD code, with
explicit language that it is not direct validation of the 3D finite-cylinder
BEM result.
