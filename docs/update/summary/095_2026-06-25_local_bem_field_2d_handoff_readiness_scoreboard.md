# Local BEM Field 2D Handoff Readiness Scoreboard

Date: 2026-06-25

## Scope

This checkpoint records output `198`, a cross-track handoff readiness
scoreboard after the latest BEM, field, local 2D, and snapshot-policy work.

## Output

```text
outputs/summary_tables/198_local_bem_field_2d_handoff_readiness_scoreboard
```

Key artifacts:

```text
data/local_bem_field_2d_handoff_readiness_scoreboard.csv
data/local_bem_field_2d_handoff_readiness_scoreboard_summary.json
docs/LOCAL_BEM_FIELD_2D_HANDOFF_READINESS_SCOREBOARD.md
figures/local_bem_field_2d_handoff_readiness_scoreboard.png
scripts/run_local_bem_field_2d_handoff_readiness_scoreboard.py
scripts/test_local_bem_field_2d_handoff_readiness_scoreboard.py
scripts/script_snapshot_manifest.json
```

## Result

```text
tracks:                         4
handoff-ready tracks:           4
compute/claim-ready tracks:     0
compute/claim-blocked tracks:   3
snapshot policy pass:           true
latest full suite:              1298 passed in 30.62 s
```

Current track endpoints:

| Track | Handoff artifact | Compute/claim ready | Primary metric |
| --- | --- | --- | --- |
| BEM 3D | run `102` external-FDTD request bundle | false | bundle SHA-256 `3216f129b340a14502d20ecff6b9785e790afece485e88b80ffdbc58f9ffe86a` |
| Field | run `178` real-archive collection bundle | false | bundle SHA-256 `dd6ed7c7900d75077840c8ab2292c67465282a48e497b2e93c713aefed19ce2a` |
| Local 2D | run `194` source-factor decision boundary | false | update-case truth depth/radius support `2/2` |
| Snapshot policy | run `197` milestone audit | true | `70/70` milestones pass |

## Decision

Use the BEM request bundle and field collection bundle for handoff. Do not
start BEM 3D validation, field FWI/GPU/3D, or source-factor full-batch work
until the listed gates are satisfied.

## Milestone Snapshot

This milestone froze:

```text
run_local_bem_field_2d_handoff_readiness_scoreboard.py
sha256: 52d360c4027d98b71701d8f6f5744160b02541667e4f016f06ad0c753337d96f

test_local_bem_field_2d_handoff_readiness_scoreboard.py
sha256: 1419a37f49462c1e6bbe8a661ad6cbdd70a5780c84d45a32998e418ba6f6e814
```

## Validation

Focused tests:

```text
tests/test_local_bem_field_2d_handoff_readiness_scoreboard.py
2 passed
```

Full test suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1298 passed in 30.62s
```

Figure check:

```text
local_bem_field_2d_handoff_readiness_scoreboard.png
1744x774, dynamic range=255
```

Marathon status: active. The next useful branch is snapshot-policy refresh and
then another bounded report/readiness improvement.
