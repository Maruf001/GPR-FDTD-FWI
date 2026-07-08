# BEM Experiment 059: Layered Interface Basis Ladder

Date: 2026-06-25

## Purpose

Diagnose the run `058` layered boundary-image failure with simple layer-aware
Green surrogate terms.

The tested basis terms include air-speed direct fields, concrete-speed direct
fields, optical-path air/concrete fields, interface-reflected source terms, and
finite-domain optical image terms. This is a CPU-only diagnostic; it does not
run field preprocessing, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/bem_experiments/059_project_core_bem_layered_interface_basis_ladder
```

Key artifacts:

```text
data/project_core_bem_layered_interface_basis_ladder.csv
data/project_core_bem_layered_interface_basis_ladder_summary.json
figures/project_core_bem_layered_interface_basis_ladder.png
docs/PROJECT_CORE_BEM_LAYERED_INTERFACE_BASIS_LADDER.md
```

## Result

```text
variants checked:                   81
surface samples:                    19
target cells:                       533
selected frequency bins:            17
run 046 sparse interpolated L2:     1.1770012780031571
run 046 exact-surface L2:           0.619762715748986
best field-table LOO L2:            1.1925655903879098
best scattering all-scan L2:        0.8083671696254245
best scattering LOO L2:             1.0946737347877629
layer-aware basis ready:            false
```

Best scattering variant:

```text
source z:             0.038 m
lower-index scale:    1.15
basis set:            layer_mix_cardinal
scattering variant:   product_no_div
```

Best scattering rows:

| Rank | z | Lower-index scale | Basis | Field LOO L2 | Scattering LOO L2 | Variant |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 1 | 0.038 | 1.15 | layer_mix_cardinal | 1.3119809476663844 | 1.0946737347877629 | product_no_div |
| 2 | 0.038 | 1.15 | optical_cardinal | 1.3347857833534187 | 1.0972837020095705 | product_no_div |
| 3 | 0.038 | 1.15 | optical_cardinal_interface | 1.3320768146271686 | 1.100973542631527 | product_no_div |
| 4 | 0.038 | 1.0 | optical_cardinal | 1.3156123166727056 | 1.1081956583411663 | product_no_div |

## Interpretation

Simple optical-path and interface-image terms do not close the saved layered
replay gate. They are also worse than run `058`'s best homogeneous
boundary-image replay, which reached scattering LOO L2 `0.9920836859251249`.

The missing layered physics is therefore not a small scalar correction to the
homogeneous image model. The tested layer requires either the dense
project-domain field table, a true layered Green function, or a tabulated FDTD
surface model.

## Decision

Keep layered media on the dense project-domain field-table path.

Do not use low-order optical/interface image terms for layered, field, 3D, FWI,
GPU, or historical `outputs/experiments` archive claims.

## Validation

Compile check:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_project_core_bem_layered_interface_basis_ladder.py
pass
```

Run:

```text
conda run -n gpr-fdtd-fwi python run_project_core_bem_layered_interface_basis_ladder.py
pass
```

Figure check:

```text
project_core_bem_layered_interface_basis_ladder.png
2392x1098, dynamic range=255
```
