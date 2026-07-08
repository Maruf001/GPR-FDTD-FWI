# BEM Experiment 239: Half-Space Finite-Rebar BEM Schema Exporter Validator

Date: 2026-06-28

## Purpose

Validate the BEM-side schema export from run `238`.

Run `238` exported scalar BEM background, scattered, and total complex
frequency fields into the run `235` BEM comparison schema. This run checks that
the exported table is internally consistent and still does not imply FDTD
comparison readiness.

This is a CPU-only validator. It does not run FDTD, extract FDTD frequency
bins, compare real paired files, implement full 3D Maxwell BEM, run inversion,
launch GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/239_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_SCHEMA_EXPORTER_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
source export rows:                 351
source schema columns:              10
BEM exporter ready:                 true
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The eight checks confirm:

| Check | Outcome |
| --- | --- |
| Export row count matches the contract | Pass |
| Columns match the BEM-side contract | Pass |
| Background, scattered, and total role key sets are complete | Pass |
| Field values are finite and residual accounting holds | Pass |
| Scattered norm matches the source run | Pass |
| Geometry, observable, and normalization metadata are locked | Pass |
| Source exporter checks all pass | Pass |
| Exporter readiness remains separated from downstream execution | Pass |

## Interpretation

The BEM schema export is internally consistent. Row count, contract columns,
role key sets, finite values, residual accounting, scattered norm, metadata
locks, and source schema checks all pass.

## Decision

Use run `239` as the consumer validator for the BEM-side exporter. The next BEM
step is a negative-control sensitivity run. FDTD extraction, real comparison,
3D validation, inversion, field transfer, GPU/HPC readiness, and field FWI
remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter_validator.py: pass
```

Figure check:

```text
2537x835, dynamic range=255
```
