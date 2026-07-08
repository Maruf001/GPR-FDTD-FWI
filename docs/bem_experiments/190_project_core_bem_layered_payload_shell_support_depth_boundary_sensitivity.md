# BEM Experiment 190: Shell-Support Depth Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `189` depth-boundary validator with damaged boundary
variants.

Run `189` showed that the exact run `188` synthesis is consumer-ready. This run
checks the negative-control side: damaged boundary syntheses should fail.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/190_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity_scenarios.csv
data/project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity_summary.json
figures/project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_DEPTH_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py
scripts/test_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py
```

## Result

```text
scenarios:                         9
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        8
observed failure scenarios:        8
unexpected outcomes:               0
sensitivity ready:                 true
depth robust shell rule ready:     false
field transfer ready:              false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

| Scenario | Expected pass | Observed pass | Failed checks |
| --- | --- | --- | --- |
| exact_depth_boundary | true | true | none |
| missing_known_depth_failure | false | false | subcell_shell_case_count_matches_summary; known_depth_failure_is_present; known_depth_failure_has_negative_margin |
| known_failure_margin_positive | false | false | known_depth_failure_has_negative_margin |
| repair_support_marked_ready | false | false | repair_ready_support_count_is_zero |
| depth_robust_rule_marked_ready | false | false | depth_robust_rule_remains_blocked |
| boundary_synthesis_not_ready | false | false | boundary_synthesis_marked_ready |
| field_transfer_marked_ready | false | false | field_3d_gpu_remain_blocked |
| validated_contract_count_mismatch | false | false | validated_contract_case_count_matches_summary |
| subcell_count_mismatch | false | false | subcell_shell_case_count_matches_summary |

## Interpretation

The depth-boundary validator accepts the exact synthesis and rejects all damaged
variants: missing known failure, positive failure margin, ready repair support,
depth-robust rule marked ready, boundary not ready, field transfer marked ready,
and count drift.

This gives the BEM depth-boundary package both positive and negative-control
coverage.

## Decision

Use runs `188`-`190` as the current BEM shell-support depth-boundary guard
package.

Keep the depth-robust shell rule, field transfer, 3D validation, GPU/HPC, and
field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_validator.py
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py
8 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py: pass
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_sensitivity.py: pass
```

Figure check:

```text
2717x842, dynamic range=255
```
