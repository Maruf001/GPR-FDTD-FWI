# BEM Experiment 066: Layered Sommerfeld Proxy Stress

Date: 2026-06-25

## Purpose

Freshly stress-test the run `065` scalar two-layer Sommerfeld proxy on layered
project-core cases.

This validates whether the positive saved-case result from run `065` survives
new lateral, depth, and contrast variations.

This is CPU-only project-core FDTD/BEM adapter validation. It does not use
field data, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/066_project_core_bem_layered_sommerfeld_proxy_stress
```

Key artifacts:

```text
data/project_core_bem_layered_sommerfeld_proxy_stress.csv
data/project_core_bem_layered_sommerfeld_proxy_stress_summary.json
figures/project_core_bem_layered_sommerfeld_proxy_stress.png
docs/PROJECT_CORE_BEM_LAYERED_SOMMERFELD_PROXY_STRESS.md
```

## Result

```text
cases checked:                      4
ready cases:                        4
worst field leave-one-x L2:         0.3928483810786592
worst scattering leave-one-scan L2: 0.6497571611891657
Sommerfeld stress ready:            true
```

Case metrics:

| Case | epsr | x | z | Field LOO L2 | Scattering LOO L2 | Ready |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| base_epsr9 | 9.0 | 0.13 | 0.09 | 0.3928483810786592 | 0.6497571611891657 | true |
| left_shift_epsr9 | 9.0 | 0.11 | 0.09 | 0.3902655408879497 | 0.6274272306214017 | true |
| deep_z_epsr9 | 9.0 | 0.13 | 0.11 | 0.3786552771243828 | 0.5830498205741614 | true |
| high_contrast_epsr12 | 12.0 | 0.13 | 0.09 | 0.3928483810786592 | 0.6201923660960406 | true |

## Interpretation

The scalar Sommerfeld proxy survives the fresh layered stress ladder. This is a
substantial improvement over low-order image-source variants and the compact
30 mm tabulated-surface candidate.

It is now the active layered 2D BEM replacement candidate for the tested
project-core layered envelope.

## Decision

Promote the scalar Sommerfeld proxy to the active layered 2D BEM replacement
candidate.

Keep measured-field, 3D, FWI, GPU, and historical `outputs/experiments` archive
claims blocked pending matched gates.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_sommerfeld_proxy_stress.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_sommerfeld_proxy_stress.py
pass
```

Figure check:

```text
project_core_bem_layered_sommerfeld_proxy_stress.png
1924x846, dynamic range=255
```
