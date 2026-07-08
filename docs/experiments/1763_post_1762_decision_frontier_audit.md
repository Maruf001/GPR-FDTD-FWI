# Experiment 1763: Post-1762 Decision Frontier Audit

Date: 2026-07-01

## Purpose

Consolidate the current 2D objective-revision branch into a decision frontier.

This run reads saved 2D artifacts from runs `1446` through `1762` and separates
what is now supported from what remains blocked. It does not run new FDTD,
GPU work, field transfer, field FWI, or 3D/HPC work.

## Output

```text
outputs/experiments/1763_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_decision_rows.csv
data/local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_frontier_rows.csv
data/local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit_summary.json
figures/local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit.png
```

## Result

```text
source summaries read:                 16
decision blocks:                       8
frontier items:                        4
blocked frontier items:                3
local objective cases recovered:       5 / 5
five-axis generalization ready:        true
45 mm suppression bracket span:        0.023437 mm
follow-up any-failure models:          20
84-row subset estimate:                54.77962 min
pilot row count:                       5
observed_by_case jobs:                 10
expected FDTD trace solves:            80
blank approval fields:                 4
external approval token present:       false
new FDTD executed:                     false
gpu work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

## Interpretation

The current 2D evidence supports a guarded local mechanism result: the revised
objective route works on its validated local cases, the wrong-x failure is tied
to near/far radius-error interactions, and the mechanism is sensitive to
geometry and acquisition layout.

The 45 mm acquisition result remains a narrow sampled edge, not a broad
acquisition rule. The bounded 84-row screen and five-row pilot are well
specified, but observed-data materialization still requires a real approval
token and return packet.

## Decision

Use this run as the current 2D decision frontier. Do not promote broad physical
transfer, new FDTD execution, GPU work, field FWI, or 3D/HPC from this branch
until the external approval token and observed-data return packet are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_1762_decision_frontier_audit.py
4 passed
```

