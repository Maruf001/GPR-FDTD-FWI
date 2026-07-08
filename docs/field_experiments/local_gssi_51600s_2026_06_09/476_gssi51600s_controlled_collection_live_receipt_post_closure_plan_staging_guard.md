# Field Experiment 476: Live Receipt Post-Closure-Plan Staging Guard

Date: 2026-06-30

## Purpose

Audit the live field staging paths after the closure-plan block in runs
`473-475`.

Run `473` reduced the current live staging gap into six collection-day action
groups. This run checks that planning step did not create or promote any live
field files.

This run does not copy field files, accept receipt rows, run the parser, accept
provenance, build an archive, run field FWI, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/476_gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_live_guard_rows.csv
data/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_summary.json
figures/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard.png
scripts/
```

## Result

```text
source closure plan ready:                true
source validation ready:                  true
source sensitivity ready:                 true
guard rows:                               33
DZT guard rows:                           9
metadata JSON guard rows:                 24
present parent directories:               33
live files present:                       0
live nonempty files:                      0
receipt-ready rows:                       0
closure-plan-created files:               0
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

## Interpretation

The closure-plan block was planning-only. All 33 required live receipt files
remain absent: nine measured DZT files and 24 completed metadata JSON files.

The live staging directory structure is present, but there is still no accepted
field evidence. The required next physical step remains copying real measured
files and completed metadata files into live staging, followed by receipt,
parser, provenance, and archive reruns.

## Decision

Use run `476` as the post-closure-plan live-boundary guard. Keep receipt,
parser, provenance, archive, field FWI, GPU work, and field 3D/HPC blocked
until real files are copied and accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_post_closure_plan_staging_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
