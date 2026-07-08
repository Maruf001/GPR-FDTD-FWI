# Field Experiment 216: Controlled Archive Command-Plan Evaluator Contract Validator

Date: 2026-06-28

## Purpose

Validate the run `215` command-plan evaluator contract.

This run does not ingest real field files, execute shell command templates,
accept a real archive, run field FWI, launch GPU/HPC work, or run 3D
validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/216_gssi51600s_controlled_archive_command_plan_evaluator_contract_validator
```

Key artifacts:

```text
data/field_controlled_archive_command_plan_evaluator_contract_validation_checks.csv
data/field_controlled_archive_command_plan_evaluator_contract_validator_summary.json
figures/field_controlled_archive_command_plan_evaluator_contract_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_COMMAND_PLAN_EVALUATOR_CONTRACT_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_command_plan_evaluator_contract_validator.py
scripts/test_gssi_field_controlled_archive_command_plan_evaluator_contract_validator.py
```

## Result

```text
validation checks:                  6
validation passes:                  6
blocking failures:                  0
validation ready:                   true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The evaluator contract is internally consistent: it contains exactly the
empty-archive fail-closed guard and the synthetic positive-control guard, both
ready, while real archive and downstream states remain blocked.

## Decision

Use run `216` as the validator for run `215`; sensitivity remains required
before treating the evaluator contract as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract_validator.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_command_plan_evaluator_contract_validator.py: pass
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract_validator.py: pass
```

Figure check:

```text
2285x847, dynamic range=255
```
