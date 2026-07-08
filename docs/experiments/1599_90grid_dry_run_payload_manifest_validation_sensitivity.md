# Experiment 1599: 90-Grid Dry-Run Payload Manifest Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1598` validator against controlled damage to the 90-grid
dry-run payload manifest.

## Output

```text
outputs/experiments/1599_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       23
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  22
observed failure scenarios:                  22
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 1597:            true
validator rejects damaged variants:          true
commands executed:                           false
new FDTD executed:                           false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator accepts the exact run `1597` manifest and rejects controlled
damage to row counts, objective-profile counts, transition-bin counts, budget
envelope, hidden execution, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `1597-1599` as the guarded 90-grid dry-run payload-manifest block. A
future execution run still needs a run-specific script and review before any
new FDTD computation is launched.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_validation_sensitivity.py
3 passed
```

Figure check:

```text
3401x904, dynamic range=255
```
