# Local Field BEM 3D Marathon Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the current local marathon state after the BEM 3D
decision refresh, field real-archive worksheet, matched local 2D source gate,
presentation refreshes, and snapshot-policy audits.

## Key Results

```text
BEM 3D run 099: external FDTD request path ready, validation still blocked
field run 177: 20-row real-archive operator worksheet ready for collection day
local 2D run 159: prior 126 mm source span refined to 5 mm matched delta
local 2D run 160: 3 matched-robust cases, 2 blocked variable-radius cases
presentation run 162: 48 claims, 40 ready scoped, 8 blocked
snapshot audit 164: 33 milestones, 62 frozen snapshots, all pass
```

## Current Decisions

```text
BEM 3D validation: blocked until real paired target/background FDTD returns exist
field FWI/GPU/3D: blocked until real archive acceptance passes
local 2D broad source robustness: blocked
time-zero-only explanation: blocked
new GPU/FWI launch: not justified by current evidence
milestone snapshot policy: pass
```

## Validation

Targeted regression:

```text
18 passed
```

Full suite:

```text
1197 passed in 30.36s
```

Resource state at validation:

```text
RAM: 18 GiB used / 119 GiB total
GPU: NVIDIA GB10 at about 5% utilization
```

Marathon status: active. The next defensible branch is a BEM-side external 3D
FDTD team request packet that turns run `099` into a concrete handoff artifact.
