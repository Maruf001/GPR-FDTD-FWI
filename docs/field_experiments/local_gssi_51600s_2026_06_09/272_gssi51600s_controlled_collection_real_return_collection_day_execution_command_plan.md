# Field Experiment 272: Controlled Collection-Day Execution Command Plan

Date: 2026-06-28

## Purpose

Convert the guarded fill packet from runs `269-271` into a non-executed
collection-day execution plan.

This run uses saved artifacts only. It does not ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/272_gssi51600s_controlled_collection_real_return_collection_day_execution_command_plan
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_execution_command_rows.csv
data/field_controlled_collection_real_return_collection_day_commands.sh
data/field_controlled_collection_real_return_collection_day_execution_command_plan_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_execution_command_plan.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_EXECUTION_COMMAND_PLAN.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required files:                      9
metadata values:                    32
checksums:                           9
acceptance gates:                    7
command phases:                      8
commands executing now:              0
execution plan ready:                true
real files present:                  false
metadata values present:             false
checksums present:                   false
provenance acceptance ready:         false
real archive acceptance ready:       false
controlled evidence ready:           false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

Command phases:

| Phase | Produces |
| ---: | --- |
| 1 | 11 measured global metadata values |
| 2 | three controlled profile repeat DZT files |
| 3 | three time-zero reference DZT files |
| 4 | three amplitude-reference DZT files |
| 5 | nine staged real DZT files in exact inbox slots |
| 6 | nine checksum values |
| 7 | 21 measured per-file metadata values |
| 8 | structural and provenance pass/fail summaries |

## Interpretation

The field-side collection now has an ordered non-executed plan for real
metadata capture, nine DZT files, checksums, metadata fill, and validator
reruns. No real files or values are present yet.

## Decision

Use run `272` as the controlled collection-day execution plan. Keep provenance
acceptance, archive acceptance, controlled evidence, field FWI, field 3D/HPC,
and GPU work blocked until real measured files, metadata, and checksums are
staged and validated.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_execution_command_plan.py
3 passed
```

Figure validation:

```text
3077x915, dynamic range=255
```
