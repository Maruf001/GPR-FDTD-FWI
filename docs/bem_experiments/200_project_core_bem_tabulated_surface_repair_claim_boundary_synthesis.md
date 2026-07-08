# BEM Experiment 200: Tabulated Surface Repair Claim Boundary Synthesis

Date: 2026-06-27

## Purpose

Synthesize the current BEM claim boundary after the guarded tabulated-surface
repair package from runs `194`-`199`.

This is a CPU-only synthesis run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/200_project_core_bem_tabulated_surface_repair_claim_boundary_synthesis
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_repair_claim_boundary_rows.csv
data/project_core_bem_tabulated_surface_repair_claim_boundary_synthesis_summary.json
figures/project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_REPAIR_CLAIM_BOUNDARY_SYNTHESIS.md
scripts/run_project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.py
scripts/test_project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.py
```

## Result

```text
claims:                             5
ready claims:                       3
blocked claims:                     2
offset-family ready:                true
offset-family cases:                5
offset-family worst best L2:        0.650662226077945
offset-family worst best margin:    0.099337773922055
claim-boundary synthesis ready:     true
claim-boundary validation ready:    true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

Claim boundary:

| Claim | Status | Ready | Scope |
| --- | --- | --- | --- |
| Analytic shell-support contract | Scoped ready | true | Local 2D layered payload validated cases only |
| Depth-robust analytic shell rule | Blocked | false | The deeper 35 mm offset remains a known analytic-shell failure |
| Single-case tabulated-surface repair | Guarded ready | true | Specific deeper `z_plus_2p5mm` local 2D repair |
| Offset-family tabulated-surface repair | Guarded ready | true | Local 2D 35 mm offset family with 10 mm tabulated field surface |
| Analytic BEM replacement for tabulated surface | Blocked | false | Not supported by the current low-order analytic basis tests |

## Interpretation

The current defensible BEM result is no longer only a failure boundary. The
tabulated FDTD field-surface path repairs the 35 mm offset family in local 2D
and is guarded by validator and sensitivity runs.

The repair is practical but scoped. It is not an analytic BEM replacement, not a
field-data result, not a 3D result, and not a GPU/HPC-ready path.

## Decision

Use run `200` as the claim-boundary checkpoint. Validate it before using it in
report or presentation text. Keep analytic contract refresh, field transfer,
3D validation, GPU/HPC, field FWI, and synthetic `outputs/experiments`
promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.py
3 passed
```

Figure validation:

```text
project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.png
2591x847, dynamic range=255
```
