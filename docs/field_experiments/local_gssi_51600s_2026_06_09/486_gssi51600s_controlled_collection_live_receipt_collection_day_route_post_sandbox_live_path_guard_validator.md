# Field Experiment 486: Controlled Collection Live Receipt Collection-Day Route Post-Sandbox Live-Path Guard Validator

Date: 2026-06-30

## Purpose

Validate run `485` from saved artifacts.

This run checks that the post-sandbox live-path guard has the expected 33 guard
rows, that all sandbox files remain separate from the locked live paths, and
that measured field evidence and downstream field-processing readiness remain
blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/486_gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validator.png
scripts/
```

## Result

```text
checks:                       5
passed checks:                5
failed checks:                0
guard rows:                   33
live files present:           0
sandbox files present:        33
sandbox/live path overlap:    0
sandbox under live root:      0
synthetic-only files:         33
measured evidence files:      0
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
gpu priority:                 none
```

The five checks cover source readiness, guard row shape, empty live paths,
evidence/downstream blocking, and figure/script artifacts.

## Interpretation

Run `485` is a valid live-path guard. It confirms the sandbox receipt smoke did
not populate or overlap the locked live external return tree.

## Decision

Use run `486` as the artifact guard for run `485`. Keep live receipt, parser,
provenance, archive, controlled field evidence, field FWI, GPU work, and field
3D/HPC blocked until real measured files are placed in the locked live paths.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validator.py

3 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```
