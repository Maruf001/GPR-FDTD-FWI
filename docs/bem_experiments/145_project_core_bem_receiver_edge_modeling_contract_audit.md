# BEM Experiment 145: Receiver-Edge Modeling Contract Audit

Date: 2026-06-27

## Purpose

Define the evidence contract required before a receiver-edge correction can be
promoted.

Runs `142`-`144` diagnosed receiver-local and aperture-position residual
structure. This run separates diagnosis from promotion: it lists what must be
true before receiver-edge modeling can become a valid bridge correction.

This is a CPU-only contract audit. It does not rerun FDTD, rerun BEM, compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/145_project_core_bem_receiver_edge_modeling_contract_audit
```

Key artifacts:

```text
data/project_core_bem_receiver_edge_modeling_contract_rows.csv
data/project_core_bem_receiver_edge_modeling_contract_audit_summary.json
figures/project_core_bem_receiver_edge_modeling_contract_audit.png
docs/PROJECT_CORE_BEM_RECEIVER_EDGE_MODELING_CONTRACT_AUDIT.md
scripts/run_project_core_bem_receiver_edge_modeling_contract_audit.py
scripts/test_project_core_bem_receiver_edge_modeling_contract_audit.py
```

## Result

```text
contract items:                   6
contract passes:                  2
blocking contract items:          4
receiver-edge contract ready:     false
posthoc receiver subset promoted: false
project-core bridge ready:        false
field FWI ready:                  false
GPU/HPC ready:                    false
```

Contract table:

| Contract item | Status | Blocking | Evidence |
| --- | --- | --- | --- |
| full_aperture_must_pass_gate | fail | true | full aperture L2 `0.117062890994582`, gate pass false |
| posthoc_receiver_exclusion_not_allowed | pass | false | posthoc subset promoted false |
| aperture_geometry_localization_available | pass | false | edge plus center residual fraction `0.6414922156373816` |
| edge_correction_must_be_pre_registered | missing | true | no pre-registered edge correction exists in current runs |
| holdout_validation_required | missing | true | receiver subsets that pass are selected after observing residuals |
| frequency_receiver_joint_residual_must_close | fail | true | frequency bins passing `8 / 17`; receiver rows passing `3 / 7` |

## Interpretation

The current evidence diagnoses aperture/edge residual structure but does not
satisfy the contract for promoting a receiver-edge correction. A future
correction must be pre-registered, must pass the full aperture, and must be
validated on held-out receivers, held-out frequencies, or a fresh matched case.

## Decision

Do not promote receiver-edge correction, receiver exclusion, project-core
comparison, 3D validation, GPU/HPC escalation, or field FWI from the current
evidence. Use this contract to design the next adapter test.

## Validation

Focused tests:

```text
tests/test_project_core_bem_receiver_edge_modeling_contract_audit.py
3 passed
```

Figure validation:

```text
project_core_bem_receiver_edge_modeling_contract_audit.png
2285x839, dynamic range=255
```
