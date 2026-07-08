# BEM Experiment 183: Layered Payload Shell-Support Contract Sensitivity

Date: 2026-06-28

## Purpose

Test whether the run `182` consumer validator rejects damaged versions of the
run `181` validated shell-support contract.

Run `182` showed that the current contract can be consumed correctly. This run
checks the opposite side of the gate: a damaged contract should not pass.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/183_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_validated_contract_sensitivity_scenarios.csv
data/project_core_bem_layered_payload_shell_support_validated_contract_sensitivity_summary.json
figures/project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_VALIDATED_CONTRACT_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py
scripts/test_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py
```

## Result

```text
scenarios:                         10
expected pass scenarios:           1
expected block scenarios:          9
unexpected outcomes:               0
sensitivity ready:                 true
field transfer ready:              false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

| Scenario | Expected ready | Observed ready | Blocking failures | Failed checks |
| --- | --- | --- | ---: | --- |
| exact_contract | true | true | 0 | none |
| missing_case_row | false | false | 2 | total_case_count_matches_summary; material_holdout_count_matches_summary |
| row_not_ready | false | false | 1 | all_rows_ready |
| contract_count_mismatch | false | false | 1 | contract_case_count_matches_summary |
| worst_l2_above_gate | false | false | 1 | worst_l2_below_acceptance_gate |
| source_contract_not_ready | false | false | 1 | source_contract_marked_ready |
| field_transfer_marked_ready | false | false | 1 | field_transfer_remains_blocked |
| gpu_marked_ready | false | false | 1 | gpu_3d_field_fwi_remain_blocked |
| three_d_marked_ready | false | false | 1 | gpu_3d_field_fwi_remain_blocked |
| field_fwi_marked_ready | false | false | 1 | gpu_3d_field_fwi_remain_blocked |

## Interpretation

The consumer validator accepts the exact run `181` contract and rejects all nine
intentionally damaged variants: missing rows, not-ready rows, count mismatch,
above-gate L2, false source readiness, and incorrect field/3D/GPU/FWI promotion
flags.

This strengthens the BEM contract package by showing that the validator has
negative-control behavior, not only positive acceptance behavior.

## Decision

Use runs `181`-`183` as the current validated local 2D BEM shell-support
contract package.

Keep field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_validator.py
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py: pass
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py: pass
```

Figure check:

```text
2716x851, dynamic range=255
```
