# BEM Experiment 065: Layered Sommerfeld Proxy Probe

Date: 2026-06-25

## Purpose

Test a scalar two-layer transmitted Sommerfeld-style Green proxy against the
cached layered project-domain surface and scattering replay gate.

This is the first run after the image-source failures (`058`, `059`) to use a
layer-aware spectral Green construction rather than finite-domain image
tuning. It uses the run `061` cache as the FDTD reference and does not rerun
FDTD.

## Output

```text
outputs/bem_experiments/065_project_core_bem_layered_sommerfeld_proxy_probe
```

Key artifacts:

```text
data/project_core_bem_layered_sommerfeld_proxy_probe.csv
data/project_core_bem_layered_sommerfeld_proxy_probe_summary.json
data/project_core_bem_layered_sommerfeld_proxy_probe_arrays.npz
figures/project_core_bem_layered_sommerfeld_proxy_probe.png
docs/PROJECT_CORE_BEM_LAYERED_SOMMERFELD_PROXY_PROBE.md
```

## Result

```text
field all-x L2:                     0.38374219251352587
field leave-one-x L2:               0.3928483810786592
scattering all-scan L2:             0.5236861579717635
scattering leave-one-scan L2:       0.6497571611891658
Sommerfeld proxy ready:             true
```

The saved proxy surface has shape:

```text
19x533x17
```

## Interpretation

The scalar two-layer Sommerfeld proxy closes the saved layered replay gate and
substantially improves the field-table match relative to the low-order image
attempts.

This is not yet a promoted layered BEM replacement. It is a positive proxy
probe on one saved layered case.

## Decision

Promote the proxy to a fresh layered stress branch.

Keep field, 3D, FWI, GPU, and historical `outputs/experiments` archive claims
blocked.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_sommerfeld_proxy_probe.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_sommerfeld_proxy_probe.py
pass
```

Figure check:

```text
project_core_bem_layered_sommerfeld_proxy_probe.png
1564x810, dynamic range=255
```
