# Experiment 1791: 84-Grid External Return Preflight Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the 84-grid external-return preflight block from
runs `1788-1790`.

The external-return requirements and preflight gate are guarded. Observed-by-case
materialization, new FDTD execution, physical claims, field transfer, and 3D/HPC
remain blocked because no real approval, cache-array, or result-JSON file has
passed preflight.

## Output

```text
outputs/experiments/1791_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary
```

## Result

```text
source preflight gate ready:      true
source validation ready:          true
source sensitivity ready:         true
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight items:                  21
approval items:                   1
cache-array items:                10
result-JSON items:                10
artifact jobs:                    10
candidate files present:          0
preflight-passed items:           0
ready-to-stage items:             0
observed-by-case materialized:    false
new FDTD executed:                false
3D/HPC ready:                     false
gpu priority:                     none
```

## Decision

Use run `1791` to prevent the external-return checklist from being cited as
completed materialization, new FDTD execution, field transfer, or 3D/HPC
readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_claim_boundary.py
3 passed
```

Figure check:

```text
3509x904, dynamic range=255
```
