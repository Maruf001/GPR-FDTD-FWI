# Experiment 1436: Local 2D Objective Revision Prospective Sweep

Date: 2026-06-28

## Purpose

Execute a small prospective CPU sweep for the drop-`veryhigh` and majority-vote
objective-revision candidates.

This run is CPU-only. It does not launch GPU work, transfer to field data, run
field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1436_local_2d_state_consistent_objective_revision_prospective_sweep_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_expanded_window_radius_bracket_results.csv
data/local_2d_state_consistent_expanded_window_radius_bracket_candidates.csv
data/local_2d_state_consistent_objective_revision_prospective_objective_rows.csv
data/local_2d_state_consistent_objective_revision_prospective_policy_rows.csv
data/local_2d_state_consistent_objective_revision_prospective_design_rows.csv
data/local_2d_state_consistent_objective_revision_prospective_sweep_summary.json
figures/local_2d_state_consistent_objective_revision_prospective_sweep.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_PROSPECTIVE_SWEEP.md
scripts/run_local_2d_state_consistent_objective_revision_prospective_sweep_cpu.py
scripts/test_local_2d_state_consistent_objective_revision_prospective_sweep_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
prospective perturbations:           5
objective selection rows:            30
objectives per case:                 6
veryhigh failure count:              3
non-veryhigh failure count:          0
policies recovering all cases:       drop_veryhigh_all_remaining;majority_vote_all_objectives
drop-veryhigh supported:             true
majority-vote supported:             true
prospective sweep executed:          true
objective revision local validation: true
promote revised objective now:       false
broad radius tolerance promoted:     false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
elapsed seconds:                     252.46
```

The failures were:

```text
far_neighbor_radius_minus_1p10mm, veryhigh, selected x=187.0
far_neighbor_radius_minus_1p40mm, veryhigh, selected x=187.0
near_neighbor_radius_plus_2p00mm, veryhigh, selected x=187.0
```

All non-`veryhigh` objectives selected truth across all five prospective
perturbations. Drop-`veryhigh` and majority-vote policies recovered truth across
the full prospective sweep.

## Decision

Use run `1436` as the prospective local 2D validation checkpoint for the revised
objective policy.

Keep broad-radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked. A separate claim-boundary refresh is still needed before changing the
canonical local 2D decision state.

## Validation

Focused test before execution:

```text
tests/test_local_2d_state_consistent_objective_revision_prospective_sweep_cpu.py
4 passed
```

Figure validation:

```text
3222x884, dynamic range=255
```
