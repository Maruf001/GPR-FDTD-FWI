# Experiment 1663: 84-Grid Pilot Revised Artifact Compatibility Audit

Date: 2026-06-30

## Purpose

Check whether the existing pilot-result artifacts still match the revised
five-row pilot candidate validated in run `1662`.

Run `1662` replaced the unsupported `retained_blend` row `86` with the standard
`veryhigh` row `68`. This run audits the downstream producer checklist, command
plan, and fillable template pack that were created before that replacement.

This run does not refresh those artifacts, execute FDTD, accept pilot evidence,
launch GPU work, transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1663_local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit_artifact_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit_payload_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source revised-pilot validation ready:     true
downstream artifacts audited:              3
compatible artifacts:                      0
artifacts requiring refresh:               3
artifacts missing payload 68:              3
artifacts retaining stale payload 86:      3
artifacts still carrying retained_blend:   3
minimum common payload count:              4
total missing revised payload entries:     3
total stale payload entries:               3
real executor script available:            false
accepted revised-pilot artifacts ready:    false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
audit ready:                               true
```

Artifact compatibility:

| Artifact | Common rows | Missing revised row | Stale old row | Refresh required |
| --- | ---: | --- | --- | --- |
| Producer checklist | 4 | 68 | 86 | yes |
| Command plan | 4 | 68 | 86 | yes |
| Fillable template pack | 4 | 68 | 86 | yes |

## Interpretation

The revised pilot is valid, but the downstream result artifacts are stale. They
still expect the old `retained_blend` payload `86` and do not include the new
`veryhigh` payload `68`.

This is a concrete implementation blocker. A real executor should not be wired
to the old checklist, command plan, or template pack.

## Decision

Refresh the producer checklist, command plan, and fillable templates around
payload `68` before any real executor or FDTD run. Keep execution, GPU work,
field transfer, and 3D/HPC blocked until those revised artifacts pass their own
guards.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_artifact_compatibility_audit.py
4 passed
```

Figure check:

```text
2465x847, dynamic range=255
```
