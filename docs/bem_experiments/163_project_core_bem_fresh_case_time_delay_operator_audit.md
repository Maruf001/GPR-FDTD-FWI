# BEM Experiment 163: Fresh-Case Time-Delay Operator Audit

Date: 2026-06-27

## Purpose

Test whether the fresh-case project-core mismatch can be explained by a
physically constrained time-delay operator.

Runs `159` through `162` showed structured receiver/frequency residuals and
ruled out empirical receiver/frequency scale tables. This run tests a more
constrained phase-ramp hypothesis: global delay, receiver-specific delay, and
linear receiver-delay models fitted on two fresh cases and evaluated on the
held-out third case.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/163_project_core_bem_fresh_case_time_delay_operator_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_time_delay_operator_rows.csv
data/project_core_bem_fresh_case_time_delay_operator_audit_summary.json
figures/project_core_bem_fresh_case_time_delay_operator_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_TIME_DELAY_OPERATOR_AUDIT.md
scripts/run_project_core_bem_fresh_case_time_delay_operator_audit.py
scripts/test_project_core_bem_fresh_case_time_delay_operator_audit.py
```

## Result

```text
fresh cases:                         3
time-delay models:                   3
leave-one-case-out rows:             9
improvement rows:                    2
strict-gate passes:                  0
all best cases pass gate:            false
worst best case:                     shifted_deeper_epsr4
worst best model:                    receiver_specific_delay
worst best L2:                       0.5924545602816863
max absolute receiver delay ns:      0.03999999999999986
time-delay operator ready:           false
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

| Held-out case | Best model | Baseline L2 | Best corrected L2 |
| --- | --- | ---: | ---: |
| lower_contrast_radius_25mm | global_delay | 0.18685792461171657 | 0.18685792461171657 |
| shifted_deeper_epsr4 | receiver_specific_delay | 0.5997321402926066 | 0.5924545602816863 |
| larger_high_contrast_epsr6 | global_delay | 0.5119171157297535 | 0.5119171157297535 |

## Interpretation

A constrained time-delay phase ramp does not explain the fresh-case mismatch.
Global delay is neutral, receiver-specific delays slightly help only one
high-error case, and no delay model reaches the strict gate.

## Decision

Keep the project-core bridge blocked. The next BEM operator change should
target geometry/material Green-function structure or source/receiver aperture
modeling rather than a pure timing-delay phase ramp. Do not promote this branch
to 3D validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_time_delay_operator_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_fresh_case_time_delay_operator_audit.png
2896x842, dynamic range=255
```
