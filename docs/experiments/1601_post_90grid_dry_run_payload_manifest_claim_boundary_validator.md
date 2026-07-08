# Experiment 1601: Post 90-Grid Dry-Run Payload Manifest Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1600` claim boundary from artifacts.

## Output

```text
outputs/experiments/1601_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      30
guarded claims:                              27
blocked claims:                              3
payload rows:                                90
objective profiles:                          5
transition bins:                             18
budget:                                      60 min
estimated total runtime:                     58.69245 min
executable commands:                         0
run-specific execution script available:     false
commands executed:                           false
new FDTD executed:                           false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator confirms that the 90-grid manifest claim is present, cites runs
`1597-1599`, records the expected manifest metrics, and keeps downstream
readiness blocked.

## Decision

Use this validator as the artifact guard for run `1600`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validator.py
6 passed
```

Figure check:

```text
2645x832, dynamic range=255
```
