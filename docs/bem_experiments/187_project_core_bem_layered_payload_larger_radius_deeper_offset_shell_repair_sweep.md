# BEM Experiment 187: Larger-Radius Deeper-Offset Shell Repair Sweep

Date: 2026-06-28

## Purpose

Sweep shell thickness for the failing deeper +2.5 mm 35 mm larger-radius case
from run `186`.

Run `186` showed that the 11 mm shell-support rule fails when the target is
shifted 2.5 mm deeper. This run tests whether thicker shells can repair that
specific failure.

This run reruns one local CPU project-core FDTD case through the BEM adapter. It
does not compare against field data, launch GPU/HPC work, run 3D validation, or
run field FWI.

## Output

```text
outputs/bem_experiments/187_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_best_payload_shapes.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep_summary.json
data/project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_best_payload_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_SHELL_REPAIR_SWEEP.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py
```

## Result

```text
support modes:                       9
ready support modes:                 0
source failed shell L2:              0.7549628470028724
best support mode:                   outer_shell_11mm
best shell thickness m:              0.011
volume-full leave-one L2:            0.7847859895257936
best leave-one L2:                   0.7549628470028724
best acceptance margin:              -0.004962847002872417
best vs original shell improvement:  0.0
deeper offset repaired:              false
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

| Support mode | Shell thickness m | Active cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | --- |
| volume_full | 0.0 | 1016 | 0.5842131837893164 | 0.7847859895257936 | false |
| outer_shell_10mm | 0.01 | 523 | 0.5587579031836243 | 0.7591654029359443 | false |
| outer_shell_11mm | 0.011 | 566 | 0.5530952943599055 | 0.7549628470028724 | false |
| outer_shell_12mm | 0.012 | 597 | 0.5610744988368188 | 0.7570651361078097 | false |
| outer_shell_13mm | 0.013 | 640 | 0.5623254455091424 | 0.7625016537963157 | false |
| outer_shell_14mm | 0.014 | 669 | 0.5781597618038262 | 0.7768291495635734 | false |
| outer_shell_15mm | 0.015 | 706 | 0.5787768818570991 | 0.7793781006218392 | false |
| outer_shell_16mm | 0.016 | 731 | 0.5846376908922377 | 0.7865906385370898 | false |
| outer_shell_18mm | 0.018 | 785 | 0.5888152757255137 | 0.7912632321588797 | false |

## Interpretation

The repair sweep does not recover the deeper +2.5 mm offset. Zero support modes
pass; the best row remains `outer_shell_11mm` at leave-one L2
`0.7549628470028724`, matching the source failed shell. Thicker shells worsen
the fit rather than closing the gate.

## Decision

Keep the deeper +2.5 mm offset as a known local 2D BEM shell-support failure.
Do not refresh the contract with a depth-sensitive shell rule from this sweep.

The next BEM repair must change the model or grid treatment, not shell
thickness alone. Keep field transfer, 3D validation, GPU/HPC, field FWI, and
synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py
tests/test_project_core_bem_layered_payload_larger_radius_subcell_offset_stress.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py: pass
```

Figure check:

```text
2914x773, dynamic range=255
```
