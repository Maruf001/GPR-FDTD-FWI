# Experiment 1644: 84-Grid Pilot Real-Result File Staging Scaffold

Date: 2026-06-30

## Purpose

Create a concrete filesystem target for the future five-row real FDTD pilot
results defined by runs `1635-1643`.

This run creates the staging directory and records the required file list. It
does not run FDTD, does not synthesize result JSON files, and does not promote
any physical, GPU, field, or 3D/HPC claim.

## Output

```text
outputs/experiments/1644_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold
```

External staging root:

```text
outputs/experiments/_external_2d_returns/local_2d_state_consistent_objective_revision_84grid_pilot_pending
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_directory_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_file_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                        true
source validation ready:                  true
source sensitivity ready:                 true
required directories:                     1
present directories:                      1
required result files:                    5
present result files:                     0
nonempty result files:                    0
JSON parse ready files:                   0
accepted result files:                    0
unexpected files:                         0
new FDTD executions:                      0
staging actions:                          3
ready staging actions:                    0
staging scaffold ready:                   true
GPU priority:                             none
```

## Decision

The five-row pilot now has a stable return directory. The directory is empty by
design, and the five required real-result JSON files remain missing.

The next useful 2D implementation step is to write real five-row pilot outputs
into this staging area, then rerun the acceptance gate. Full 84-row execution,
GPU work, field transfer, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
