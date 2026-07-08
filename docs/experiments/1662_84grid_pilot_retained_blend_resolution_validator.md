# Experiment 1662: 84-Grid Pilot Retained-Blend Resolution Validator

Date: 2026-06-30

## Purpose

Validate the revised five-row pilot candidate from run `1661`.

Run `1661` recommended replacing the undefined `retained_blend` pilot row with
payload row `68`, the standard `veryhigh` objective at the same transition bin.
This run checks that the revised pilot candidate is internally consistent and
still does not permit FDTD execution.

This run does not execute FDTD, accept pilot evidence, launch GPU work, transfer
to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1662_local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source resolution audit ready:             true
validation checks:                         6
passed checks:                             6
failed checks:                             0
candidate revised pilot rows:              5
candidate revised unique objectives:       4
candidate revised retained_blend rows:     0
candidate revised veryhigh rows:           2
recommended replacement payload row:       68
recommended replacement transition bin:    13
real executor script available:            false
accepted revised pilot ready:              false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
validation ready:                          true
```

The validated revised pilot is:

| Order | Payload row | Objective profile | Transition bin | Notes |
| ---: | ---: | --- | ---: | --- |
| 1 | 1 | highband | 0 | unchanged |
| 2 | 23 | late | 4 | unchanged |
| 3 | 46 | late_high | 9 | unchanged |
| 4 | 68 | veryhigh | 13 | replaces `retained_blend` row 86 |
| 5 | 72 | veryhigh | 17 | unchanged |

## Interpretation

The revised pilot is valid as a candidate execution target. It removes the
unsupported `retained_blend` label, keeps the same five transition-bin
locations, and uses only existing parser-supported objective definitions.

It is still not executable evidence. The separate real pilot executor does not
exist yet, and no FDTD run was performed.

## Decision

Use runs `1661-1662` as the guarded revised-pilot candidate block. The next 2D
task should define the real-executor contract around this revised pilot while
keeping FDTD execution, GPU work, field transfer, and 3D/HPC blocked until that
contract passes.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_retained_blend_resolution_validator.py
6 passed
```

Figure check:

```text
2285x847, dynamic range=255
```
