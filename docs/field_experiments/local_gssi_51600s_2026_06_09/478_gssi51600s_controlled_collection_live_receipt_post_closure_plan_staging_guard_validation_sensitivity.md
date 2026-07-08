# Field Experiment 478: Live Receipt Post-Closure-Plan Staging Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `477`.

This run checks that the validator accepts the exact run `476` guard and
rejects damaged states that would falsely promote live files, receipt
readiness, closure-plan side effects, downstream field readiness, or damaged
artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/478_gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_post_closure_plan_staging_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
cases:                               14
expected pass cases:                 1
expected fail cases:                 13
actual pass cases:                   1
actual fail cases:                   13
unexpected outcomes:                 0
damaged cases:                       13
parser ready:                        false
provenance ready:                    false
archive ready:                       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

The damaged states cover source-chain damage, guard-row removal, DZT-count
damage, metadata-count damage, parent-directory damage, live-file promotion,
live nonempty-file promotion, receipt-readiness promotion, closure-plan-created
file promotion, field-FWI promotion, figure damage, and script-snapshot damage.

## Interpretation

The live staging guard validator is sensitive to the failure modes that would
matter before accepting field evidence. It does not allow missing field files
to be promoted by a planning artifact.

## Decision

Use runs `476-478` as the closed post-closure-plan live-boundary block. Keep
receipt, parser, provenance, archive, field FWI, and field 3D/HPC blocked until
real files are copied and accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_post_closure_plan_staging_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
