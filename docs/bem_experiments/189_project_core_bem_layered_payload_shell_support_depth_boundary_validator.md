# BEM Experiment 189: Shell-Support Depth Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `188` depth-boundary synthesis from a consumer perspective.

Run `188` made the known deeper-offset failure explicit. This run checks that a
downstream consumer preserves the scoped 11-case contract, the known
`z_plus_2p5mm` failure, the negative failure margin, zero ready repair supports,
and blocked field/3D/GPU states.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/189_project_core_bem_layered_payload_shell_support_depth_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_depth_boundary_validation_checks.csv
data/project_core_bem_layered_payload_shell_support_depth_boundary_validator_summary.json
figures/project_core_bem_layered_payload_shell_support_depth_boundary_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_DEPTH_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py
scripts/test_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
known depth failure:                z_plus_2p5mm
depth robust shell rule ready:      false
boundary validation ready:          true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Check | Expected | Observed | Passes |
| --- | --- | --- | --- |
| validated_contract_case_count_matches_summary | 11 | 11 | true |
| subcell_shell_case_count_matches_summary | 5 | 5 | true |
| known_depth_failure_is_present | z_plus_2p5mm | z_plus_2p5mm | true |
| known_depth_failure_has_negative_margin | < 0 | -0.004962847002872417 | true |
| repair_ready_support_count_is_zero | 0 | 0 | true |
| depth_robust_rule_remains_blocked | false | false | true |
| boundary_synthesis_marked_ready | true | true | true |
| field_3d_gpu_remain_blocked | false | false | true |

## Interpretation

The depth-boundary synthesis is internally consistent and consumer-ready. The
11 accepted contract cases remain scoped, the deeper +2.5 mm failure is present
with negative margin, repair-ready supports remain zero, and field/3D/GPU
promotions remain blocked.

## Decision

Use run `188` as the BEM shell-support depth-boundary synthesis and run `189` as
its consumer validator.

Do not widen the shell-support claim or promote field transfer, 3D validation,
GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py: pass
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py: pass
```

Figure check:

```text
2537x823, dynamic range=255
```
