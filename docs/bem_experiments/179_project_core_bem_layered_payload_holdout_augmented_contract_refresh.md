# BEM Experiment 179: Layered Payload Holdout-Augmented Contract Refresh

Date: 2026-06-28

## Purpose

Refresh the scoped layered payload contract with the independent holdout
validation evidence from run `178`.

Run `177` recorded the four-case shell-support contract. Run `178` added four
neighboring 35 mm holdout cases using the same 11 mm shell support. This run
synthesizes both evidence sets into one holdout-augmented contract.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/179_project_core_bem_layered_payload_holdout_augmented_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_layered_payload_holdout_augmented_contract_cases.csv
data/project_core_bem_layered_payload_holdout_augmented_contract_refresh_summary.json
figures/project_core_bem_layered_payload_holdout_augmented_contract_refresh.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_HOLDOUT_AUGMENTED_CONTRACT_REFRESH.md
scripts/run_project_core_bem_layered_payload_holdout_augmented_contract_refresh.py
scripts/test_project_core_bem_layered_payload_holdout_augmented_contract_refresh.py
```

## Result

```text
contract cases:                     4
holdout shell cases:                4
total cases:                        8
total passes:                       8
total failures:                     0
acceptance L2 gate:                 0.75
worst case:                         larger_radius_epsr9
worst leave-one L2:                 0.7443538860706249
holdout-augmented contract ready:   true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Evidence set | Case | Support | Shell thickness | Leave-one L2 | Ready |
| --- | --- | --- | ---: | ---: | --- |
| contract_case | shallow_z_epsr9 | volume_full | 0.0 | 0.678333487523724 | true |
| contract_case | larger_radius_epsr9 | outer_shell_11mm | 0.011 | 0.7443538860706249 | true |
| contract_case | low_contrast_epsr7p5 | volume_full | 0.0 | 0.6672239886633535 | true |
| contract_case | high_interface_epsr12 | volume_full | 0.0 | 0.5738072739328918 | true |
| holdout_shell_case | radius35_left_shift_x120 | outer_shell_11mm | 0.011 | 0.6595823083052277 | true |
| holdout_shell_case | radius35_right_shift_x140 | outer_shell_11mm | 0.011 | 0.6382118948201204 | true |
| holdout_shell_case | radius35_shallow_z080 | outer_shell_11mm | 0.011 | 0.7200480775878574 | true |
| holdout_shell_case | radius35_deep_z100 | outer_shell_11mm | 0.011 | 0.7187880423003535 | true |

## Interpretation

The scoped BEM layered-payload contract now includes the original four accepted
cases plus four neighboring 35 mm shell-support holdouts. All eight rows pass
the `0.75` leave-one-scan gate.

This remains a local 2D project-core BEM/FDTD result. It does not establish
measured-field transfer, 3D finite-rebar validity, GPU/HPC readiness, or field
FWI readiness.

## Decision

Record this as the holdout-augmented BEM layered-payload contract.

Keep field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_holdout_validation.py
tests/test_project_core_bem_layered_payload_holdout_augmented_contract_refresh.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_holdout_augmented_contract_refresh.py: pass
tests/test_project_core_bem_layered_payload_holdout_augmented_contract_refresh.py: pass
```

Figure check:

```text
2680x807, dynamic range=255
```
