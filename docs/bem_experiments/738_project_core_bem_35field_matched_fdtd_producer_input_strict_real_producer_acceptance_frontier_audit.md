# BEM Experiment 738: Strict Real-Producer Acceptance Frontier Audit

Date: 2026-07-01

## Purpose

Convert the strict-template dry run and synthetic positive control into a real
producer acceptance frontier.

Run `732` showed that the strict contract hashes are correct but real producer
data are missing. Run `735` showed that the same strict path accepts complete
output-local synthetic files. This run combines those facts into the exact
remaining requirements for real BEM/FDTD comparison evidence.

No FDTD, real BEM/FDTD comparison, 3D validation, GPU/HPC work, field transfer,
or field FWI is executed.

## Output

```text
outputs/bem_experiments/738_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_error_family_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_action_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit.png
```

## Result

```text
required live producer files:          2
live producer files present:           0
required rows:                         558
exact contract hashes ready:           558
strict contract-hash errors:           0
remaining real-data errors:            2232
error families:                        5
real solver provenance errors:         1116
real FDTD export flag errors:          558
returned FDTD value errors:            558
synthetic accepted files:              2
synthetic accepted rows:               558
completed actions now:                 2 / 7
real evidence ready files:             0
real BEM/FDTD comparison ready:        false
3D validation claim ready:             false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

## Interpretation

The strict acceptance path is not the blocker anymore. Exact contract hashes
are already closed, and the synthetic positive control proves that complete
files pass. The blocker is now concrete real producer output: two live files
must be returned with real solver status, real solver log hashes, real FDTD
export flags, returned source hashes, and returned scattered-norm values.

## Decision

Use this run as the current BEM real-producer acceptance frontier. Keep real
BEM/FDTD comparison, 3D validation, GPU/HPC, field transfer, and field FWI
blocked until both live producer files pass strict acceptance with real values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit.py
3 passed
```

