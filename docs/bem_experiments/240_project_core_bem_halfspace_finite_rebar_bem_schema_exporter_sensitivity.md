# BEM Experiment 240: Half-Space Finite-Rebar BEM Schema Exporter Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the BEM-side schema exporter validator from run `239`.

Run `239` validated the scalar BEM export from run `238`. This run checks
whether the validator rejects controlled damage to the exported table, source
checks, summary counts, and downstream decision flags.

This is a CPU-only sensitivity run. It does not run FDTD, extract FDTD
frequency bins, compare real paired files, implement full 3D Maxwell BEM, run
inversion, launch GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/240_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_SCHEMA_EXPORTER_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         22
expected pass scenarios:           1
expected failure scenarios:        21
observed pass scenarios:           1
observed failure scenarios:        21
unexpected outcomes:               0
sensitivity ready:                 true
exporter guarded:                  true
BEM schema exporter ready:          true
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The exact run `238` export passes. The damaged scenarios fail as expected for:

| Damage family | Validator response |
| --- | --- |
| Export row-count or role-key drift | Rejected |
| Extra schema columns | Rejected |
| Residual-accounting drift | Rejected |
| Nonfinite field values | Rejected |
| Scattered-norm drift | Rejected |
| Geometry, observable, or normalization metadata drift | Rejected |
| Failed source exporter checks | Rejected |
| Summary-count drift | Rejected |
| False exporter, FDTD extraction, real-comparison, 3D, inversion, field, GPU, or field-FWI promotion | Rejected |

## Interpretation

The BEM schema exporter validator accepts the exact run `238` export and rejects
controlled damage to row count, columns, role keys, residual accounting, finite
fields, scattered norm, metadata locks, source checks, summary counts, exporter
readiness, and downstream promotion flags.

## Decision

Use runs `238`-`240` as the guarded BEM-side export package for the scalar
comparison contract. The next useful BEM branch is the FDTD-side frequency
extraction input path. Real comparison, 3D validation, inversion, field
transfer, GPU/HPC readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_sensitivity.py: pass
```

Figure check:

```text
3365x892, dynamic range=255
```
