# Field Experiment 473: Live Receipt Acceptance Gate Staging Gap Closure Plan

Date: 2026-06-30

## Purpose

Reduce the live staging gap from run `470` into a short collection-day closure
plan.

Runs `470-472` prove that the current staging tree has all required
directories but none of the 33 required live receipt files. This run keeps the
exact missing-file rows and adds a grouped action view.

This run does not copy field files, accept receipt rows, run the parser, accept
provenance, build an archive, run field FWI, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/473_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_missing_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_closure_group_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan.png
scripts/
```

## Result

```text
source gap ready:                         true
source validation ready:                  true
source sensitivity ready:                 true
closure groups:                           6
file closure groups:                      5
gate-rerun groups:                        1
missing files:                            33
missing DZT files:                        9
missing metadata JSON files:              24
missing controlled profile files:         3
missing time-zero reference files:        3
missing amplitude-reference files:        3
missing global metadata files:            15
missing per-file metadata files:          9
present files:                            0
ready groups:                             0
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The six closure groups are:

| Priority | Closure group | Missing files |
| ---: | --- | ---: |
| 1 | copy measured controlled profile repeat DZT files | 3 |
| 2 | copy measured time-zero reference DZT files | 3 |
| 3 | copy measured amplitude-reference DZT files | 3 |
| 4 | copy completed global session metadata JSON files | 15 |
| 5 | copy completed per-file metadata JSON files | 9 |
| 6 | rerun receipt, parser, provenance, and archive gates | 0 |

## Interpretation

The field blocker is now both exact and compact. The exact missing-file table
still has all 33 required paths, while the closure plan reduces the work into
five file-copy groups plus one gate-rerun group.

No field evidence has been accepted. The next physical step remains copying
measured DZT files and completed metadata JSON files into the live staging
tree, then rerunning the receipt, parser, provenance, and archive gates.

## Decision

Use run `473` as the current field-side collection-day action reducer. Keep
field FWI, GPU work, and field 3D/HPC blocked until the live receipt and
downstream acceptance gates pass with real files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan.py

3 passed
```

Figure validation:

```text
2465x843, dynamic range=255
```
