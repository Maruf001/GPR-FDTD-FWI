# Result Milestone Snapshot Audit: X-Envelope Execution Refresh

Date: 2026-06-25

## Scope

Refresh the result-driven milestone snapshot audit after run `220`, the local
2D x-envelope CPU execution audit.

## Output

```text
outputs/summary_tables/221_result_milestone_snapshot_audit_x_envelope_execution_refresh
```

## Result

```text
milestones audited:       98
passed milestones:        98
failed milestones:        0
snapshot files audited:   192
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

The refresh added:

```text
219_result_milestone_snapshot_audit_x_envelope_command_refresh
220_local_2d_source_factor_x_envelope_cpu_execution_audit
```

Both pass the frozen-script manifest check.

## Snapshot Discipline

The audit milestone also froze itself:

```text
run_result_milestone_snapshot_audit_x_envelope_execution_refresh.py
sha256: 2f3b60d0ca9fdebab5734838a73ad7402cff49be3054bcbec38eaa9513d75903

test_result_milestone_snapshot_audit_x_envelope_execution_refresh.py
sha256: 09f4ac98184dcf29e683ce52879095ca7b68c3e25f9e17bab63644b9088346b6
```

## Validation

Focused tests:

```text
conda run -n gpr-fdtd-fwi python -m pytest tests/test_result_milestone_snapshot_audit_x_envelope_execution_refresh.py -q
2 passed
```

Compile check:

```text
python -m py_compile run_result_milestone_snapshot_audit_x_envelope_execution_refresh.py tests/test_result_milestone_snapshot_audit_x_envelope_execution_refresh.py
pass
```

Figure check:

```text
1492x738, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This audit is a checkpoint,
not a stop condition. Continue with the geometry-instability discriminant
analysis from a duplicated run-specific script.
