# Experiment 1789: 84-Grid External Return Preflight Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved 84-grid external-return preflight gate from run `1788`.

This validator checks that the preflight gate preserves the current pre-return
state: twenty-one external-return items are represented, no producer file is
present, no file passes its core check, no paired artifact job is complete, no
item is ready to stage, and materialization remains blocked.

This is a CPU-only validation run. It does not create approval files, cache
arrays, or result JSON files; it does not execute FDTD; and it does not promote
materialization, GPU work, field transfer, field FWI, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1789_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight gate ready:      true
validation checks:                7
passed validation checks:         7
failed validation checks:         0
preflight items:                  21
approval items:                   1
cache-array items:                10
result-JSON items:                10
artifact jobs:                    10
candidate files present:          0
preflight-passed items:           0
ready-to-stage items:             0
executed commands:                0
ready for materialization:        false
new FDTD executed:                false
gpu priority:                     none
```

The seven checks cover:

```text
1. source preflight gate readiness
2. twenty-one items and five stages
3. approval, cache-array, result-JSON, and artifact-job counts
4. absent producer files and zero core preflight passes
5. zero preflight-passed, stageable, or executed items
6. blocked materialization and downstream states
7. nonblank figure and script snapshots
```

## Interpretation

The saved preflight gate is internally consistent. It represents the full
21-file external return but does not treat placeholders, templates, missing
cache arrays, missing result JSON files, or unexecuted commands as usable 2D
simulation evidence.

## Decision

Use run `1789` as the validator for the run `1788` preflight gate. Keep
materialization and FDTD execution blocked until real files pass the preflight
and live-intake checks.

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
run_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
