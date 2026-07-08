# Experiment 1661: 84-Grid Pilot Retained-Blend Resolution Audit

Date: 2026-06-30

## Purpose

Resolve the undefined `retained_blend` row in the five-row 2D pilot without
inventing an unsupported objective.

Runs `1658-1660` showed that the transition-bin mapper is now internally
consistent, but the pilot still contains one policy-only objective label. This
run compares executable ways to handle that label before any real FDTD pilot
execution.

This run does not execute FDTD, accept pilot evidence, launch GPU work, transfer
to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1661_local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit_option_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit_candidate_revised_pilot_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source mapper validation ready:             true
source pilot rows:                          5
source retained_blend rows:                 1
resolution options evaluated:               5
execution-candidate options:                2
standard same-bin replacements available:   4
recommended option:                         substitute_veryhigh_at_same_bin
recommended replacement payload row:        68
recommended replacement objective:          veryhigh
recommended replacement transition bin:     13
recommended objective parses:               true
recommended preserves five-row pilot:       true
recommended preserves transition bin:       true
recommended removes policy-only label:      true
recommended requires new definition:        false
same-objective crossing pair created:       true
candidate revised pilot rows:               5
candidate revised unique objectives:        4
candidate revised retained_blend rows:      0
accepted revised pilot ready:               false
new FDTD executed:                          false
GPU work ready:                             false
field transfer ready:                       false
3D/HPC ready:                               false
```

The recommended candidate replaces payload row `86`, `retained_blend` at bin
`13`, with payload row `68`, `veryhigh` at the same bin. This keeps the five-row
pilot and preserves the 0.75 transition sample while avoiding a new objective
definition.

Candidate revised pilot:

| Order | Payload row | Objective profile | Transition bin | Notes |
| ---: | ---: | --- | ---: | --- |
| 1 | 1 | highband | 0 | unchanged |
| 2 | 23 | late | 4 | unchanged |
| 3 | 46 | late_high | 9 | unchanged |
| 4 | 68 | veryhigh | 13 | replaces `retained_blend` row 86 |
| 5 | 72 | veryhigh | 17 | unchanged |

## Interpretation

The safest executable treatment is to remove `retained_blend` from the pilot.
Creating a new midpoint window or aliasing the label to `veryhigh` would be
parseable, but it would also introduce an unsupported scientific definition or
a misleading label.

The `veryhigh` bin-13 substitution is conservative. It uses an existing
objective definition, preserves the transition-bin location, and creates a
below/above crossing pair with the existing `veryhigh` endpoint at bin 17.

## Decision

Use payload row `68` as the candidate replacement for the undefined
`retained_blend` pilot row. Keep real pilot execution, full 84-row expansion,
GPU work, field transfer, and 3D/HPC blocked until the revised pilot is
separately validated and a real executor exists.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_audit.py
5 passed
```

Figure check:

```text
3328x888, dynamic range=255
```
