# BEM Experiment 325: Receiver-Operator Conditioning Attribution Validator

Date: 2026-06-28

## Purpose

Validate the saved run `324` receiver-operator conditioning attribution audit
from artifacts.

This validator checks that the no-conditioner-repair conclusion is reproducible
from saved tables before the BEM branch moves to another next step.

This is an artifact-only validator. It does not run a new BEM solve, run FDTD,
launch GPU/HPC work, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/325_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_validator_summary.json
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_CONDITIONING_ATTRIBUTION_VALIDATOR.md
```

## Result

```text
validation checks:                  6
passed checks:                      6
failed checks:                      0
validation ready:                   true
operator frequency rows:            90
operator models:                    10
pass-all models:                    2
max condition number:               14.402570318619736
rows above condition threshold:     0
instability explained by condition: false
physical operator claim ready:      false
field transfer ready:               false
GPU/HPC ready:                      false
field FWI ready:                    false
```

## Interpretation

Run `324` validates as a conditioning-attribution audit. The saved receiver
operator design matrices remain well below the condition threshold, so the
coefficient instability from run `321` is not explained by condition number
alone.

## Decision

Use runs `324-325` as the guarded no-conditioner-repair block. The next BEM
branch should not focus on condition-number repair alone. Physical BEM/FDTD
agreement, 3D validation, field transfer, GPU/HPC, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_audit.py
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_conditioning_attribution_validator.py

6 passed
```

Figure validation:

```text
3365x897, dynamic range=255
```
