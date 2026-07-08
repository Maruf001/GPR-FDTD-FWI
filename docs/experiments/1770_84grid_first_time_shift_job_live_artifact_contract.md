# Experiment 1770: 84-Grid First Time-Shift Job Live Artifact Contract

Date: 2026-07-01

## Purpose

Define the exact external artifact contract for the first time-shift
observed-by-case job in the 84-grid materialization path.

This run extends the first nominal-job contract from run `1769`. It does not
materialize observed-by-case data, execute FDTD, launch GPU work, transfer to
field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1770_local_2d_state_consistent_objective_revision_84grid_first_time_shift_job_live_artifact_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_first_time_shift_job_live_artifact_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_first_time_shift_job_live_artifact_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_first_time_shift_job_live_artifact_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract artifacts:                   2
cache arrays required:                1
result JSON files required:           1
artifact jobs required:               1
live parent directories present:      0
live artifacts present:               0
live approval token present:          0
first nominal contract artifacts:     2
cumulative first-payload artifacts:   4
full external return items required:  21
missing external return items:        21
materialization ready:                false
new FDTD executed:                    false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

Expected live artifacts:

```text
payload_001/ff_max_geometry_instability_time_shift_only_observed_by_case.npz
payload_001/ff_max_geometry_instability_time_shift_only_observed_by_case.result.json
```

## Interpretation

The paired first-payload time-shift return is now exact: one cache array and
one result JSON under `payload_001`. Together with the first nominal contract
from run `1769`, the first-payload smoke return requires four external
artifacts after the approval token.

The `payload_001` parent directory and both time-shift artifacts are absent.

## Decision

Use this as the paired first-job live artifact contract. Keep
materialization, FDTD execution, GPU work, field transfer, field FWI, and
3D/HPC blocked until the approval token and external artifacts are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_first_time_shift_job_live_artifact_contract.py
3 passed
```

Figure check:

```text
1852x826, dynamic range=255
```
