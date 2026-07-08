# BEM Experiment 185: Larger-Radius Sub-Millimeter Shell Margin Stress

Date: 2026-06-28

## Purpose

Stress-test the near-boundary 35 mm larger-radius shell-support case with shell
thicknesses from 10.00 mm to 12.00 mm in 0.25 mm steps.

Run `184` showed that the current shell-support contract is valid but narrow:
the limiting 35 mm larger-radius row has only `0.005646113929375085` L2 margin
below the `0.75` leave-one-scan gate. This run asks whether sub-millimeter shell
tuning can improve that boundary row.

This run reruns one local CPU project-core FDTD case through the BEM adapter. It
does not compare against field data, launch GPU/HPC work, run 3D validation, or
run field FWI.

## Output

```text
outputs/bem_experiments/185_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_rows.csv
data/project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_best_payload_shapes.csv
data/project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress_summary.json
data/project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_best_payload_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_SUBMILLIMETER_SHELL_MARGIN_STRESS.md
scripts/run_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py
scripts/test_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py
```

## Result

```text
support modes:                       10
shell support modes:                 9
ready support modes:                 6
unique shell active-cell counts:     6
best support mode:                   outer_shell_11p00mm
best shell thickness m:              0.011
best support active cells:           574
volume-full leave-one L2:            0.7745663063852277
previous contract worst L2:          0.7443538860706249
best leave-one L2:                   0.7443538860706249
best acceptance margin:              0.005646113929375085
margin improved vs contract:         false
grid quantization detected:          true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

| Support mode | Shell thickness m | Active cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | --- |
| volume_full | 0.0 | 1013 | 0.5723932793988704 | 0.7745663063852277 | false |
| outer_shell_10p00mm | 0.01 | 524 | 0.5497397130195996 | 0.7503674453090535 | false |
| outer_shell_10p25mm | 0.01025 | 524 | 0.5497397130195996 | 0.7503674453090535 | false |
| outer_shell_10p50mm | 0.0105 | 532 | 0.5490620619530998 | 0.7524349018713278 | false |
| outer_shell_10p75mm | 0.01075 | 548 | 0.5473049538812854 | 0.7498211239389766 | true |
| outer_shell_11p00mm | 0.011 | 574 | 0.5435764558982101 | 0.7443538860706249 | true |
| outer_shell_11p25mm | 0.01125 | 576 | 0.5437716529068228 | 0.7456205800797603 | true |
| outer_shell_11p50mm | 0.0115 | 576 | 0.5437716529068228 | 0.7456205800797603 | true |
| outer_shell_11p75mm | 0.01175 | 592 | 0.5449013627080745 | 0.7460439721118112 | true |
| outer_shell_12p00mm | 0.012 | 592 | 0.5449013627080745 | 0.7460439721118112 | true |

## Interpretation

Sub-millimeter shell tuning does not improve the near-boundary larger-radius
row. The best support remains the 11.00 mm outer shell with leave-one L2
`0.7443538860706249`, exactly matching the previous contract row.

The repeated active-cell counts show grid quantization: 10.00 mm and 10.25 mm
select the same 524 cells, 11.25 mm and 11.50 mm select the same 576 cells, and
11.75 mm and 12.00 mm select the same 592 cells. The limiting behavior is
therefore not solved by sub-grid shell-thickness tweaks.

## Decision

Keep the run `181` larger-radius 11 mm shell row as the current boundary case.
Do not refresh the contract from sub-millimeter shell tuning.

The next BEM stress should target model/grid behavior rather than sub-grid
shell-thickness tweaks. Keep field transfer, 3D validation, GPU/HPC, field FWI,
and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_margin_audit.py
tests/test_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py
8 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py: pass
```

Figure check:

```text
2914x755, dynamic range=255
```
