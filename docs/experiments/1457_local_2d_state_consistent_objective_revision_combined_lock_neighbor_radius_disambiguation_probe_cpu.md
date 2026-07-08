# Experiment 1457: Combined Lock Neighbor-Radius Disambiguation Probe

Date: 2026-06-28

## Purpose

Test whether the combined wrong-x lock is driven by incorrect near/far
neighbor radii.

This bounded CPU probe uses the dense scan from run `1456`, the hard combined
near/far perturbation, four neighbor-radius model assumptions, and target
x-candidates at 187, 188, 189, and 190 mm. It does not launch GPU work,
transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1457_local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_result_rows.csv
data/local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_COMBINED_LOCK_NEIGHBOR_RADIUS_DISAMBIGUATION_PROBE.md
scripts/run_local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_probe_cpu.py
scripts/test_local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_probe_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
neighbor models:                     4
objective selection rows:           24
candidate rows:                     96
scan positions:                      8
target x candidates:                 4
all-objectives-truth models:         2
veryhigh-only failure models:        0
all-objective failure models:        2
both neighbors corrected all truth:  true
near corrected only all truth:       true
far corrected only all truth:        false
neighbor probe ready:                true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
elapsed seconds:                     144.023
```

Outcome by neighbor model:

| Neighbor model | Outcome |
| --- | --- |
| combined perturbed neighbors | all six objectives select wrong x=187 mm |
| near corrected, far perturbed | all six objectives select truth x=190 mm |
| near perturbed, far corrected | all six objectives select wrong x=187 mm |
| both neighbors corrected | all six objectives select truth x=190 mm |

## Interpretation

The combined wrong-x lock is tied mainly to near-neighbor radius error.
Correcting the near neighbor restores all-objective truth selection even if the
far neighbor remains perturbed; correcting only the far neighbor does not.

## Decision

Use run `1457` as a local diagnostic showing that the next repair must estimate
or validate the near-neighbor radius, not just alter target selection policy.
Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused setup test:

```text
tests/test_local_2d_state_consistent_objective_revision_combined_lock_neighbor_radius_disambiguation_probe_cpu.py
3 passed
```

Figure validation:

```text
2463x1490, dynamic range=255
```
