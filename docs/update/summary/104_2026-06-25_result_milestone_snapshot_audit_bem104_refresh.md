# Result Milestone Snapshot Audit: BEM 104 Refresh

Date: 2026-06-25

## Scope

This checkpoint records snapshot-audit run `205`, refreshed after BEM run `104`
made the external-FDTD return inbox executable as a preflight gate.

The audit checks that recent result-driven BEM, field, local 2D, and summary
milestones froze their run scripts and tests under each output folder's
`scripts/` directory, and that the frozen SHA-256 values still match.

## Output

```text
outputs/summary_tables/205_result_milestone_snapshot_audit_bem104_refresh
```

## Result

```text
milestones audited:       80
passed milestones:        80
failed milestones:        0
snapshot files audited:   156
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

The refresh adds these audited milestones:

```text
104_project_core_bem_3d_external_fdtd_return_inbox_preflight
204_result_milestone_snapshot_audit_bem103_refresh
```

## Decision

The milestone-freezing policy remains active. After each result-driven
milestone, freeze the exact script/test into that output folder. Start the next
related experiment from a duplicated run-specific script, then edit the
duplicate.

## Milestone Snapshot

This snapshot audit froze:

```text
run_result_milestone_snapshot_audit_bem104_refresh.py
sha256: 73d1cd52c86fcdb3d8ec3dd65db1999a264af94b05f35ba0f985b13454de15af

test_result_milestone_snapshot_audit_bem104_refresh.py
sha256: 08fed07e5f1a287774e2d2aa6769eb6667613f3f5d146eb2ec04428aff20ef1d
```

## Validation

Focused test:

```text
tests/test_result_milestone_snapshot_audit_bem104_refresh.py
2 passed
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```
