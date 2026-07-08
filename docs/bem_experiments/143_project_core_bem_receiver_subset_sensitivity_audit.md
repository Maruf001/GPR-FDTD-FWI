# BEM Experiment 143: Receiver-Subset Sensitivity Audit

Date: 2026-06-27

## Purpose

Check whether the scaled project-core BEM/FDTD bridge only fails because of
specific receiver rows.

Run `142` showed receiver-local residual concentration after the best
phase-corrected separable scaling. This run tests selected receiver subsets to
see whether dropping high-residual receivers can make the comparison pass.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/143_project_core_bem_receiver_subset_sensitivity_audit
```

Key artifacts:

```text
data/project_core_bem_receiver_subset_sensitivity_rows.csv
data/project_core_bem_receiver_subset_sensitivity_audit_summary.json
figures/project_core_bem_receiver_subset_sensitivity_audit.png
docs/PROJECT_CORE_BEM_RECEIVER_SUBSET_SENSITIVITY_AUDIT.md
scripts/run_project_core_bem_receiver_subset_sensitivity_audit.py
scripts/test_project_core_bem_receiver_subset_sensitivity_audit.py
```

## Result

```text
best candidate:                    separable_receiver_frequency_complex_scale
scenarios:                         5
full aperture relative L2:         0.117062890994582
full aperture passes gate:         false
passing post-hoc subsets:          3
best subset:                       only_passing_receivers_1_4_5
best subset relative L2:           0.08606518727283405
edge-drop subset passes gate:      true
post-hoc receiver subset promoted: false
project-core bridge ready:         false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Receiver subset table:

| Scenario | Included receivers | Excluded receivers | Excluded residual energy | Relative L2 | Passes gate |
| --- | --- | --- | ---: | ---: | --- |
| all_receivers | 0;1;2;3;4;5;6 |  | 0.0 | 0.117062890994582 | false |
| drop_top_receiver_6 | 0;1;2;3;4;5 | 6 | 0.22944615703970803 | 0.10899321819765909 | false |
| drop_edge_receivers_0_6 | 1;2;3;4;5 | 0;6 | 0.4414221920328564 | 0.09909330221470856 | true |
| drop_top3_residual_receivers_6_0_3 | 1;2;4;5 | 0;3;6 | 0.6414922156373816 | 0.09017485138990873 | true |
| only_passing_receivers_1_4_5 | 1;4;5 | 0;2;3;6 | 0.7617432321421918 | 0.08606518727283405 | true |

## Interpretation

Receiver exclusion can make selected post-hoc subsets pass the `0.1` gate.
Dropping both edge receivers passes narrowly at `0.09909330221470856`, and
more aggressive exclusions pass more clearly.

This is diagnostic evidence for receiver-local residual structure, not a valid
bridge promotion. The full aperture still fails, and the passing subsets are
defined after seeing the residual pattern.

## Decision

Do not promote a receiver-subset bridge from post-hoc exclusions. Use this
result to focus the next adapter work on receiver-edge modeling and aperture
consistency before any 3D validation, GPU/HPC escalation, or field FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_receiver_subset_sensitivity_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_receiver_subset_sensitivity_audit.png
2284x846, dynamic range=255
```
