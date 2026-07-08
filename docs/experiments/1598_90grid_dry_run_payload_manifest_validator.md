# Experiment 1598: 90-Grid Dry-Run Payload Manifest Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1597` manifest from artifacts.

The validator checks that the 90-row dry-run manifest has the expected shape,
stays within the one-hour budget envelope, remains non-executable, keeps all
downstream states blocked, and includes nonblank figure and script snapshots.

## Output

```text
outputs/experiments/1598_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validator_checks.csv
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validator_summary.json
figures/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
dry-run manifest validation ready:           true
payload rows:                                90
objective profiles:                          5
transition bins:                             18
budget:                                      60 min
estimated total runtime:                     58.69245 min
executable commands:                         0
run-specific execution script available:     false
commands executed:                           false
new FDTD executed:                           false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator confirms that the saved manifest is a review-ready planning
artifact, not an execution artifact.

## Decision

Use this validator as the artifact guard for run `1597`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validator.py
4 passed
```

Figure check:

```text
2825x873, dynamic range=255
```
