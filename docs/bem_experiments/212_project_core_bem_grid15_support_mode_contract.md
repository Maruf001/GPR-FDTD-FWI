# BEM Experiment 212: Grid-15 Support-Mode Contract

Date: 2026-06-28

## Purpose

Turn the guarded 15 mm grid-only tabulated-surface result into an explicit
support-mode contract.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/212_project_core_bem_grid15_support_mode_contract
```

Key artifacts:

```text
data/project_core_bem_grid15_support_mode_contract_support_summary.csv
data/project_core_bem_grid15_support_mode_contract_case_rows.csv
data/project_core_bem_grid15_support_mode_contract_summary.json
figures/project_core_bem_grid15_support_mode_contract.png
docs/PROJECT_CORE_BEM_GRID15_SUPPORT_MODE_CONTRACT.md
scripts/run_project_core_bem_grid15_support_mode_contract.py
scripts/test_project_core_bem_grid15_support_mode_contract.py
```

## Result

```text
surface policy:                     grid_15mm_only
cases:                              5
surface samples:                    13
ready support modes:                2
recommended support mode:           outer_shell_11mm_binary
recommended worst leave-one L2:     0.6083307089797199
recommended mean leave-one L2:      0.5941811606779211
recommended acceptance margin:      0.14166929102028014
volume ready cases:                 1
per-case router required:           false
support contract ready:             true
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

| Support mode | Ready cases | All cases ready | Mean leave-one L2 | Worst leave-one L2 | Margin |
| --- | ---: | --- | ---: | ---: | ---: |
| outer_shell_11mm_binary | 5 | true | 0.5941811606779211 | 0.6083307089797199 | 0.14166929102028014 |
| outer_shell_18mm_linear_radial | 5 | true | 0.5898125655154037 | 0.6160940767643346 | 0.13390592323566541 |
| volume_full | 1 | false | 0.7970688851709264 | 0.8213055444944041 | -0.07130554449440407 |

## Interpretation

The 15 mm grid-only policy does not need a per-case support router for the
tested 35 mm offset family. Both shell support modes pass all five tested cases.
The 11 mm binary shell has the lower worst-case error, while the 18 mm linear
radial shell has a slightly lower mean error but a worse worst case.

Volume support is not acceptable as the fixed support mode because it passes
only one of the five tested cases.

## Decision

Use `grid_15mm_only` with `outer_shell_11mm_binary` as the current fixed
support-mode contract for the tested 35 mm offset family.

Do not promote analytic replacement, field transfer, 3D validation, GPU/HPC, or
field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_support_mode_contract.py
5 passed
```

Python compile check:

```text
run_project_core_bem_grid15_support_mode_contract.py: pass
tests/test_project_core_bem_grid15_support_mode_contract.py: pass
```

Figure check:

```text
2932x847, dynamic range=255
```
