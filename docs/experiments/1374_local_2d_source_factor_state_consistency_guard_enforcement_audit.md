# Experiment 1374: Local 2D Source-Factor State-Consistency Guard Enforcement Audit

Date: 2026-06-27

## Purpose

Rebuild the neighbor-state guard from the actual local 2D experiment outputs
`1371`-`1373` and write the guard result inside the 2D experiment stream.

Run `913` showed that wrong fixed-neighbor state can bias target x. Run `914`
designed a guard, but the next clean step is to enforce that guard directly from
the numbered 2D experiment outputs.

This run does not launch new optimizer commands, GPU work, field transfer,
field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/experiments/1374_local_2d_source_factor_state_consistency_guard_enforcement_audit
```

Key artifacts:

```text
data/local_2d_source_factor_state_consistency_execution_rows.csv
data/local_2d_source_factor_state_consistency_guard_rows.csv
data/local_2d_source_factor_state_consistency_launch_scenarios.csv
data/local_2d_source_factor_state_consistency_guard_enforcement_summary.json
figures/local_2d_source_factor_state_consistency_guard_enforcement_audit.png
docs/LOCAL_2D_SOURCE_FACTOR_STATE_CONSISTENCY_GUARD_ENFORCEMENT_AUDIT.md
scripts/run_local_2d_source_factor_state_consistency_guard_enforcement_audit.py
scripts/test_local_2d_source_factor_state_consistency_guard_enforcement_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source experiment outputs checked: 3
truth-x design count:              1
guard rows:                        3
guard rows supported:              3
state-consistency guard enforced:  true
bounded local continuation ready:  true
broad batch ready:                 false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
```

Source-output results:

| Design | Best x mm | Best z mm | Best radius mm | Best misfit | Truth x | Truth xyz |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `truth_neighbor_positions_base` | 189.0 | 90.0 | 5.0 | 0.16869103277938238 | false | false |
| `truth_neighbor_radii_base` | 188.0 | 90.0 | 5.0 | 0.42822235203536657 | false | false |
| `truth_neighbor_full_base` | 190.0 | 90.0 | 5.0 | 0.09154466861337839 | true | true |

Launch scenarios:

| Scenario | Status | Allowed next | Reason |
| --- | --- | --- | --- |
| `wrong_fixed_neighbor_state` | fail | none | baseline wrong-neighbor branch selected the lower-x state |
| `positions_only_corrected` | partial | diagnostic only | positions move the solution toward truth but do not fully repair it |
| `radii_only_corrected` | fail | none | radii alone do not repair the lower-x branch |
| `positions_and_radii_corrected` | pass | bounded local continuation only | full fixed-neighbor state correction restores the truth-x branch |

## Interpretation

The actual `1371`-`1373` outputs reproduce the mechanism: positions-only
correction is partial, radii-only correction fails, and correcting both neighbor
positions and radii restores the truth target state.

The guard is therefore enforceable from the experiment stream itself. This is a
local 2D mechanism result, not a field-transfer or GPU-launch result.

## Decision

Allow only bounded local continuation from the fully corrected neighbor-state
case.

Keep broad local 2D batches, GPU work, and field transfer blocked unless fixed
neighbor states are accepted, measured, jointly optimized, or explicitly
uncertain.

## Milestone Snapshot

This is a result-driven local 2D guard-enforcement milestone. It froze:

```text
run_local_2d_source_factor_state_consistency_guard_enforcement_audit.py
sha256: 79a590036942156df0df4f4be30c3f34742109a2d33c605954aba2e4768fd1dd

test_local_2d_source_factor_state_consistency_guard_enforcement_audit.py
sha256: 0eab96eece8e4a6c829f0afcfdc9af06cbc578c6b15c3b9dd81ea839762617cc
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_state_consistency_guard_enforcement_audit.py
2 passed
```

Figure check:

```text
local_2d_source_factor_state_consistency_guard_enforcement_audit.png
2104x846, dynamic range=255
```
