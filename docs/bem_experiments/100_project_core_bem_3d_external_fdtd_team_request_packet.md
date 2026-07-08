# BEM Experiment 100: External FDTD Team Request Packet

Date: 2026-06-25

## Purpose

Turn the run `099` external-FDTD decision into a concrete team-facing request
packet.

This run packages the exact paired full-Maxwell 3D FDTD request for discussion
or handoff. It does not launch local 3D FDTD, GPU/HPC work, field FWI, or
neural-network training.

## Output

```text
outputs/bem_experiments/100_project_core_bem_3d_external_fdtd_team_request_packet
```

Key artifacts:

```text
data/project_core_bem_3d_external_fdtd_team_request_runs.csv
data/project_core_bem_3d_external_fdtd_team_request_artifacts.csv
data/project_core_bem_3d_external_fdtd_team_request_acceptance_gates.csv
data/project_core_bem_3d_external_fdtd_team_request_message.txt
data/project_core_bem_3d_external_fdtd_team_request_packet_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_TEAM_REQUEST_PACKET.md
figures/project_core_bem_3d_external_fdtd_team_request_packet.png
scripts/run_project_core_bem_3d_external_fdtd_team_request_packet.py
scripts/test_project_core_bem_3d_external_fdtd_team_request_packet.py
scripts/script_snapshot_manifest.json
```

## Result

```text
requested paired FDTD runs:        2
request artifacts:                 7
acceptance gates:                  7
receiver count:                    31
frequency count:                   4
frequency rows per run:            124
total frequency rows expected:     248
all request artifacts exist:       true
ready for team handoff:            true
real external FDTD data present:   false
3D validation ready:               false
local 3D FDTD launch ready:        false
GPU/HPC ready:                     false
```

## Request Summary

The request is for two paired full-Maxwell 3D FDTD runs:

```text
1. target-present run: finite PEC cylinder target
2. background run: same domain/source/receivers/frequencies, no target
```

Return either receiver time traces matching the run `080` schema or filled
target/background frequency-bin templates matching run `077`.

## Interpretation

The BEM 3D validation request is now packaged for a teammate: two paired runs,
seven artifacts, seven acceptance gates, and a message that preserves the
no-validation-before-real-return boundary.

This is still not 3D validation. Real BEM/FDTD comparison, 3D validation, local
3D launch, and GPU/HPC remain blocked until returned target/background files
pass metadata, frequency-bin, and comparator gates.

## Decision

Use this packet for the Wednesday/team discussion or external FDTD handoff.
Keep BEM/FDTD comparison, 3D validation, local 3D launch, and GPU/HPC blocked
until returned real target/background files pass the gates.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_team_request_packet.py
sha256: a47a4401579fd2d9de683e33a4f22ae71cc95d59d34bdcdd1d27bc5f3d9a7f31

test_project_core_bem_3d_external_fdtd_team_request_packet.py
sha256: ea118fa94dc96bf185bc1d9a741fcdc5c1ae92156996d69a9b00bbe9d6d23147
```

Subsequent BEM 3D request or return-intake experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_team_request_packet.py
3 passed
```

Figure check:

```text
project_core_bem_3d_external_fdtd_team_request_packet.png
2285x738, dynamic range=255
```
