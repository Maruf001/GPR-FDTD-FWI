# BEM Experiment 184: Layered Payload Shell-Support Margin Audit

Date: 2026-06-28

## Purpose

Quantify the acceptance margin for each row in the validated local 2D BEM/FDTD
shell-support contract.

Runs `181`-`183` established the current positive and negative-control contract
package. This run asks whether the accepted cases are comfortably below the
`0.75` leave-one-scan L2 gate or whether the contract is narrow and
near-boundary.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/184_project_core_bem_layered_payload_shell_support_margin_audit
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_margin_cases.csv
data/project_core_bem_layered_payload_shell_support_margin_groups.csv
data/project_core_bem_layered_payload_shell_support_margin_audit_summary.json
figures/project_core_bem_layered_payload_shell_support_margin_audit.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_MARGIN_AUDIT.md
scripts/run_project_core_bem_layered_payload_shell_support_margin_audit.py
scripts/test_project_core_bem_layered_payload_shell_support_margin_audit.py
```

## Result

```text
case count:                         11
pass count:                         11
acceptance L2 gate:                 0.75
tight-margin threshold:             0.025
tight-margin cases:                 1
worst case:                         larger_radius_epsr9
worst support mode:                 outer_shell_11mm
worst leave-one L2:                 0.7443538860706249
minimum acceptance margin:          0.005646113929375085
median acceptance margin:           0.08277601133664647
targeted stress follow-up ready:    true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

| Evidence set | Cases | Worst L2 | Minimum margin | Tight cases |
| --- | ---: | ---: | ---: | ---: |
| contract_case | 4 | 0.7443538860706249 | 0.005646113929375085 | 1 |
| holdout_shell_case | 4 | 0.7200480775878574 | 0.029951922412142618 | 0 |
| material_shell_case | 3 | 0.7109170307749919 | 0.03908296922500809 | 0 |

## Interpretation

The validated shell-support contract passes all 11 cases, but it is not a broad
high-margin result. The closest case is `larger_radius_epsr9`, which uses
11 mm outer-shell support and sits only `0.005646113929375085` L2 below the
`0.75` gate.

The holdout and material/interface cases have more margin than the original
larger-radius contract case, so the next BEM work should stress that
near-boundary centered larger-radius case rather than widening the claim.

## Decision

Treat the local 2D shell-support contract as valid but narrow.

The next BEM work should stress the larger-radius shell case near the acceptance
boundary before any field transfer, 3D validation, GPU/HPC, field FWI, or
synthetic `outputs/experiments` promotion.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_validator.py
tests/test_project_core_bem_layered_payload_shell_support_validated_contract_sensitivity.py
tests/test_project_core_bem_layered_payload_shell_support_margin_audit.py
11 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_margin_audit.py: pass
tests/test_project_core_bem_layered_payload_shell_support_margin_audit.py: pass
```

Figure check:

```text
2752x851, dynamic range=255
```
