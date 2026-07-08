# BEM Experiment 215: Grid-15 Shell-11 Claim-Boundary Refresh

Date: 2026-06-28

## Purpose

Refresh the practical BEM claim boundary with the guarded 15 mm grid-only,
11 mm shell support contract from runs `212`-`214`.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/215_project_core_bem_grid15_shell11_claim_boundary_refresh
```

Key artifacts:

```text
data/project_core_bem_grid15_shell11_claim_boundary_rows.csv
data/project_core_bem_grid15_shell11_claim_boundary_summary.json
figures/project_core_bem_grid15_shell11_claim_boundary_refresh.png
docs/PROJECT_CORE_BEM_GRID15_SHELL11_CLAIM_BOUNDARY_REFRESH.md
scripts/run_project_core_bem_grid15_shell11_claim_boundary_refresh.py
scripts/test_project_core_bem_grid15_shell11_claim_boundary_refresh.py
```

## Result

```text
claims:                             5
ready claims:                       2
blocked claims:                     3
recommended policy count:           1
recommended practical policy:       grid15_shell11_tabulated_surface_offset_repair
recommended surface policy:         grid_15mm_only
recommended support mode:           outer_shell_11mm_binary
recommended sample count:           13
recommended worst leave-one L2:     0.6083307089797199
recommended acceptance margin:      0.14166929102028014
claim boundary refresh ready:       true
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The refreshed practical BEM claim is now:

```text
grid_15mm_only + outer_shell_11mm_binary
```

for the tested local 2D 35 mm offset family.

## Interpretation

The prior BEM claim identified `grid_15mm_only` as the practical surface policy.
This run tightens that claim by making the support mode explicit. The 18 mm
linear radial shell remains a guarded alternative, but it is not recommended
because its worst-case leave-one L2 is higher than the 11 mm binary shell.

Volume support and a per-case support router are both blocked. Field transfer,
3D validation, GPU/HPC, field FWI, and analytic replacement also remain blocked.

## Decision

Use run `215` as the refreshed support-specific BEM claim boundary, pending
validator and sensitivity guards.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_shell11_claim_boundary_refresh.py
4 passed
```

Python compile check:

```text
run_project_core_bem_grid15_shell11_claim_boundary_refresh.py: pass
tests/test_project_core_bem_grid15_shell11_claim_boundary_refresh.py: pass
```

Figure check:

```text
2716x840, dynamic range=255
```
