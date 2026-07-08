# Result Milestone Snapshot Audit: Source-Factor X/Radius Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `186`, the refreshed result-milestone snapshot
audit after the source-factor CPU smoke sequence through run `185`.

## Output

```text
outputs/summary_tables/186_result_milestone_snapshot_audit_source_factor_xradius_refresh
```

## Result

```text
milestones audited:       57
passed milestones:        57
failed milestones:        0
snapshot files audited:   110
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

The audit includes new source-factor outputs `176` through `185`, including the
run `185` x/radius mini-neighborhood execution audit.

## Decision

The result-driven milestone-freezing rule is currently satisfied. Related
follow-up experiments should continue to start from duplicated run-specific
scripts, then modify the duplicate.

## Milestone Snapshot

This milestone froze:

```text
run_result_milestone_snapshot_audit_source_factor_xradius_refresh.py
sha256: 7b88104a5be2dd35551c3fb5d3390fe6919b2cda6cd9ca750f5510c2c57146a5

test_result_milestone_snapshot_audit_source_factor_xradius_refresh.py
sha256: 9d61434895cf8bb1e15cc1296be278fa0333b76bab26f50f77196e2e48e2ee57
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_source_factor_xradius_refresh.py
2 passed
```

Python compile check:

```text
run_result_milestone_snapshot_audit_source_factor_xradius_refresh.py: pass
tests/test_result_milestone_snapshot_audit_source_factor_xradius_refresh.py: pass
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. Continue with bounded source-factor follow-up work; do
not stop at this checkpoint.
