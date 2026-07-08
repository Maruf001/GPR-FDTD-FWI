# BEM 3D External FDTD Team Request Packet Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records BEM run `100`, a team-facing request packet for the
external full-Maxwell 3D FDTD target/background data needed by the BEM 3D
validation branch.

No local 3D FDTD, GPU/HPC work, field FWI, or neural-network training was
launched.

## Output

```text
outputs/bem_experiments/100_project_core_bem_3d_external_fdtd_team_request_packet
```

Tracked note:

```text
docs/bem_experiments/100_project_core_bem_3d_external_fdtd_team_request_packet.md
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

## Interpretation

The BEM 3D external-FDTD handoff is now concrete. The packet includes the two
paired runs, seven artifacts, seven gates, and a request message suitable for a
team discussion.

This is a data request, not a validation result. Real BEM/FDTD comparison and
3D validation remain blocked until real target/background returns pass metadata,
frequency-bin, and comparator gates.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_team_request_packet.py
sha256: a47a4401579fd2d9de683e33a4f22ae71cc95d59d34bdcdd1d27bc5f3d9a7f31

test_project_core_bem_3d_external_fdtd_team_request_packet.py
sha256: ea118fa94dc96bf185bc1d9a741fcdc5c1ae92156996d69a9b00bbe9d6d23147
```

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

Marathon status: active. The next defensible branch is to add run `100` to the
snapshot audit and then continue with another bounded technical improvement.
