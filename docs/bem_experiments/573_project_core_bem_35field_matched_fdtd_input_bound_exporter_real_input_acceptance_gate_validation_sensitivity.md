# BEM Experiment 573: Matched-FDTD Input-Bound Exporter Real Input Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `572` validator with controlled damage to the run `571`
acceptance-gate artifacts.

This run checks that the validator fails when file shape, row counts, column
gates, evidence flags, command execution state, downstream readiness, figure
paths, or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/573_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   11
expected pass cases:                 1
expected fail cases:                 10
actual pass cases:                   1
actual fail cases:                   10
unexpected cases:                    0
damaged cases:                       10
ready for exporter execution:         false
ready for real BEM/FDTD comparison:  false
ready for 3D validation claim:       false
ready for GPU/HPC:                  false
ready for field transfer:            false
ready for field FWI:                 false
```

The exact source state passes. Damaged states fail for:

```text
source readiness removal
missing file gate
required row-count drift
missing column gate
premature input acceptance
premature command execution
premature accepted-return promotion
premature BEM/FDTD comparison promotion
missing figure
missing script snapshots
```

## Interpretation

The input acceptance-gate validator is sensitive to the intended failure modes.
It cannot accidentally promote blank templates, partial inputs, command strings,
or damaged artifacts into BEM/FDTD comparison evidence.

## Decision

Keep the BEM/FDTD comparison blocked until real matched-FDTD input files are
present, accepted by the gate, and exported into accepted return files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
