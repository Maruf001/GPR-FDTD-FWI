# Field Experiment 251: Controlled Archive Real Return Current Guard Execution Smoke

Date: 2026-06-28

## Purpose

Execute only the current guard-validation commands from the guarded run `248`
real-return archive command checklist.

This run does not execute future real-archive commands, inspect real measured
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/251_gssi51600s_controlled_archive_real_return_current_guard_execution_smoke
```

Key artifacts:

```text
data/field_controlled_archive_real_return_current_guard_execution_rows.csv
data/field_controlled_archive_real_return_current_guard_execution_summary.json
figures/field_controlled_archive_real_return_current_guard_execution_smoke.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_CURRENT_GUARD_EXECUTION_SMOKE.md
scripts/run_gssi_field_controlled_archive_real_return_current_guard_execution_smoke.py
scripts/test_gssi_field_controlled_archive_real_return_current_guard_execution_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source sensitivity guarded:            true
executable guard commands:             3
executed commands:                     3
passed commands:                       3
failed commands:                       0
current guard execution smoke ready:   true
future real-archive commands executed: false
real files present:                    false
ready for real archive acceptance:     false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Executed guard commands:

| Command | Return code | Passed |
| --- | ---: | ---: |
| real-return boundary focused tests | 0 | true |
| empty skeleton validator | 0 | true |
| synthetic positive-control validator | 0 | true |

## Interpretation

The current field real-return guard commands execute cleanly. Future real
archive commands remain unexecuted and blocked because real measured files are
still missing.

## Decision

Use run `251` as the current-guard execution smoke for the real-return archive
checklist. Real measured files remain required before archive acceptance, field
evidence promotion, field FWI, field 3D/HPC, or GPU escalation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_current_guard_execution_smoke.py
4 passed
```

Executed guard commands:

```text
14 passed
empty skeleton validator: return code 0
synthetic positive-control validator: return code 0
```

Figure validation:

```text
2465x822, dynamic range=255
```
