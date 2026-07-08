# BEM Experiment 053: Replacement Model Requirements

Date: 2026-06-25

## Purpose

Define the requirements for replacing the project-domain target-cell field table
with BEM-derived fields.

This is a CPU-only design artifact. It does not run FDTD time stepping, field
data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/053_project_core_bem_replacement_model_requirements
```

Key artifacts:

```text
data/project_core_bem_replacement_model_requirements.csv
data/project_core_bem_replacement_model_actions.csv
data/project_core_bem_replacement_model_requirements_summary.json
figures/project_core_bem_replacement_model_requirements.png
docs/PROJECT_CORE_BEM_REPLACEMENT_MODEL_REQUIREMENTS.md
```

## Result

```text
requirements:                       6
blocked requirements:               3
missing requirements:               2
conditional requirements:           1
field claim ready:                  false
3D claim ready:                     false
gpu required:                       false
```

## Interpretation

The project-domain field table remains the active bridge. Raw analytic Green
fields, simple per-source scaling, per-cell finite-domain scaling, and denser
finite-domain scaling do not currently replace it.

## Decision

A BEM-derived replacement must first reproduce project source, finite-domain
boundary, and material conventions, then pass both field-table and scattering
replay gates.

Field and 3D claims remain blocked.

## Validation

```text
python -m py_compile run_project_core_bem_replacement_model_requirements.py
python run_project_core_bem_replacement_model_requirements.py
```

Figure check:

```text
project_core_bem_replacement_model_requirements.png: 1872x842, dynamic range=255
```
