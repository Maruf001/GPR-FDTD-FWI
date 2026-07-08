# Field Experiment 208: Controlled Archive Execution Command Plan Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the controlled archive execution command-plan validator from run
`207` with damaged command-plan variants.

This is a CPU-only sensitivity run. It does not ingest real DZT files, execute
command templates, modify any archive, accept field evidence, run field FWI,
launch GPU work, run field 3D/HPC, or train a neural network.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/208_gssi51600s_controlled_archive_execution_command_plan_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_sensitivity_rows.csv
data/field_controlled_archive_execution_command_plan_sensitivity_summary.json
figures/field_controlled_archive_execution_command_plan_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_sensitivity.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_sensitivity.py
```

## Result

```text
sensitivity scenarios:              10
expected pass scenarios:             1
observed pass scenarios:             1
expected failure scenarios:          9
observed failure scenarios:          9
unexpected outcomes:                 0
command-plan sensitivity ready:      true
real archive acceptance ready:       false
checksum intake ready:               false
controlled evidence ready:           false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

The exact command plan passes. These damaged variants fail as expected:

| Scenario | Failed checks |
| --- | --- |
| Missing command row | Command count, per-slot command count, checksum coverage |
| Wrong command group | Expected group set and file-exists coverage |
| Missing archive-root scope | Archive-root template scoping |
| Wrong DZT header guard | DZT size/header guard content |
| Wrong DZT size guard | DZT size/header guard content |
| Command-count mismatch | Summary command count |
| Command plan not ready | Ready flag |
| Commands marked executed | Premature execution/downstream state |
| Field FWI marked ready | Premature execution/downstream state |

## Interpretation

The command-plan validator is sensitive to the main failure modes that would
make a future real archive intake unsafe or ambiguous. It catches missing
coverage, command-group drift, loss of archive-root scoping, damaged DZT guards,
count mismatches, a not-ready command-plan state, and premature downstream
readiness.

This still does not accept a real archive. It validates the template and its
guard behavior only.

## Decision

Use runs `206`-`208` as the current command-plan guard package for future
controlled archive intake. Keep real archive acceptance, checksum intake,
controlled evidence, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until the commands are executed on real files
and all integrated gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan.py
tests/test_gssi_field_controlled_archive_execution_command_plan_validator.py
tests/test_gssi_field_controlled_archive_execution_command_plan_sensitivity.py
12 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan_sensitivity.png
2681x847, dynamic range=255
```
