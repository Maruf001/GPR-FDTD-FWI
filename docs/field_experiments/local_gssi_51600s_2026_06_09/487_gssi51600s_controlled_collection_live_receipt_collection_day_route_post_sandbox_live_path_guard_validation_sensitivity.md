# Field Experiment 487: Controlled Collection Live Receipt Collection-Day Route Post-Sandbox Live-Path Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `486`.

This run checks that the validator accepts the exact run `485` live-path guard
and rejects damaged states that would promote live files, create sandbox/live
path overlap, place sandbox files under the live root, lose the synthetic
boundary, promote measured evidence, promote downstream field readiness, or
damage artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/487_gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:      true
cases:                       19
expected pass cases:         1
expected fail cases:         18
actual pass cases:           1
actual fail cases:           18
unexpected outcomes:         0
damaged cases:               18
controlled evidence ready:   false
field FWI ready:             false
field 3D/HPC ready:          false
gpu priority:                none
```

The damaged states cover source readiness removal, guard-row removal, guard
count damage, sandbox file-count damage, live-file promotion, sandbox/live path
overlap, sandbox-under-live-root promotion, synthetic-boundary loss, measured
evidence promotion, controlled-evidence promotion, parser/provenance/archive
readiness promotion, field FWI promotion, field 3D/HPC promotion,
parser-rerun readiness promotion, figure damage, and script-snapshot damage.

## Interpretation

The post-sandbox live-path guard validator is sensitive to the failure modes
that would falsely promote the sandbox into live measured field evidence.

## Decision

Use runs `485-487` as the current closed post-sandbox live-path guard block.
Keep the live field packet blocked until real measured files are copied into
the locked live paths and pass downstream gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_post_sandbox_live_path_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
