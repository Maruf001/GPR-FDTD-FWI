# Field Experiment 490: Controlled Collection Live Receipt Collection-Day Route Incremental Acceptance Frontier Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `489` validator.

This run mutates the saved run `488` frontier state one condition at a time and
checks that the validator accepts only the exact source state. It covers family
count damage, receipt-check count damage, frontier row damage, partial-complete
promotion, all-family completion removal, live-file promotion, downstream
promotion, figure damage, and missing script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/490_gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:       true
cases:                        17
expected pass cases:          1
expected fail cases:          16
actual pass cases:            1
actual fail cases:            16
unexpected cases:             0
damaged cases:                16
controlled evidence ready:    false
field FWI ready:              false
field 3D/HPC ready:           false
gpu priority:                 none
```

The exact source state passes. All damaged states fail as expected:

```text
source readiness false
family row removed
family file count damaged
family receipt-check count damaged
frontier row removed
current-state scenario removed
partial scenario promoted complete
all-family completion removed
minimum family count damaged
current live file promoted
current live receipt promoted
controlled evidence promoted
field FWI promoted
parser rerun readiness promoted
figure dynamic range removed
script snapshots removed
```

## Interpretation

The run `489` validator is sensitive to the failure modes that matter for the
collection-day frontier. It does not accept partial-completion promotion,
damaged family totals, live-file promotion, downstream promotion, or damaged
supporting artifacts.

## Decision

Use run `490` as the sensitivity audit for the run `488` acceptance-frontier
decision.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
