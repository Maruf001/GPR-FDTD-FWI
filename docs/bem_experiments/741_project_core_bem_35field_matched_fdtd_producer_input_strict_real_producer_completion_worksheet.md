# BEM Experiment 741: Strict Real-Producer Completion Worksheet

Date: 2026-07-01

## Purpose

Convert the aggregate strict real-producer frontier into a per-file completion
worksheet.

This run does not execute FDTD, create real BEM/FDTD evidence, run 3D
validation, launch GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/741_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_completion_worksheet
```

## Result

```text
producer files:                       2
required rows:                        558
exact contract hashes ready:          558
strict contract-hash errors:          0
missing solver-status cells:          558
missing solver-log-hash cells:        558
missing real-FDTD-export flags:       558
missing returned-value cells:         558
total missing real-data cells:        2232
live files present:                   0
strict-acceptance-ready files:        0
real-evidence-ready files:            0
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
```

Each file has 279 required rows. For each row, the producer must provide real
solver status, a real solver log hash, a real FDTD export flag, and the returned
value for that file type.

## Decision

Use this worksheet as the producer-facing completion checklist. Keep real
BEM/FDTD comparison blocked until both live producer files pass strict
acceptance with real values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_completion_worksheet.py
3 passed
```

