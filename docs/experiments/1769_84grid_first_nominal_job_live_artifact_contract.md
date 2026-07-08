# Experiment 1769: 84-Grid First Nominal Job Live Artifact Contract

Date: 2026-07-01

## Purpose

Define the exact live artifact pair for the first nominal job in the 84-grid
staged return packet.

This run does not create approval, materialize observed-by-case data, run FDTD,
launch GPU work, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1769_local_2d_state_consistent_objective_revision_84grid_first_nominal_job_live_artifact_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_first_nominal_job_live_artifact_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_first_nominal_job_live_artifact_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_first_nominal_job_live_artifact_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract artifacts:                 2
cache arrays:                       1
result JSON files:                  1
artifact jobs:                      1
live parent directories present:    0
live artifacts present:             0
live approval tokens present:       0
full external return items:         21
missing external return items:      21
materialization ready:              false
new FDTD executed:                  false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Expected first-job artifacts:

```text
outputs/experiments/_external_2d_returns/84grid_observed_by_case_pending/payload_001/ff_max_geometry_instability_nominal_observed_by_case.npz
outputs/experiments/_external_2d_returns/84grid_observed_by_case_pending/payload_001/ff_max_geometry_instability_nominal_observed_by_case.result.json
```

## Interpretation

The first artifact smoke return is now exact: one cache array and one result
JSON for the nominal `payload_001` job. The `payload_001` parent directory is
not present yet, and neither artifact is present.

## Decision

Use this as the first-job live artifact contract after the real approval token
arrives. Keep materialization, FDTD execution, GPU work, field transfer, field
FWI, and 3D/HPC blocked until approval and all external artifacts are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_first_nominal_job_live_artifact_contract.py
3 passed
```

Figure check:

```text
1852x826, dynamic range=255
```
