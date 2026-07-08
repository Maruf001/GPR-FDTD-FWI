# BEM Experiment 912: Panel-116 Continuous-Shift Project-FDTD Comparison Design Contract

Date: 2026-07-01

## Purpose

Define the guarded project-FDTD comparison design contract for the smooth
continuous-shift BEM model from runs `909-911`.

This run writes the comparison requirements and fail-closed gates. It does not
write a launch packet, execute FDTD, consume FDTD return rows, complete a
BEM/FDTD comparison, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/912_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract
```

## Result

```text
source continuous ready:                  true
source validation ready:                  true
source sensitivity ready:                 true
contract items:                            6
ready contract items:                      2
gates:                                     5
fail-closed gates:                         5
BEM model:                                 best_gaussian_bump
BEM continuous pass count:                25
BEM high-band continuous pass count:       9
BEM continuous worst relative L2:          0.0008519458802336965
project FDTD comparison design ready:   true
project FDTD launch packet written:     false
project FDTD execution authorized now:  false
project FDTD executed now:              false
project FDTD return rows present:       false
project FDTD comparison completed:      false
field transfer ready:                   false
real 3D validation ready:               false
gpu priority:                           none
```

Contract items:

| Item | Ready now |
| --- | --- |
| geometry_identity | true |
| observable_identity | false |
| source_receiver_model | true |
| fdtd_return_schema | false |
| comparison_metric | false |
| claim_boundary | false |

Fail-closed gates:

| Gate | State | Execution allowed | Claim allowed |
| --- | --- | --- | --- |
| bem_candidate_validated | pass | false | false |
| project_fdtd_input_contract | design_only | false | false |
| project_fdtd_execution | not_executed | false | false |
| project_fdtd_comparison | not_completed | false | false |
| field_or_3d_transfer | blocked | false | false |

## Interpretation

The smooth continuous-shift BEM model is now ready for a fair project-FDTD
comparison design. The required comparison surface is clear: matched geometry,
matched complex electric-field observable, a finite real/imaginary FDTD return
schema, a relative-L2 metric on matched receiver-frequency rows, and a claim
boundary that requires real FDTD rows to pass schema and value checks.

The comparison itself is not complete. This run deliberately keeps execution
and downstream claims blocked.

## Decision

Use this as the comparison design contract. The next branch should be a
separate guarded launch/return packet or adapter, not a direct field or 3D
promotion.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_comparison_design_contract.py
4 passed
```

Figure check:

```text
2789x881, dynamic range=255
```
