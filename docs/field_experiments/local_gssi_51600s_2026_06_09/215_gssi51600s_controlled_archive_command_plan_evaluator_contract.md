# Field Experiment 215: Controlled Archive Command-Plan Evaluator Contract

Date: 2026-06-28

## Purpose

Combine the fail-closed and positive-control command-plan evaluator guards into
one field-side evaluator contract.

This run does not ingest real field files, execute shell command templates,
accept a real archive, run field FWI, launch GPU/HPC work, or run 3D
validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/215_gssi51600s_controlled_archive_command_plan_evaluator_contract
```

Key artifacts:

```text
data/field_controlled_archive_command_plan_evaluator_contract_rows.csv
data/field_controlled_archive_command_plan_evaluator_contract_summary.json
figures/field_controlled_archive_command_plan_evaluator_contract.png
docs/FIELD_CONTROLLED_ARCHIVE_COMMAND_PLAN_EVALUATOR_CONTRACT.md
scripts/run_gssi_field_controlled_archive_command_plan_evaluator_contract.py
scripts/test_gssi_field_controlled_archive_command_plan_evaluator_contract.py
```

## Result

```text
guards:                             2
ready guards:                       2
fail-closed guard ready:            true
positive-control guard ready:       true
evaluator contract ready:           true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Guard | Source runs | Passes | Failures | Ready |
| --- | --- | ---: | ---: | --- |
| empty_archive_fail_closed | 209-211 | 0 | 27 | true |
| synthetic_valid_archive_positive_control | 212-214 | 27 | 0 | true |

## Interpretation

The command-plan evaluator now has two guarded behaviors:

```text
empty archive:          fails closed
synthetic valid archive: passes all checks
```

This is evaluator readiness. It is not real archive acceptance.

## Decision

Use this evaluator contract before real archive intake.

Real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC remain blocked until real measured files pass the same
checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_command_plan_evaluator_contract.py: pass
tests/test_gssi_field_controlled_archive_command_plan_evaluator_contract.py: pass
```

Figure check:

```text
2284x804, dynamic range=255
```
