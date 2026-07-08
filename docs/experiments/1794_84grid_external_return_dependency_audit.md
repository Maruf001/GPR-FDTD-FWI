# Experiment 1794: 84-Grid External Return Dependency Audit

Date: 2026-07-01

## Purpose

Split the 84-grid external-return blocker into explicit approval and paired
artifact dependencies after the guarded preflight block from runs `1788-1793`.

This run answers a practical staging question:

```text
Which real producer files have to arrive together before observed-by-case
materialization can be rerun?
```

It is a CPU-only dependency audit. It does not create synthetic cache arrays,
stage placeholder files, run FDTD, promote observed-by-case materialization,
launch GPU work, or create field/3D evidence.

## Output

```text
outputs/experiments/1794_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_stage_dependency_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_job_dependency_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight ready:             true
source claim boundary ready:        true
source sensitivity ready:           true
stages:                             5
required return items:              21
approval items:                     1
cache-array NPZ items:              10
result-JSON items:                  10
paired artifact jobs:               10
approval-gate stages:               1
paired-artifact stages:             4
paired-artifact required items:     20
producer files present:             0
core preflight-passed items:        0
paired artifact jobs ready:         0
preflight-passed items:             0
ready stages:                       0
action groups:                      6
ready action groups:                0
observed-by-case materialized:      false
new FDTD executed:                  false
field transfer ready:               false
3D/HPC ready:                       false
gpu priority:                       none
```

The 21 required files split into one global approval token and ten paired
artifact jobs. Each artifact job requires both one cache-array NPZ file and one
result JSON file. A cache file without its result JSON, or a result JSON without
its cache file, is not enough to pass the dependency gate.

## Decision

Keep observed-by-case materialization, new FDTD execution, field transfer, and
3D/HPC blocked until the approval token and all ten cache/result pairs pass
preflight together.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_dependency_audit.py
3 passed
```

Figure check:

```text
3364x918, dynamic range=255
```
