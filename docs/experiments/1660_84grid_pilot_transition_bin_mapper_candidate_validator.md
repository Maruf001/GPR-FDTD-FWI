# Experiment 1660: 84-Grid Pilot Transition-Bin Mapper Candidate Validator

Date: 2026-06-30

## Purpose

Validate the candidate transition-bin mapper from run `1659`.

Run `1659` proposed a concrete mapping from the 18-bin pilot axis to a 40-45 mm
Tx/Rx-offset axis. This run checks whether that design is internally
consistent and whether it correctly remains a design artifact rather than an
accepted execution contract.

This run does not execute FDTD, accept pilot evidence, define `retained_blend`,
launch GPU work, transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1660_local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source candidate mapper design ready:      true
checks passed:                             5 of 5
transition bins validated:                 18
pilot rows validated:                      5
directly sampled pilot offsets:            2
interpolated pilot offsets:                3
pilot rows at/above crossing:              1
zero-margin crossing offset:               44.62073709151374 mm
accepted execution mapper ready:           false
retained_blend definition available:       false
real executor script available:            false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
```

The five checks cover:

| Check | Result |
| --- | --- |
| Source mapper design ready | pass |
| 18-bin 40-45 mm axis shape | pass |
| Five-row pilot mapping shape | pass |
| Interpolation and crossing counts | pass |
| Figure/script artifacts and blocked states | pass |

## Interpretation

The candidate mapper is internally consistent. It maps the 18 transition bins
monotonically from 40 to 45 mm, preserves the five selected pilot rows, records
two directly sampled offsets and three interpolated offsets, and keeps only the
45 mm endpoint at or above the saved crossing.

The result does not make the pilot executable. The `retained_blend` row remains
undefined as a concrete objective, and a separate real executor is still
missing.

## Decision

Keep the five-row real FDTD pilot, full 84-row expansion, GPU work, field
transfer, and 3D/HPC blocked. The next 2D work should resolve the
`retained_blend` policy into either a concrete objective definition or a
deliberate removal from the executable pilot.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_validator.py
5 passed
```

Figure check:

```text
2285x847, dynamic range=255
```
