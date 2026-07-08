# Local 2D Source-Factor State-Consistency Guard Design

Date: 2026-06-25

## Scope

This checkpoint records run `240`, a read-only guard synthesis from the run
`238` neighbor-state mechanism.

This was guard design only. It did not execute FDTD, optimizer commands, GPU
work, field transfer, field FWI, 3D/HPC, or neural-network training.

## Output

```text
outputs/summary_tables/240_local_2d_source_factor_state_consistency_guard_design
```

Tracked note:

```text
docs/experiments/914_local_2d_source_factor_state_consistency_guard_design.md
```

## Result

```text
neighbor-state repair found:      true
guard rows:                       3
guard rows supported:             3
state-consistency guard ready:    true
broad batch ready:                false
GPU work ready:                   false
field transfer ready:             false
```

## Decision

Before broad local 2D batches, GPU escalation, or field transfer, every fixed
non-target neighbor state must be accepted, measured, jointly optimized, or
explicitly uncertain.

This converts the run `238` mechanism into a reusable pre-launch guard.

## Snapshot Discipline

The milestone froze:

```text
run_local_2d_source_factor_state_consistency_guard_design.py
sha256: ec4932684e33bc5efbd64a894e445381721c0f71a004860635190e40feb1020d

test_local_2d_source_factor_state_consistency_guard_design.py
sha256: d2c463098d851fa292a0c2744677cae4b5ad3e2c8b2cf691291cdcb11f9e1ed0
```

Future related local 2D work should start from a duplicated run-specific
script.

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_local_2d_source_factor_state_consistency_guard_design.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_local_2d_source_factor_state_consistency_guard_design.py tests/test_local_2d_source_factor_state_consistency_guard_design.py
pass
```

Figure check:

```text
1564x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This is a checkpoint, not a
stop condition. Continue with snapshot refresh, then integrate this guard into
the current local 2D evidence/scoreboard stream.
