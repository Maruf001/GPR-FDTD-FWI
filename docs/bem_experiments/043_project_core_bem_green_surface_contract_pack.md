# BEM Experiment 043: Green-Surface Contract Pack

Date: 2026-06-25

## Purpose

Turn runs `037`-`042` into the current reusable BEM/project-core adapter
contract.

This is a CPU-only packaging artifact. It does not run FDTD time stepping,
field data, GPU work, FWI, 3D/HPC, neural networks, or the historical
`outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/043_project_core_bem_green_surface_contract_pack
```

Key artifacts:

```text
data/project_core_bem_green_surface_contract_interface.csv
data/project_core_bem_green_surface_contract_gates.csv
data/project_core_bem_green_surface_contract_limits.csv
data/project_core_bem_green_surface_contract_pack_summary.json
figures/project_core_bem_green_surface_contract_pack.png
docs/PROJECT_CORE_BEM_GREEN_SURFACE_CONTRACT_PACK.md
```

## Result

```text
contract ready:                     true
usable bridge:                      project-domain target-cell Green surface
not usable bridge:                  raw continuous analytic/free-space Green fields
interface items:                    7
gates:                              8
numeric gates passed:               4
numeric gates failed:               2
blocked claim gates:                2
gpu required:                       false
```

Gate summary:

| Gate | Run | Value | Status |
| --- | --- | ---: | --- |
| discrete_born_contract | 037 | 0.44601690298659386 | pass |
| adapter_smoke_schema | 038 | 0.44601690298659386 | pass |
| raw_analytic_green_fields | 039 | 0.8309901396143111 | fail |
| analytic_field_map_leave_one_scan | 040 | 0.9869554402632811 | fail |
| project_domain_surface_leave_one_scan | 041 | 0.5573625471027422 | pass |
| project_domain_surface_stress | 042 | 0.5974979747759482 | pass |
| historical_archive_claim |  |  | blocked |
| field_or_3d_claim |  |  | blocked |

## Interpretation

The supported bridge is not raw analytic/BEM-compatible Green fields. The
supported bridge is a project-domain target-cell Green surface coupled to the
discrete scattering operator and validated by held-out scan and stress gates.

## Decision

Use this contract pack as the current BEM/project-core adapter specification.
Do not attach it to historical archive, field, 3D, FWI, or GPU claims until the
listed limits have their own validation gates.

Immediate uncovered limits:

```text
depth shifts
radius changes
offset changes
layered/half-space media
BEM-derived field replacement
3D finite-rebar validation
field provenance closure
```

## Validation

```text
python -m py_compile run_project_core_bem_green_surface_contract_pack.py
python run_project_core_bem_green_surface_contract_pack.py
```

Figure check:

```text
project_core_bem_green_surface_contract_pack.png: 1853x841, dynamic range=255
```
