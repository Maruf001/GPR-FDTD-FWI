# BEM Experiment 220: 2D Support To 3D FDTD Alignment Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `219` 2D-support to 3D-FDTD alignment validator with
damaged alignment summaries.

This run does not launch 3D FDTD, run a real BEM/FDTD comparison, compare
against field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/220_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity
```

Key artifacts:

```text
data/project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity_scenarios.csv
data/project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity_summary.json
figures/project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.png
docs/PROJECT_CORE_BEM_2D_SUPPORT_TO_3D_FDTD_ALIGNMENT_SENSITIVITY.md
scripts/run_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.py
scripts/test_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.py
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
sensitivity ready:                 true
direct 2D-to-3D promotion ready:   false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The exact alignment boundary passes. Damaged cases fail for count drift,
2D-support policy drift, removed direct-promotion blockers, external request
readiness drift, synthetic-return smoke drift, real-data status drift, direct
promotion, real comparison readiness, 3D validation readiness, field transfer,
GPU readiness, field FWI readiness, and a next-action contract change.

## Interpretation

Runs `218`-`220` form a guarded BEM alignment package: the current 2D support
claim is useful but bounded, and the 3D validation path remains the external
paired target/background FDTD return gate.

## Decision

Use runs `218`-`220` as the guarded BEM 2D-support to 3D-FDTD alignment
package.

Keep direct 2D-to-3D promotion, real BEM/FDTD comparison, 3D validation, field
transfer, GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.py
5 passed
```

Python compile check:

```text
run_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.py: pass
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_sensitivity.py: pass
```

Figure check:

```text
3077x878, dynamic range=255
```
