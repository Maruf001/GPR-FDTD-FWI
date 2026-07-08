# Field Experiment 217: Controlled Archive Command-Plan Evaluator Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `216` evaluator-contract validator with damaged guard rows
and summaries.

This run does not ingest real field files, execute shell command templates,
accept a real archive, run field FWI, launch GPU/HPC work, or run 3D
validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/217_gssi51600s_controlled_archive_command_plan_evaluator_contract_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_command_plan_evaluator_contract_sensitivity_scenarios.csv
data/field_controlled_archive_command_plan_evaluator_contract_sensitivity_summary.json
figures/field_controlled_archive_command_plan_evaluator_contract_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_COMMAND_PLAN_EVALUATOR_CONTRACT_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_command_plan_evaluator_contract_sensitivity.py
scripts/test_gssi_field_controlled_archive_command_plan_evaluator_contract_sensitivity.py
```

## Result

```text
scenarios:                         13
expected pass scenarios:           1
expected failure scenarios:        12
observed pass scenarios:           1
observed failure scenarios:        12
unexpected outcomes:               0
sensitivity ready:                 true
real archive acceptance ready:     false
checksum intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
3D/HPC ready:                      false
```

The exact evaluator contract passes. Damaged contracts fail for the intended
reasons: missing guard row, guard-count drift, fail-closed unexpected pass,
fail-closed not ready, positive-control failure, positive-control not ready,
fail-closed flag false, positive flag false, contract not ready, real archive
ready, checksum intake ready, and field FWI ready.

## Interpretation

Runs `215`-`217` form a guarded field command-plan evaluator contract. The
evaluator has both expected-failure and expected-pass behavior:

```text
empty archive:          0 passes, 27 failures
synthetic valid archive: 27 passes, 0 failures
```

This remains evaluator readiness only, not real archive acceptance.

## Decision

Use runs `215`-`217` as the guarded field command-plan evaluator contract.

Real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC remain blocked until real measured files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract_sensitivity.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_command_plan_evaluator_contract_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract_sensitivity.py: pass
```

Figure check:

```text
2825x860, dynamic range=255
```
