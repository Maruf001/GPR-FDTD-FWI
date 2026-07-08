# BEM Experiment 174: Layered Payload Larger-Radius Shell Support Audit

Date: 2026-06-28

## Purpose

Test whether the 35 mm larger-radius failure improves when the adapter uses
boundary-shell target support instead of the full target volume.

Run `173` showed that the current layered payload adapter passes through a
32.5 mm radius and fails at 35 mm. A boundary element method represents target
interfaces naturally, so this run tests whether shell-focused target support is
a better approximation for the larger target.

This run reruns one local CPU project-core FDTD case. It does not compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/174_project_core_bem_layered_payload_larger_radius_shell_support_audit
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_shell_support_rows.csv
data/project_core_bem_layered_payload_larger_radius_shell_support_best_payload_arrays.npz
data/project_core_bem_layered_payload_larger_radius_shell_support_audit_summary.json
figures/project_core_bem_layered_payload_larger_radius_shell_support_audit.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_SHELL_SUPPORT_AUDIT.md
scripts/run_project_core_bem_layered_payload_larger_radius_shell_support_audit.py
scripts/test_project_core_bem_layered_payload_larger_radius_shell_support_audit.py
```

## Result

```text
support modes:                       6
ready support modes:                 0
acceptance L2 gate:                  0.75
best support mode:                   outer_shell_10mm
best active target cells:            524
volume-full leave-one L2:            0.7745663063852277
best leave-one L2:                   0.7503674453090535
best vs volume improvement:          0.024198861076174194
larger-radius shell support ready:   false
corrected ladder resynthesis ready:  false
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
```

| Support mode | Shell thickness | Active cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | --- |
| volume_full | 0.0 | 1013 | 0.5723932793988704 | 0.7745663063852277 | false |
| outer_shell_02mm | 0.002 | 152 | 0.5559659771996551 | 0.7675904594758513 | false |
| outer_shell_04mm | 0.004 | 264 | 0.565122992999286 | 0.7567716691647545 | false |
| outer_shell_06mm | 0.006 | 348 | 0.5594824911461329 | 0.7605965231562812 | false |
| outer_shell_08mm | 0.008 | 436 | 0.5543627449197203 | 0.7551857167030698 | false |
| outer_shell_10mm | 0.01 | 524 | 0.5497397130195996 | 0.7503674453090535 | false |

## Interpretation

Shell support materially improves the 35 mm case, reducing leave-one-scan L2 by
`0.024198861076174194` relative to full-volume support.

The best row, a 10 mm outer shell, misses the `0.75` gate by only
`0.0003674453090535`. This is a near miss, not a solved gate. It suggests that
larger-target support modeling is the right repair direction, but the current
coarse shell ladder is not sufficient for promotion.

## Decision

Do not promote the extended layered payload ladder.

Refine the shell-support branch around the 8-12 mm shell-thickness region before
deciding whether a shell-style support repair can close the larger-radius
blocker. Keep project-core bridge promotion, field transfer, 3D validation,
GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_transition_sweep.py
tests/test_project_core_bem_layered_payload_larger_radius_shell_support_audit.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_shell_support_audit.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_shell_support_audit.py: pass
```

Figure check:

```text
2950x755, dynamic range=255
```
