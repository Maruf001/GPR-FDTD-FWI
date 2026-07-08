# BEM Experiment 209: Grid-Only Tabulated Surface Claim Boundary Refresh

Date: 2026-06-28

## Purpose

Refresh the BEM claim boundary after the guarded 15 mm grid-only
tabulated-surface result from runs `206`-`208`.

This is a CPU-only synthesis run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/209_project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh
```

Key artifacts:

```text
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_rows.csv
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_summary.json
figures/project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh.png
docs/PROJECT_CORE_BEM_GRID_ONLY_TABULATED_SURFACE_CLAIM_BOUNDARY_REFRESH.md
scripts/run_project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh.py
scripts/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh.py
```

## Result

```text
claims:                                      6
ready claims:                                2
blocked claims:                              4
recommended practical claim:                 grid15_tabulated_surface_offset_repair
recommended surface policy:                  grid_15mm_only
recommended surface sample count:            13
recommended surface worst best L2:           0.6083307089797199
recommended surface acceptance margin:       0.14166929102028014
grid-only sensitivity ready:                 true
supersedes 10 mm plus exact policy:          true
claim-boundary refresh ready:                true
claim-boundary validation ready:             true
analytic contract refresh ready:             false
field transfer ready:                        false
3D validation ready:                         false
GPU work ready:                              false
field FWI ready:                             false
```

Claim table:

| Claim | Status | Ready | Recommended | Source runs | Metric | Margin |
| --- | --- | --- | --- | --- | ---: | ---: |
| analytic_shell_support_contract | scoped_ready | true | false | 181-183 | 0.7443538860706249 | 0.005646113929375085 |
| grid15_tabulated_surface_offset_repair | guarded_ready_practical_policy | true | true | 206-208 | 0.6083307089797199 | 0.14166929102028014 |
| grid20_tabulated_surface_offset_repair | blocked_too_coarse | false | false | 206-208 | 1.0308329002503434 | -0.28083290025034335 |
| depth_robust_analytic_shell_rule | blocked | false | false | 186-190 | 0.7549628470028724 | -0.004962847002872417 |
| analytic_bem_replacement_for_tabulated_surface | blocked | false | false | 192-193 | 0.6083307089797199 | 0.0 |
| field_transfer_from_grid_only_tabulated_surface | blocked | false | false | 206-208 | 0.6083307089797199 | 0.0 |

## Interpretation

The claim boundary now uses the guarded 15 mm grid-only tabulated surface as
the practical local 2D repair for the tested 35 mm offset family. The previous
10 mm plus-exact practical policy is superseded by a lower-sample grid-only
policy.

The scoped analytic shell-support claim remains ready for its validated local
2D scope. Depth-robust analytic shell behavior, analytic replacement of the
tabulated surface, field transfer, 3D validation, GPU/HPC readiness, and field
FWI remain blocked.

## Decision

Use run `209` as the refreshed BEM claim-boundary synthesis. Validate and
stress-test it before using the refreshed language in downstream reports or
presentation material.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh.py
3 passed
```

Figure validation:

```text
project_core_bem_grid_only_tabulated_surface_claim_boundary_refresh.png
3005x857, dynamic range=255
```
