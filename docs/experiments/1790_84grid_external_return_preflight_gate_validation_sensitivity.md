# Experiment 1790: 84-Grid External Return Preflight Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1789` preflight-gate validator by damaging the saved run
`1788` state in controlled ways.

This run checks whether the validator accepts only the exact saved pre-return
state and rejects premature promotion of file presence, JSON validity, NPZ
loadability, core file checks, paired-job completion, staging, materialization,
FDTD execution, downstream states, figures, and script snapshots.

This is a CPU-only validation-sensitivity run. It does not create approval
files, cache arrays, or result JSON files; it does not execute FDTD; and it does
not promote materialization, GPU work, field transfer, field FWI, or 3D/HPC
readiness.

## Output

```text
outputs/experiments/1790_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:           true
scenarios:                        26
expected pass scenarios:          1
expected fail scenarios:          25
observed pass scenarios:          1
observed fail scenarios:          25
unexpected outcomes:              0
damaged scenarios:                25
damaged scenarios rejected:       25
gpu priority:                     none
```

The exact saved state passes. The damaged states all fail as expected:

```text
source readiness damage
item-count damage
stage-count damage
approval-count damage
cache-count damage
result-count damage
job-count damage
candidate-file false promotion
nonzero-file false promotion
approval-JSON false promotion
approval-core false promotion
NPZ-loadable false promotion
cache-core false promotion
result-JSON false promotion
result-core false promotion
paired-job false promotion
preflight-passed false promotion
ready-to-stage false promotion
executed-command false promotion
materialization-input false promotion
materialization false promotion
FDTD false promotion
downstream false promotion
figure damage
script-snapshot damage
```

## Interpretation

The validator is sensitive to every state change that would make the external
return appear more complete than it is. The only accepted state is the saved run
`1788` state: twenty-one required external-return items are listed, but zero
real files pass preflight and zero items are stageable.

## Decision

Use runs `1788-1790` as the guarded 84-grid external-return preflight block.
The next 2D step still requires the real approval token, ten real cache arrays,
ten real result JSON files, and then guarded live intake before materialization
or FDTD-derived claims.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity.py

9 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validation_sensitivity.py: pass
```

Figure check:

```text
3796x873, dynamic range=255
```
