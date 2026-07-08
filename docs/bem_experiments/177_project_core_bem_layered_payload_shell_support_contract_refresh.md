# BEM Experiment 177: Layered Payload Shell-Support Contract Refresh

Date: 2026-06-28

## Purpose

Refresh the scoped layered payload BEM contract after the shell-repaired ladder
passed.

Run `176` showed that replacing the failed 35 mm full-volume row with the
11 mm outer-shell support row makes all four corrected extended ladder cases
pass the leave-one-scan gate. This run records the resulting accepted scope and
the remaining blocked claims.

This run does not rerun FDTD or BEM solvers, compare against field data, launch
GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/177_project_core_bem_layered_payload_shell_support_contract_refresh
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_contract_cases.csv
data/project_core_bem_layered_payload_shell_support_contract_items.csv
data/project_core_bem_layered_payload_shell_support_contract_refresh_summary.json
figures/project_core_bem_layered_payload_shell_support_contract_refresh.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_CONTRACT_REFRESH.md
scripts/run_project_core_bem_layered_payload_shell_support_contract_refresh.py
scripts/test_project_core_bem_layered_payload_shell_support_contract_refresh.py
```

## Result

```text
case count:                         4
passed cases:                       4
failed cases:                       0
acceptance L2 gate:                 0.75
worst case:                         larger_radius_epsr9
worst leave-one L2:                 0.7443538860706249
accepted contract rows:             5
blocked contract rows:              3
scoped contract refreshed:          true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

Accepted case evidence:

| Case | Support mode | Shell thickness | Leave-one L2 | Ready |
| --- | --- | ---: | ---: | --- |
| shallow_z_epsr9 | volume_full | 0.0 | 0.678333487523724 | true |
| larger_radius_epsr9 | outer_shell_11mm | 0.011 | 0.7443538860706249 | true |
| low_contrast_epsr7p5 | volume_full | 0.0 | 0.6672239886633535 | true |
| high_interface_epsr12 | volume_full | 0.0 | 0.5738072739328918 | true |

Contract boundary:

| Item | Value | Status |
| --- | --- | --- |
| Domain | 2D local project-core air/concrete layered dielectric payload cases | accepted |
| Acceptance gate | leave-one-scan relative L2 <= 0.75 | accepted |
| Standard support rule | full-volume target support for standard 25 mm radius cases | accepted |
| Larger-radius support rule | 11 mm outer-shell support for the 35 mm radius case | accepted |
| Extended ladder result | 4/4 cases pass | accepted |
| Field transfer | not accepted | blocked |
| 3D validation | not accepted | blocked |
| GPU/HPC escalation | not accepted | blocked |

## Interpretation

The BEM layered-payload branch now has a refreshed scoped contract. The adapter
passes the local 2D project-core air/concrete dielectric ladder when standard
targets use full-volume support and the 35 mm larger target uses an 11 mm
outer-shell support.

This does not establish measured-field transfer, 3D finite-rebar validity,
heavy GPU/HPC readiness, or field FWI readiness.

## Decision

Record this as the current scoped BEM layered-payload contract.

Continue with independent validation or a new BEM branch before any field, 3D,
GPU/HPC, or synthetic `outputs/experiments` promotion.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py
tests/test_project_core_bem_layered_payload_shell_support_contract_refresh.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_contract_refresh.py: pass
tests/test_project_core_bem_layered_payload_shell_support_contract_refresh.py: pass
```

Figure check:

```text
2716x793, dynamic range=255
```
