# BEM Experiment 328: Project-Grid Adapter Lineage Audit

Date: 2026-06-28

## Purpose

Validate the BEM/project-grid adapter lineage that starts at the run `037`
contract.

This run checks the current saved evidence before continuing the adapter branch.
It uses saved BEM artifacts only. It does not run FDTD, launch GPU/HPC work,
use field data, use the synthetic 2D experiment archive, or run field FWI.

## Output

```text
outputs/bem_experiments/328_project_core_bem_project_grid_adapter_lineage_audit
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_lineage_audit_lineage_rows.csv
data/project_core_bem_project_grid_adapter_lineage_audit_guard_rows.csv
data/project_core_bem_project_grid_adapter_lineage_audit_summary.json
figures/project_core_bem_project_grid_adapter_lineage_audit.png
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_LINEAGE_AUDIT.md
```

## Result

```text
lineage rows:                     11
accepted lineage rows:            10
blocked lineage rows:             1
blocked lineage step:             raw_bem_compatible_analytic_field_probe
run 037 contract ready:           true
run 038 smoke ready:              true
raw analytic field adapter ready: false
project-domain surface ready:     true
surface stress ready:             true
current payload contract ready:   true
implementation branch ready:      true
lineage audit ready:              true
guard violations:                 0
field claim ready:                false
3D validation ready:              false
GPU work ready:                   false
field FWI ready:                  false
```

## Interpretation

The run `037` contract was implemented and validated, but not by raw continuous
analytic fields. The accepted branch is project-grid target cells plus
finite-domain or grid-aware target-cell field payloads.

Historical 2D archive, field, 3D, GPU, and FWI claims remain outside the
accepted scope.

## Decision

Use run `328` as the lineage validator for the project-grid adapter branch.
Continue future BEM work from the guarded payload/field-surface adapters, not
from the failed raw analytic-field replacement path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_lineage_audit.py
3 passed
```

Figure validation:

```text
3437x994, dynamic range=255
```
