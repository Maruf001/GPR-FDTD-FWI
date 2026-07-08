# BEM Experiment 181: Layered Payload Shell-Support Validated Contract Refresh

Date: 2026-06-28

## Purpose

Refresh the scoped shell-support contract with both geometric and
material/interface holdout evidence.

Run `179` combined the original four contract cases with four geometric
holdouts. Run `180` added three material/interface holdouts. This run combines
both evidence sets into the current validated local 2D BEM/FDTD layered-payload
contract.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/181_project_core_bem_layered_payload_shell_support_validated_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_validated_contract_cases.csv
data/project_core_bem_layered_payload_shell_support_validated_contract_refresh_summary.json
figures/project_core_bem_layered_payload_shell_support_validated_contract_refresh.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_VALIDATED_CONTRACT_REFRESH.md
scripts/run_project_core_bem_layered_payload_shell_support_validated_contract_refresh.py
scripts/test_project_core_bem_layered_payload_shell_support_validated_contract_refresh.py
```

## Result

```text
contract cases:                     4
geometric holdout cases:            4
material holdout cases:             3
total cases:                        11
total passes:                       11
total failures:                     0
acceptance L2 gate:                 0.75
worst case:                         larger_radius_epsr9
worst leave-one L2:                 0.7443538860706249
validated shell contract ready:     true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Evidence set | Count | Worst leave-one L2 |
| --- | ---: | ---: |
| contract_case | 4 | 0.7443538860706249 |
| holdout_shell_case | 4 | 0.7200480775878574 |
| material_shell_case | 3 | 0.7109170307749919 |

## Interpretation

The current scoped BEM shell-support contract contains 11 passing local 2D
BEM/FDTD rows: four original contract rows, four geometric holdouts, and three
material/interface holdouts.

The result strengthens the local 2D layered-payload evidence, but it remains
non-field and non-3D. It does not justify field transfer, 3D validation, GPU/HPC
escalation, field FWI, or promotion into the synthetic FDTD/FWI
`outputs/experiments` track.

## Decision

Record this as the current validated local 2D BEM/FDTD layered-payload contract.

Keep field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_material_holdout_validation.py
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_refresh.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_validated_contract_refresh.py: pass
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_refresh.py: pass
```

Figure check:

```text
2932x842, dynamic range=255
```
