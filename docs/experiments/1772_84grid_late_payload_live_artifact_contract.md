# Experiment 1772: 84-Grid Late Payload Live Artifact Contract

Date: 2026-07-01

## Purpose

Define the exact external artifact contract for the late payload jobs in the
84-grid materialization path.

This run extends the middle-payload contract from run `1771`. It does not
materialize observed-by-case data, execute FDTD, launch GPU work, transfer to
field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1772_local_2d_state_consistent_objective_revision_84grid_late_payload_live_artifact_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_late_payload_live_artifact_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_late_payload_live_artifact_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_late_payload_live_artifact_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract artifacts:                    8
cache arrays required:                 4
result JSON files required:            4
artifact jobs required:                4
payloads required:                     2
live parent directories present:       0
live artifacts present:                0
live approval token present:           0
cumulative artifacts through middle:   12
cumulative artifacts through all jobs: 20
full external return items required:   21
missing external return items:         21
materialization ready:                 false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

Expected live payloads:

```text
payload_068
payload_072
```

Each payload requires nominal and time-shift cache arrays plus matching result
JSON files.

## Interpretation

The late-payload return is now exact: eight artifacts across payloads `068` and
`072`. Combined with the first-payload and middle-payload contracts, all twenty
artifact files in the staged return packet are now specified. The remaining
external item is the approval token.

The `payload_068` and `payload_072` parent directories and all eight artifacts
are absent.

## Decision

Use this as the late-payload live artifact contract. Keep materialization, FDTD
execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until the
approval token and external artifacts are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_late_payload_live_artifact_contract.py
3 passed
```

Figure check:

```text
1852x826, dynamic range=255
```
