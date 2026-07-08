# BEM Experiment 219: 2D Support To 3D FDTD Alignment Validator

Date: 2026-06-28

## Purpose

Validate the run `218` 2D-support to 3D-FDTD alignment audit from a consumer
perspective.

This run does not launch 3D FDTD, run a real BEM/FDTD comparison, compare
against field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/219_project_core_bem_2d_support_to_3d_fdtd_alignment_validator
```

Key artifacts:

```text
data/project_core_bem_2d_support_to_3d_fdtd_alignment_validation_checks.csv
data/project_core_bem_2d_support_to_3d_fdtd_alignment_validator_summary.json
figures/project_core_bem_2d_support_to_3d_fdtd_alignment_validator.png
docs/PROJECT_CORE_BEM_2D_SUPPORT_TO_3D_FDTD_ALIGNMENT_VALIDATOR.md
scripts/run_project_core_bem_2d_support_to_3d_fdtd_alignment_validator.py
scripts/test_project_core_bem_2d_support_to_3d_fdtd_alignment_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
direct 3D promotion blockers:       6
direct 2D-to-3D promotion ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms the 10-item alignment table, the guarded but bounded 2D
support claim, the six named direct-promotion blockers, the handoff-ready
external-return route, absent real 3D FDTD data, and blocked downstream states.

## Interpretation

The run `218` alignment audit is internally consistent. It is now positively
validated, but not yet stress-tested by negative controls.

## Decision

Use run `219` as the positive validator for the 2D-support to 3D-FDTD alignment
boundary.

Run sensitivity testing before treating this alignment boundary as fully
guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_2d_support_to_3d_fdtd_alignment_validator.py: pass
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_validator.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```
