# BEM Experiment 913: Panel-116 Continuous-Shift Project-FDTD Comparison Design Contract Validator

Date: 2026-07-01

## Purpose

Validate the saved run `912` project-FDTD comparison design contract.

The validator checks source readiness, contract-row shape, fail-closed gate
state, preserved BEM candidate metrics, blocked execution/downstream flags,
figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/913_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
contract items:                          6
ready contract items:                    2
gates:                                   5
fail-closed gates:                       5
BEM model:                               best_gaussian_bump
BEM continuous pass count:               25
BEM high-band continuous pass count:      9
BEM continuous worst relative L2:         0.0008519458802336965
project FDTD comparison design ready:  true
project FDTD launch packet written:    false
project FDTD execution authorized now: false
project FDTD executed now:             false
project FDTD return rows present:      false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

Validation checks:

| Check | Passed |
| --- | --- |
| design_contract_ready | true |
| contract_rows_stable | true |
| gate_rows_fail_closed | true |
| bem_candidate_and_metric_preserved | true |
| execution_and_downstream_blocked | true |
| figure_and_scripts_valid | true |

## Interpretation

The run `912` design contract validates as a fail-closed project-FDTD
comparison contract. It is ready as a design artifact, but it does not
authorize FDTD execution and does not complete a BEM/FDTD comparison.

## Decision

Use run `912` as the guarded design contract. The next branch should validate
or prepare a separate launch/return packet before any FDTD execution or
comparison claim.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract_validator.py
4 passed
```

Figure check:

```text
2465x862, dynamic range=255
```
