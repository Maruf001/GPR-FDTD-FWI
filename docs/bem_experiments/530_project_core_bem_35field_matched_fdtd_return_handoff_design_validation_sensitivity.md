# BEM Experiment 530: 35-Field Matched FDTD Return Handoff Design Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `529` validator.

The exact run `528` handoff should pass. Damaged source readiness, row counts,
key alignment, premature FDTD values, premature comparison readiness, premature
writer readiness, action ordering, figure validation, and script snapshots
should fail.

## Output

```text
outputs/bem_experiments/530_project_core_bem_35field_matched_fdtd_return_handoff_design_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_handoff_design_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_handoff_design_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_handoff_design_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
handoff sensitivity ready:                 true
exact source artifacts pass:               true
row-count damage rejected:                 true
key-alignment damage rejected:             true
premature promotion rejected:              true
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

Damaged scenarios rejected:

| Scenario | Expected result |
| --- | --- |
| source readiness damage | fail |
| FDTD source row-count drift | fail |
| FDTD norm row-count drift | fail |
| pairing row-count drift | fail |
| key alignment damage | fail |
| FDTD value premature promotion | fail |
| comparison premature promotion | fail |
| accepted writer promotion | fail |
| action order damage | fail |
| figure damage | fail |
| script snapshot damage | fail |

## Decision

Use runs `528-530` as the guarded matched-FDTD handoff block after the
fine-mesh BEM export. The next BEM bridge task is real FDTD return-value export,
not an accepted comparison claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_handoff_design_validation_sensitivity.py
3 passed
```

Figure check:

```text
2897x857, dynamic range=255
```
