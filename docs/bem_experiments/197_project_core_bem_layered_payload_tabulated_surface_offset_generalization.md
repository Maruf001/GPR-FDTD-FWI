# BEM Experiment 197: Tabulated Surface Offset Generalization

Date: 2026-06-27

## Purpose

Test whether the 10 mm tabulated field-surface repair from runs `194`-`196`
generalizes across the five 35 mm subcell-offset cases from run `186`.

This run evaluates three support modes for each offset case: full volume,
11 mm binary shell, and 18 mm linear radial shell. It uses the 10 mm plus exact
tabulated surface policy because run `194` found that 19 samples were enough to
close the known deeper-offset gate.

This is a CPU-only local project-core FDTD/BEM adapter run. It does not compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/197_project_core_bem_layered_payload_tabulated_surface_offset_generalization
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_offset_generalization.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_OFFSET_GENERALIZATION.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_offset_generalization.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization.py
```

## Result

```text
offset cases:                       5
support modes:                      3
support rows:                      15
ready rows:                        11
ready cases:                        5
all cases ready:                    true
surface samples per case:          19
best case:                          z_plus_2p5mm
best support mode:                  outer_shell_18mm_linear_radial
best leave-one L2:                  0.6131125861743153
worst best case:                    z_minus_2p5mm
worst best support mode:            outer_shell_11mm_binary
worst best leave-one L2:            0.650662226077945
worst best acceptance margin:       0.099337773922055
generalization ready:               true
generalized repair validation ready:true
contract refresh ready:             false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

Best support per case:

| Case | Best support | Leave-one L2 | Ready |
| --- | --- | ---: | --- |
| centered_x130_z090 | outer_shell_18mm_linear_radial | 0.6276970918101258 | true |
| x_minus_2p5mm | outer_shell_18mm_linear_radial | 0.6266676702265497 | true |
| x_plus_2p5mm | outer_shell_18mm_linear_radial | 0.6200293616121269 | true |
| z_minus_2p5mm | outer_shell_11mm_binary | 0.650662226077945 | true |
| z_plus_2p5mm | outer_shell_18mm_linear_radial | 0.6131125861743153 | true |

## Interpretation

The 10 mm tabulated field-surface policy generalizes across the 35 mm
subcell-offset family tested here. This is stronger than run `194`: the repair
is not only a rescue of the single deeper-offset failure. All five offset cases
have at least one ready shell support, and the worst best-case margin remains
about `0.0993` L2 below the `0.75` acceptance gate.

This remains a tabulated-surface result. It supports a practical local 2D
BEM/FDTD repair path, not an analytic BEM replacement and not a field or 3D
claim.

## Decision

Treat run `197` as a candidate generalized tabulated-surface repair across the
35 mm offset family. Add validator and sensitivity guards before any claim
refresh. Keep analytic contract refresh, field transfer, 3D validation,
GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization.py
4 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_offset_generalization.png
2572x868, dynamic range=255
```
