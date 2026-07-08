# BEM Experiment 186: Larger-Radius Sub-Cell Offset Stress

Date: 2026-06-28

## Purpose

Test the near-boundary 35 mm larger-radius shell-support case with small
target-center offsets.

Run `185` showed that sub-millimeter shell-thickness tuning does not improve
the 11 mm shell boundary row. This run changes the target center by +/-2.5 mm
in `x` and `z` to test whether the issue is depth/placement sensitive.

This run reruns local CPU project-core FDTD cases through the BEM adapter. It
does not compare against field data, launch GPU/HPC work, run 3D validation, or
run field FWI.

## Output

```text
outputs/bem_experiments/186_project_core_bem_layered_payload_larger_radius_subcell_offset_stress
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_subcell_offset_rows.csv
data/project_core_bem_layered_payload_larger_radius_subcell_offset_worst_payload_shapes.csv
data/project_core_bem_layered_payload_larger_radius_subcell_offset_stress_summary.json
data/project_core_bem_layered_payload_larger_radius_subcell_offset_worst_payload_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_subcell_offset_stress.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_SUBCELL_OFFSET_STRESS.md
scripts/run_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py
scripts/test_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py
```

## Result

```text
offset cases:                       5
support rows:                       10
shell ready count:                  4
volume ready count:                 0
centered shell L2:                  0.7443538860706249
centered shell margin:              0.005646113929375085
worst shell case:                   z_plus_2p5mm
worst shell L2:                     0.7549628470028724
worst shell margin:                 -0.004962847002872417
best shell case:                    z_minus_2p5mm
best shell L2:                      0.734539466050683
best shell margin:                  0.015460533949317012
sub-cell shell ready:               false
sub-cell worsens boundary:          true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Case | Volume leave-one L2 | Shell leave-one L2 | Shell ready |
| --- | ---: | ---: | --- |
| centered_x130_z090 | 0.7745663063852277 | 0.7443538860706249 | true |
| x_minus_2p5mm | 0.7705097798405548 | 0.7458619209366606 | true |
| x_plus_2p5mm | 0.7639019524594736 | 0.7397350154139903 | true |
| z_minus_2p5mm | 0.7510327064450306 | 0.734539466050683 | true |
| z_plus_2p5mm | 0.7847859895257936 | 0.7549628470028724 | false |

## Interpretation

The 11 mm shell rule is not robust to small depth shifts. Four of five shell
rows pass, but the deeper +2.5 mm offset fails with leave-one L2
`0.7549628470028724`. The shallower -2.5 mm offset improves to
`0.734539466050683`, so depth placement is now the limiting model/grid behavior.

## Decision

Do not widen the 11 mm shell-support contract from the current evidence.

Target depth-sensitive model/grid refinement next, especially the deeper 35 mm
offset. Keep field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py
tests/test_project_core_bem_layered_payload_larger_radius_submillimeter_shell_margin_stress.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py: pass
```

Figure check:

```text
3004x820, dynamic range=255
```
