# BEM Experiment 182: Layered Payload Shell-Support Validated Contract Validator

Date: 2026-06-28

## Purpose

Validate the run `181` shell-support contract from a downstream consumer
perspective.

Run `181` created the current validated local 2D BEM/FDTD layered-payload
contract with 11 passing rows. This run checks whether a later script can read
that contract and independently confirm the case counts, readiness flags, worst
error gate, and blocked promotion states.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/182_project_core_bem_layered_payload_shell_support_validated_contract_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_validated_contract_validation_checks.csv
data/project_core_bem_layered_payload_shell_support_validated_contract_validator_summary.json
figures/project_core_bem_layered_payload_shell_support_validated_contract_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_VALIDATED_CONTRACT_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_shell_support_validated_contract_validator.py
scripts/test_project_core_bem_layered_payload_shell_support_validated_contract_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
source total cases:                 11
source validated contract ready:    true
consumer ready:                     true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Check | Expected | Observed | Passes |
| --- | --- | ---: | --- |
| total case count matches summary | 11 | 11 | true |
| all rows ready | 11 | 11 | true |
| contract case count matches summary | 4 | 4 | true |
| geometric holdout count matches summary | 4 | 4 | true |
| material holdout count matches summary | 3 | 3 | true |
| worst L2 below acceptance gate | <= 0.75 | 0.7443538860706249 | true |
| source contract marked ready | true | true | true |
| field transfer remains blocked | false | false | true |
| GPU/3D/field FWI remain blocked | false | false | true |

## Interpretation

The validated shell-support contract is internally consistent and
consumer-ready. All 11 rows are ready, all summary counts match the case table,
the worst leave-one-scan L2 remains below the `0.75` acceptance gate, the
source contract is marked ready, and the field/3D/GPU promotion flags remain
blocked.

This is a contract-consumption check, not new physics evidence. It protects the
run `181` decision from accidental downstream misreading.

## Decision

Use run `181` as the current validated BEM shell-support contract and run `182`
as its consumer validator.

Keep field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_validator.py
3 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_validated_contract_validator.py: pass
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_validator.py: pass
```

Figure check:

```text
2609x805, dynamic range=255
```
