# Result Milestone Snapshot Audit: Source-Factor X/Z/Radius Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `189`, the refreshed result-milestone snapshot
audit after the x/z/radius local source-factor execution in run `188`.

## Output

```text
outputs/summary_tables/189_result_milestone_snapshot_audit_source_factor_xzradius_refresh
```

## Result

```text
milestones audited:       60
passed milestones:        60
failed milestones:        0
snapshot files audited:   116
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

The audit includes the new source-factor outputs `186`, `187`, and `188`.

## Decision

The milestone-freezing rule remains satisfied. Continue duplicating
run-specific scripts before related follow-up runs.

## Milestone Snapshot

This milestone froze:

```text
run_result_milestone_snapshot_audit_source_factor_xzradius_refresh.py
sha256: 6d2d14643961b0202b71fd5b759cc2dd61287e2189fe11df98fc2873c3b0ff2b

test_result_milestone_snapshot_audit_source_factor_xzradius_refresh.py
sha256: 20d299e33f4af1e033f7d76d9d8c714962a59385bf839f1e8a2a3d61fb0412b7
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_source_factor_xzradius_refresh.py
2 passed
```

Python compile check:

```text
run_result_milestone_snapshot_audit_source_factor_xzradius_refresh.py: pass
tests/test_result_milestone_snapshot_audit_source_factor_xzradius_refresh.py: pass
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. Continue with bounded replication or another
single-target local neighborhood.
