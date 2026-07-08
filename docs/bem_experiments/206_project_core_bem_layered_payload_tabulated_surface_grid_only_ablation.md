# BEM Experiment 206: Tabulated Surface Grid-Only Ablation

Date: 2026-06-28

## Purpose

Test whether the tabulated-surface BEM repair needs exact source/receiver
x-positions inserted into the field table, or whether a cheaper uniform
grid-only table is enough for the five tested 35 mm offset cases.

This run reruns local CPU project-core FDTD/BEM adapter cases. It does not
compare against field data, launch GPU/HPC work, run 3D validation, run field
FWI, or promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/206_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_policy_summary.csv
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_GRID_ONLY_ABLATION.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation.py
```

## Result

```text
offset cases:                                5
support modes:                               3
surface policies:                            8
support/policy rows:                         120
ready support/policy rows:                   55
all-case-ready policies:                     5
grid-only all-case-ready policies:           3
cheapest all-case-ready policy:              grid_15mm_only
cheapest all-case-ready policy kind:         grid_only
cheapest all-case-ready max sample count:    13
cheapest all-case-ready worst best L2:       0.6083307089797199
cheapest all-case-ready margin:              0.14166929102028014
10 mm plus exact all-case ready:             true
10 mm plus exact max sample count:           19
lower-sample than 10 mm plus exact ready:    true
lower-sample ready policy:                   grid_15mm_only
grid-only repair ready:                      true
best grid-only policy:                       grid_15mm_only
best overall policy:                         grid_5mm_only
best overall leave-one L2:                   0.5651855941104873
analytic contract refresh ready:             false
field transfer ready:                        false
3D validation ready:                         false
GPU work ready:                              false
field FWI ready:                             false
```

Policy summary:

| Policy | Kind | Max samples | Ready cases | Worst best case | Worst best support | Worst best L2 | Margin | All cases ready |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| exact source/receiver only | exact only | 10 | 0 | z_minus_2p5mm | volume_full | 1.096856452174814 | -0.3468564521748141 | false |
| 20 mm grid only | grid only | 10 | 0 | z_minus_2p5mm | volume_full | 1.0308329002503434 | -0.28083290025034335 | false |
| 20 mm plus exact | grid plus exact | 14 | 0 | z_minus_2p5mm | outer_shell_11mm_binary | 0.8612125686585872 | -0.1112125686585872 | false |
| 15 mm grid only | grid only | 13 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.6083307089797199 | 0.14166929102028014 | true |
| 15 mm plus exact | grid plus exact | 23 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.6075420339182941 | 0.1424579660817059 | true |
| 10 mm grid only | grid only | 19 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.650662226077945 | 0.099337773922055 | true |
| 10 mm plus exact | grid plus exact | 19 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.650662226077945 | 0.099337773922055 | true |
| 5 mm grid only | grid only | 37 | 5 | z_minus_2p5mm | outer_shell_11mm_binary | 0.5917389381889764 | 0.15826106181102362 | true |

## Interpretation

Exact source/receiver insertion is not required for this tested offset family.
The 15 mm grid-only table passes every offset case with 13 samples, while the
previous practical policy from run `203`, 10 mm plus exact, uses 19 samples.

The 20 mm grid-only and 20 mm plus-exact policies both fail, so the current
lower-cost boundary is not "as coarse as possible." The useful boundary is now
15 mm grid-only as the cheapest passing policy, with 5 mm grid-only as the
higher-cost accuracy reference.

## Decision

Promote 15 mm grid-only to the current practical tabulated-surface policy for
the tested five-case 35 mm offset family, pending validator and sensitivity
guards. Keep analytic replacement, field transfer, 3D validation, GPU/HPC,
field FWI, and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation.py
5 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_grid_only_ablation.png
3132x922, dynamic range=255
```
