# Experiment 1375: Local 2D State-Consistent Objective-Window Ladder

Date: 2026-06-27

## Purpose

Test whether the fully corrected neighbor-state result from run `1374` is
stable across the local objective-window ladder.

Run `1374` showed that the target can be recovered only when the fixed
neighbor state uses both the correct positions and the correct radii. This run
keeps that corrected state and asks whether the recovered target is an artifact
of one objective window or a stable local result.

This is a bounded CPU-only local 2D experiment. It does not launch broad
batches, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/experiments/1375_local_2d_source_factor_state_consistent_objective_window_ladder_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_window_ladder_results.csv
data/local_2d_state_consistent_objective_window_ladder_summary.json
data/coordinate_objective_diagnostics.csv
data/multi_rebar_coordinate_optimizer_summary.json
figures/local_2d_state_consistent_objective_window_ladder_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_WINDOW_LADDER.md
scripts/run_local_2d_state_consistent_objective_window_ladder.py
scripts/test_local_2d_state_consistent_objective_window_ladder.py
scripts/script_snapshot_manifest.json
```

## Result

```text
optimizer executed:                  true
optimizer exit code:                 0
optimizer elapsed seconds:           355.744
objective windows tested:            6
diagnostic rows:                     12
update-case truth-geometry count:    6
nominal-case truth-geometry count:   0
update case all objectives truth:    true
nominal case all objectives truth:   false
bounded local continuation ready:    true
broad batch ready:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
```

Objective-window outcomes:

| Case | Objective | Best x mm | Best z mm | Best radius mm | Best misfit | Truth geometry |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| nominal | base | 189.0 | 90.0 | 5.0 | 0.32219408728906557 | false |
| nominal | highband | 189.0 | 90.0 | 5.0 | 0.21695591542159443 | false |
| nominal | late | 188.0 | 90.0 | 5.0 | 0.27763895011390993 | false |
| nominal | late_high | 188.0 | 90.0 | 5.0 | 0.2340858710275732 | false |
| nominal | veryhigh | 189.0 | 90.0 | 5.0 | 0.33882088123300436 | false |
| nominal | early_high | 189.0 | 90.0 | 5.0 | 0.21448537388378797 | false |
| corrected update | base | 190.0 | 90.0 | 5.0 | 0.09154466861337839 | true |
| corrected update | highband | 190.0 | 90.0 | 5.0 | 0.0009528743310125738 | true |
| corrected update | late | 190.0 | 90.0 | 5.0 | 0.09108659224499975 | true |
| corrected update | late_high | 190.0 | 90.0 | 5.0 | 0.0013902034575908999 | true |
| corrected update | veryhigh | 190.0 | 90.0 | 5.0 | 0.001383355816635612 | true |
| corrected update | early_high | 190.0 | 90.0 | 5.0 | 0.00018572190606984027 | true |

The corrected update case recovered the target geometry for every objective
window:

```text
x = 190 mm
z = 90 mm
radius = 5 mm
```

The nominal case recovered none of the truth-geometry rows across the same
objective windows.

## Interpretation

The run strengthens the state-consistency finding. The corrected neighbor-state
branch is not just a one-objective success: base, high-band, late, late-high,
very-high, and early-high objectives all select the truth geometry.

The nominal branch still fails under all six windows. That means objective
window tuning is not the main repair mechanism. The repair mechanism is the
corrected local state used around the target.

## Decision

Keep this as a bounded local 2D continuation result.

The next allowed synthetic 2D work should stay local to the same
state-consistent branch unless a new physical question is defined. Broad local
2D batches, GPU work, and field transfer remain blocked by the same guard.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_objective_window_ladder.py
sha256: ca1f6469e47d20c95c24d4dc69ea4f35c0f6303778a5be62438f94495af9d6ca

test_local_2d_state_consistent_objective_window_ladder.py
sha256: ff3c878b396239af39eef194651d06282f3a7340940dd9c0c50ce9f7c62330f6
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_window_ladder.py
2 passed
```

Figure check:

```text
local_2d_state_consistent_objective_window_ladder_audit.png
1924x846, dynamic range=255
```
