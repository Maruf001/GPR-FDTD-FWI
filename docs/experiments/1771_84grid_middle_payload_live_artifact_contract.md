# Experiment 1771: 84-Grid Middle Payload Live Artifact Contract

Date: 2026-07-01

## Purpose

Define the exact external artifact contract for the middle payload jobs in the
84-grid materialization path.

This run extends the first-payload time-shift contract from run `1770`. It
does not materialize observed-by-case data, execute FDTD, launch GPU work,
transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1771_local_2d_state_consistent_objective_revision_84grid_middle_payload_live_artifact_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_middle_payload_live_artifact_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_middle_payload_live_artifact_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_middle_payload_live_artifact_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
contract artifacts:                         8
cache arrays required:                      4
result JSON files required:                 4
artifact jobs required:                     4
payloads required:                          2
live parent directories present:            0
live artifacts present:                     0
live approval token present:                0
cumulative first-payload artifacts:         4
cumulative artifacts through middle stage:  12
full external return items required:        21
missing external return items:              21
materialization ready:                      false
new FDTD executed:                          false
GPU work ready:                             false
field transfer ready:                       false
field FWI ready:                            false
3D/HPC ready:                               false
```

Expected live payloads:

```text
payload_023
payload_046
```

Each payload requires nominal and time-shift cache arrays plus matching result
JSON files.

## Interpretation

The middle-payload return is now exact: eight artifacts across payloads `023`
and `046`. Combined with the first-payload contracts from runs `1769` and
`1770`, the staged return now specifies twelve artifact files after the
approval token.

The `payload_023` and `payload_046` parent directories and all eight artifacts
are absent.

## Decision

Use this as the middle-payload live artifact contract. Keep materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until
the approval token and external artifacts are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_middle_payload_live_artifact_contract.py
3 passed
```

Figure check:

```text
1852x826, dynamic range=255
```
