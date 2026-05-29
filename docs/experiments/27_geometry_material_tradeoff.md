# Experiment 27: Geometry Versus Material Tradeoff

## Goal

Test whether radius evidence can be mimicked by material changes.

Question:

```text
At the correct x/z location, can an incorrect radius plus different concrete
permittivity or effective rebar conductivity fit the observed data nearly as
well as the true radius?
```

This is the Day 8 branch from the master plan.

## Code Changes

Added:

```text
run_single_rebar_material_tradeoff.py
tests/test_material_tradeoff_runner.py
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_material_tradeoff_runner.py -q
3 passed

/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile run_single_rebar_material_tradeoff.py
passed
```

## Planned Matrix

Fixed geometry location:

```text
x=250.0 mm
z=90.0 mm
```

Sweeps:

```text
radius:         5.4-7.8 mm in 0.2 mm steps
concrete epsr:  5.5, 6.0, 6.5
rebar sigma:    1e5, 1e6, 1e7 S/m
```

This first matrix intentionally keeps x/z fixed. If material ambiguity appears
even at the correct location, the follow-up should include z as another
tradeoff dimension.

## Run Log

### 056_material_tradeoff_fixed_xz_exact

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_material_tradeoff.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-mm 250.0 \
  --z-mm 90.0 \
  --radius-values-mm 5.4:7.8:0.2 \
  --concrete-epsr-values 5.5,6.0,6.5 \
  --rebar-log10-sigma-values 5,6,7 \
  --run-name material_tradeoff_fixed_xz_exact
```

Output:

```text
outputs/experiments/056_material_tradeoff_fixed_xz_exact
```

Plot validation:

```text
material_profiled_radius.png: 1464x869 px, dynamic range 255
```

Top candidates:

| Rank | r [mm] | concrete epsr | rebar sigma [S/m] | J |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 6.0 | 6.0 | 1e7 | 0.000e+00 |
| 2 | 6.0 | 6.0 | 1e6 | 3.184e-10 |
| 3 | 6.0 | 6.0 | 1e5 | 3.853e-08 |
| 4 | 6.2 | 6.0 | 1e7 | 1.037e-03 |
| 5 | 6.2 | 6.0 | 1e6 | 1.037e-03 |
| 6 | 6.2 | 6.0 | 1e5 | 1.037e-03 |

Best distinct-radius margin:

```text
r=6.0 beats r=6.2 by 1.037e-03
```

## Interpretation

At the correct x/z location, the tested material degrees of freedom do not
erase radius evidence.

Concrete permittivity is strongly identifiable in this controlled synthetic
case:

```text
the best candidates all use epsr=6.0, the true value
epsr=5.5 or 6.5 produces much larger misfit
```

Effective rebar conductivity is mostly saturated:

```text
1e5, 1e6, and 1e7 S/m all behave almost the same for the true radius
```

This means adding rebar conductivity as a free parameter is unlikely to fix the
current radius issue. The more important ambiguity is geometry/source related:

```text
radius-depth tradeoff,
source wavelet amplitude/time/frequency mismatch.
```

## Day 8 Decision

Do not add material parameters to the normal single-rebar inversion pipeline
yet. Keep concrete epsr and rebar effective sigma fixed for the next iteration.

If future field data show concrete property uncertainty, handle it with a
separate calibration or nuisance-parameter profile, not by immediately adding
material parameters to the radius optimizer.
