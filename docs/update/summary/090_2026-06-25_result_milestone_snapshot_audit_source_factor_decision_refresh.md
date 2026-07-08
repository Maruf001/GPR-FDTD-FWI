# Result Milestone Snapshot Audit: Source-Factor Decision Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `195`, a refreshed result-milestone snapshot
audit after the source-factor decision-boundary audit.

## Output

```text
outputs/summary_tables/195_result_milestone_snapshot_audit_source_factor_decision_refresh
```

Key artifacts:

```text
data/result_milestone_snapshot_audit.csv
data/result_milestone_snapshot_audit_summary.json
docs/RESULT_MILESTONE_SNAPSHOT_AUDIT.md
figures/result_milestone_snapshot_audit.png
scripts/run_result_milestone_snapshot_audit_source_factor_decision_refresh.py
scripts/test_result_milestone_snapshot_audit_source_factor_decision_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
milestones audited:       66
passed milestones:        66
failed milestones:        0
snapshot files audited:   128
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

The refresh includes:

```text
193_result_milestone_snapshot_audit_source_factor_xzradius_geometry_refresh
194_local_2d_source_factor_xzradius_decision_boundary_audit
```

## Decision

The result-driven milestone freeze rule remains satisfied. Continue to
duplicate the prior run-specific script before starting each related follow-up
experiment.

## Milestone Snapshot

This milestone froze:

```text
run_result_milestone_snapshot_audit_source_factor_decision_refresh.py
sha256: 31638426c961c0b17b789356f2633aef5e6cd2fff89cb4680fc736ccff753d7e

test_result_milestone_snapshot_audit_source_factor_decision_refresh.py
sha256: 14c496b6bdd93aef81cd2a1ca9b2c41d0552ab5547cc7c286350b8a78daebf1f
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_source_factor_decision_refresh.py
2 passed
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. The next branch is BEM-side improvement work because
the source-factor x/z/radius branch is now decision-bounded.
