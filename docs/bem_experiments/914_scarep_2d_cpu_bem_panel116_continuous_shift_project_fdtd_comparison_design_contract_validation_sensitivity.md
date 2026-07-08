# BEM Experiment 914: Panel-116 Continuous-Shift Project-FDTD Comparison Design Contract Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `913` design-contract validator by damaging the saved run
`912` contract in controlled ways.

The sensitivity set checks source-readiness damage, contract-row removal,
gate-row removal, ready-state damage, premature FDTD-schema readiness, open
execution gates, BEM metric damage, design demotion, false launch-packet
presence, false execution authorization, false return-row presence, false
comparison completion, downstream promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/914_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract_validation_sensitivity
```

## Result

```text
source validator ready:               true
scenarios:                            18
expected passes:                       1
expected failures:                    17
observed passes:                       1
observed failures:                    17
unexpected outcomes:                   0
damaged scenarios:                    17
project FDTD launch packet written: false
project FDTD execution authorized:  false
project FDTD return rows present:   false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

Scenario results:

| Scenario | Expected pass | Observed pass | Unexpected |
| --- | --- | --- | --- |
| exact_design_contract | true | true | false |
| contract_not_ready | false | false | false |
| contract_row_removed | false | false | false |
| gate_row_removed | false | false | false |
| geometry_not_ready | false | false | false |
| fdtd_schema_premature_ready | false | false | false |
| open_execution_gate | false | false | false |
| bem_metric_above_target | false | false | false |
| design_not_ready | false | false | false |
| launch_packet_written | false | false | false |
| execution_authorized | false | false | false |
| return_rows_present | false | false | false |
| comparison_completed | false | false | false |
| field_promoted | false | false | false |
| three_d_promoted | false | false | false |
| gpu_promoted | false | false | false |
| figure_damage | false | false | false |
| snapshot_damage | false | false | false |

## Interpretation

The run `913` validator accepts only the exact fail-closed design contract. It
rejects damaged contract rows, open gates, false execution or comparison
promotion, damaged figures, and damaged script snapshots.

## Decision

Use runs `912-914` as a guarded fail-closed design-contract block before any
launch/return packet work.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract_validation_sensitivity.py
3 passed
```

Figure check:

```text
2933x887, dynamic range=255
```
