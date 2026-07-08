# Experiment 914: Local 2D Source-Factor State-Consistency Guard Design

Date: 2026-06-25

## Purpose

Convert the run `238` neighbor-state mechanism into explicit pre-launch guard
rows for local 2D target-coordinate optimization.

Run `238` showed that wrong fixed neighbor state can bias target x, and that
correcting both neighbor positions and neighbor radii restores truth x. This
run turns that result into a reusable gate.

This is guard design only. It does not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/240_local_2d_source_factor_state_consistency_guard_design
```

Key artifacts:

```text
data/local_2d_source_factor_state_consistency_guard_rows.csv
data/local_2d_source_factor_state_consistency_guard_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_STATE_CONSISTENCY_GUARD_DESIGN.md
figures/local_2d_source_factor_state_consistency_guard_design.png
scripts/run_local_2d_source_factor_state_consistency_guard_design.py
scripts/test_local_2d_source_factor_state_consistency_guard_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                       238
neighbor-state repair found:      true
truth-x design labels:            truth_neighbor_full_base
guard rows:                       3
guard rows supported:             3
state-consistency guard ready:    true
broad batch ready:                false
GPU work ready:                   false
field transfer ready:             false
```

Guard rows:

| Guard | Trigger | Required action |
| --- | --- | --- |
| `fixed_neighbor_state_required` | one or more non-target rebars are held fixed | mark every fixed neighbor as accepted, measured, jointly optimized, or explicitly uncertain |
| `neighbor_positions_required` | fixed neighbor x/z values differ from accepted state | refresh neighbor x/z state or include those neighbors in the optimization state |
| `neighbor_radii_required` | fixed neighbor radii differ from accepted state | refresh neighbor radii together with x/z or include radii in the optimization state |

## Interpretation

This guard prevents the exact failure mode found in run `238`: target
optimization should not treat wrong fixed neighbor state as reliable context.

The guard does not say broad batches can now run. It says what must be true
before broad local 2D batches, GPU escalation, or field transfer are justified.

## Decision

Require accepted, measured, jointly optimized, or explicitly uncertain
fixed-neighbor state before broad local 2D batches, GPU work, or field
transfer.

## Milestone Snapshot

This is a result-driven local 2D guard-design milestone. It froze:

```text
run_local_2d_source_factor_state_consistency_guard_design.py
sha256: ec4932684e33bc5efbd64a894e445381721c0f71a004860635190e40feb1020d

test_local_2d_source_factor_state_consistency_guard_design.py
sha256: d2c463098d851fa292a0c2744677cae4b5ad3e2c8b2cf691291cdcb11f9e1ed0
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_state_consistency_guard_design.py
2 passed
```

Compile check:

```text
run_local_2d_source_factor_state_consistency_guard_design.py: pass
tests/test_local_2d_source_factor_state_consistency_guard_design.py: pass
```

Figure check:

```text
1564x738, dynamic range=255
```
