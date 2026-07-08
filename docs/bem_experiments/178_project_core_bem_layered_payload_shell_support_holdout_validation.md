# BEM Experiment 178: Layered Payload Shell-Support Holdout Validation

Date: 2026-06-28

## Purpose

Validate the 11 mm shell-support repair on neighboring 35 mm larger-radius cases
not used to tune run `175`.

Run `175` tuned the shell-support repair on the centered 35 mm case. Run `176`
used that repair to close the corrected ladder, and run `177` refreshed the
scoped contract. This run checks whether the same 11 mm shell support transfers
to shifted and depth-varied 35 mm cases.

This run reruns local CPU project-core FDTD/BEM adapter comparisons. It does
not compare against field data, run 3D validation, launch GPU/HPC work, or run
field FWI.

## Output

```text
outputs/bem_experiments/178_project_core_bem_layered_payload_shell_support_holdout_validation
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_holdout_rows.csv
data/project_core_bem_layered_payload_shell_support_holdout_worst_payload_arrays.npz
data/project_core_bem_layered_payload_shell_support_holdout_validation_summary.json
figures/project_core_bem_layered_payload_shell_support_holdout_validation.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_HOLDOUT_VALIDATION.md
scripts/run_project_core_bem_layered_payload_shell_support_holdout_validation.py
scripts/test_project_core_bem_layered_payload_shell_support_holdout_validation.py
```

## Result

```text
holdout cases:                       4
support rows:                        8
volume pass count:                   4
shell pass count:                    4
shell failed count:                  0
acceptance L2 gate:                  0.75
worst shell case:                    radius35_shallow_z080
worst shell leave-one L2:            0.7200480775878574
mean shell-vs-volume improvement:    0.009874817016125886
shell holdout validation ready:      true
layered contract generalization:     true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

| Case | Volume L2 | 11 mm shell L2 | Shell ready |
| --- | ---: | ---: | --- |
| radius35_left_shift_x120 | 0.6876057202880246 | 0.6595823083052277 | true |
| radius35_right_shift_x140 | 0.6680475480222039 | 0.6382118948201204 | true |
| radius35_shallow_z080 | 0.6971733270163981 | 0.7200480775878574 | true |
| radius35_deep_z100 | 0.723302995751436 | 0.7187880423003535 | true |

## Interpretation

The 11 mm shell support transfers to all four neighboring 35 mm holdout cases.
The shell support improves three of four holdouts and slightly regresses the
shallower case, but the shallower case still remains below the `0.75` gate.

The full-volume rows also pass all four holdouts. That means the original
centered 35 mm failure is a specific near-boundary case, not a general failure
for all nearby 35 mm geometries.

## Decision

Treat the 11 mm shell-support repair as independently validated for this small
neighboring 35 mm holdout set.

Keep field transfer, 3D validation, GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_contract_refresh.py
tests/test_project_core_bem_layered_payload_shell_support_holdout_validation.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_holdout_validation.py: pass
tests/test_project_core_bem_layered_payload_shell_support_holdout_validation.py: pass
```

Figure check:

```text
3040x770, dynamic range=255
```
