# BEM Experiment 175: Layered Payload Larger-Radius Refined Shell Support Audit

Date: 2026-06-28

## Purpose

Refine the shell-support repair around the near miss from run `174`.

Run `174` showed that a 10 mm outer shell improved the 35 mm larger-radius case
from leave-one L2 `0.7745663063852277` to `0.7503674453090535`, just above the
`0.75` gate. This run tests shell thicknesses from 8 mm to 14 mm at 1 mm
resolution.

This run reruns one local CPU project-core FDTD case. It does not compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/175_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_refined_shell_support_rows.csv
data/project_core_bem_layered_payload_larger_radius_refined_shell_support_best_payload_arrays.npz
data/project_core_bem_layered_payload_larger_radius_refined_shell_support_audit_summary.json
figures/project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_REFINED_SHELL_SUPPORT_AUDIT.md
scripts/run_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py
scripts/run_project_core_bem_layered_payload_larger_radius_shell_support_audit.py
scripts/test_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py
```

## Result

```text
refined support modes:               8
ready support modes:                 2
acceptance L2 gate:                  0.75
best support mode:                   outer_shell_11mm
best shell thickness:                0.011 m
best active target cells:            574
volume-full leave-one L2:            0.7745663063852277
coarse best leave-one L2:            0.7503674453090535
best leave-one L2:                   0.7443538860706249
best vs volume improvement:          0.030212420314602806
best vs coarse improvement:          0.006013559238428612
gate margin:                         0.005646113929375085
refined shell support ready:         true
corrected ladder resynthesis ready:  true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
```

| Support mode | Shell thickness | Active cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | --- |
| volume_full | 0.0 | 1013 | 0.5723932793988704 | 0.7745663063852277 | false |
| outer_shell_08mm | 0.008 | 436 | 0.5543627449197203 | 0.7551857167030698 | false |
| outer_shell_09mm | 0.009 | 489 | 0.5574410483010642 | 0.7622215857968135 | false |
| outer_shell_10mm | 0.01 | 524 | 0.5497397130195996 | 0.7503674453090535 | false |
| outer_shell_11mm | 0.011 | 574 | 0.5435764558982101 | 0.7443538860706249 | true |
| outer_shell_12mm | 0.012 | 592 | 0.5449013627080745 | 0.7460439721118112 | true |
| outer_shell_13mm | 0.013 | 638 | 0.5496231916460649 | 0.7556627323984473 | false |
| outer_shell_14mm | 0.014 | 664 | 0.5727068465348235 | 0.7719110412944218 | false |

## Interpretation

The refined shell-support branch closes the larger-radius gate for the tested 35
mm case. The best repair is an 11 mm outer shell, which keeps 574 of the 1013
target cells and reaches leave-one L2 `0.7443538860706249`.

The passing window is narrow: 11 mm and 12 mm pass, while 10 mm and 13 mm do
not. This supports shell-style target support as a candidate repair, but the
repair should be synthesized into the corrected extended ladder before any
claim is promoted.

## Decision

Use the 11 mm shell-support row as the candidate repair for the larger-radius
case in the next corrected ladder synthesis.

Keep project-core bridge promotion, field transfer, 3D validation, GPU/HPC, and
field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_shell_support_audit.py
tests/test_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py: pass
```

Figure check:

```text
2914x755, dynamic range=255
```
