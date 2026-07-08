# Field Experiment 485: Controlled Collection Live Receipt Collection-Day Route Post-Sandbox Live-Path Guard

Date: 2026-06-30

## Purpose

Audit the locked live field paths after the sandbox receipt-smoke block
`482-484`.

The sandbox smoke intentionally created 33 synthetic placeholder files inside
its own output directory. This run checks that those files stayed output-local
and did not overlap with, or populate, the locked live external return paths.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/485_gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_guard_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard.png
scripts/
```

## Result

```text
source smoke ready:              true
source validation ready:         true
source sensitivity ready:        true
guard rows:                      33
live files present:              0
sandbox files present:           33
sandbox/live path overlap:       0
sandbox files under live root:   0
synthetic-only files:            33
measured field evidence files:   0
live receipt-ready files:        0
parser ready:                    false
provenance ready:                false
archive ready:                   false
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

## Interpretation

The sandbox files remained confined to the run `482` output directory. The
locked live field paths are still empty, so the live field packet has not been
promoted by the sandbox smoke.

## Decision

Use run `485` as the post-sandbox live-path guard. Keep live receipt, parser,
provenance, archive, controlled field evidence, field FWI, GPU work, and field
3D/HPC blocked until real measured files are copied into the locked live paths
and all downstream gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
