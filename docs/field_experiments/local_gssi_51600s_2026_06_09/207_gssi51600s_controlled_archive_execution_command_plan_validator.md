# Field Experiment 207: Controlled Archive Execution Command Plan Validator

Date: 2026-06-27

## Purpose

Validate the controlled archive execution command plan from run `206` from a
consumer perspective.

This is a CPU-only validation run. It does not ingest real DZT files, execute
command templates, modify any archive, accept field evidence, run field FWI,
launch GPU work, run field 3D/HPC, or train a neural network.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/207_gssi51600s_controlled_archive_execution_command_plan_validator
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_validation_checks.csv
data/field_controlled_archive_execution_command_plan_validator_summary.json
figures/field_controlled_archive_execution_command_plan_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_validator.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_validator.py
```

## Result

```text
validation checks:                  11
validation passes:                  11
blocking failures:                   0
source file slots:                   9
source commands:                    27
source command groups:               3
command-plan validation ready:       true
real archive acceptance ready:       false
checksum intake ready:               false
controlled evidence ready:           false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Command count and file-slot count | Passed |
| Required command groups | Passed |
| Exactly three commands per slot | Passed |
| File-existence command coverage | Passed |
| DZT signature command coverage | Passed |
| SHA-256 checksum command coverage | Passed |
| Archive-root template scoping | Passed |
| DZT size/header guard content | Passed |
| Command-plan ready flag | Passed |
| No premature execution or downstream readiness | Passed |

## Interpretation

The command plan is consumer-valid as a template package. Every pending DZT slot
has exactly three commands: file existence, DZT size/header guard, and SHA-256
checksum. All commands are scoped through the `${ARCHIVE_ROOT}` placeholder so a
future real archive can be checked without rewriting archive-relative paths.

This does not accept a real archive. The commands were not executed, no real
files were present, and the downstream field evidence states remain blocked.

## Decision

Use runs `206` and `207` as the command-plan package for future controlled
archive intake. Keep real archive acceptance, checksum intake, controlled
evidence, field FWI, heavy GPU work, field 3D/HPC, and neural-network training
blocked until the commands are executed on real files and all integrated gates
pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan.py
tests/test_gssi_field_controlled_archive_execution_command_plan_validator.py
8 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan_validator.png
2681x857, dynamic range=255
```
