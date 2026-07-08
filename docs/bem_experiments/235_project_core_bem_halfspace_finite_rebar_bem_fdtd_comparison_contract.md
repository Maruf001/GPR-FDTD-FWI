# BEM Experiment 235: Half-Space Finite-Rebar BEM/FDTD Comparison Contract

Date: 2026-06-28

## Purpose

Define the contract for a future matched BEM/FDTD comparison from the guarded
scalar finite-rebar half-space package.

Run `234` clarified that the current package supports a scalar coupling proxy,
not a real FDTD-validated or full 3D Maxwell BEM claim. This run turns that
boundary into a concrete comparison contract: what geometry, material, source,
receiver, frequency, observable, normalization, schema, and acceptance metrics
must match before comparison is meaningful.

This is a CPU-only contract run. It does not run FDTD, compare real paired
files, implement full 3D Maxwell BEM, run inversion, launch GPU/HPC work, run
field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/235_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_comparison_schema_columns.csv
data/project_core_bem_halfspace_finite_rebar_comparison_requirements.csv
data/project_core_bem_halfspace_finite_rebar_comparison_acceptance_metrics.csv
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_COMPARISON_CONTRACT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
requirements:                       14
ready / implementation / blocked:   9 / 3 / 2
blocking not ready:                 4
schema columns:                     31
acceptance metrics:                 6
comparison contract ready:          true
BEM exporter ready:                 false
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The contract-ready requirements are:

| Contract item | Purpose |
| --- | --- |
| Geometry lock | Same finite-rebar and receiver-line geometry |
| Material lock | Same half-space material convention |
| Source/receiver lock | Same source/receiver height and receiver keys |
| Frequency-grid lock | Same nine frequency keys |
| Observable lock | Complex scattered field after target-background subtraction |
| Normalization and phase lock | Explicit time-zero and amplitude references |
| BEM scalar output schema | Required BEM frequency-output columns |
| FDTD frequency output schema | Required FDTD frequency-output columns |
| Comparison output schema | Required paired residual-output columns |

The four blocking gaps are BEM exporter alignment, FDTD frequency extraction,
threshold calibration, and absent real paired BEM/FDTD files.

## Interpretation

The matched comparison is now specified as a contract. Geometry, material,
source/receiver keys, frequency keys, observable, normalization, output schemas,
and acceptance metrics are explicit.

Actual comparison remains blocked. The current package has no BEM exporter in
the comparison schema, no matched FDTD frequency extraction, no calibrated
comparison thresholds, and no real paired files.

## Decision

Use run `235` as the implementation target for a future scalar BEM/FDTD
comparison. The next BEM task can validate and stress-test this contract. Do not
claim real BEM/FDTD agreement, 3D validation, inversion, field transfer,
GPU/HPC readiness, or field FWI from the contract alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_comparison_contract.py: pass
```

Figure check:

```text
3005x843, dynamic range=255
```
