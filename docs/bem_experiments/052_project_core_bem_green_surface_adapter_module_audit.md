# BEM Experiment 052: Green-Surface Adapter Module Audit

Date: 2026-06-25

## Purpose

Audit the reusable helper module `bem_green_surface_adapter.py`.

This is a CPU-only tooling artifact. It does not run FDTD time stepping, field
data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/052_project_core_bem_green_surface_adapter_module_audit
```

Key artifacts:

```text
data/project_core_bem_green_surface_adapter_module_audit.csv
data/project_core_bem_green_surface_adapter_module_audit_summary.json
figures/project_core_bem_green_surface_adapter_module_audit.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_ADAPTER_MODULE_AUDIT.md
```

## Result

```text
module:                             bem_green_surface_adapter.py
synthetic cases:                    2
focused tests passed:               true
gpu required:                       false
```

Focused tests:

```text
tests/test_bem_green_surface_adapter.py
4 passed
```

## Interpretation

The Green-surface scaling and leave-one-source logic now has a small reusable
module with focused tests. This reduces the risk of copy/paste drift in future
BEM adapter runs.

## Decision

Use `bem_green_surface_adapter.py` for future field-surface scaling and
leave-one-source diagnostics instead of duplicating this math in new scripts.

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_adapter_module_audit.py \
  bem_green_surface_adapter.py tests/test_bem_green_surface_adapter.py
python -m pytest tests/test_bem_green_surface_adapter.py -q
python run_project_core_bem_green_surface_adapter_module_audit.py
```

Figure check:

```text
project_core_bem_green_surface_adapter_module_audit.png: 1535x735, dynamic range=255
```
