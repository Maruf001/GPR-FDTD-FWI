# Result Milestone Snapshot Audit: Full-Factorial Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `171`, a refreshed result-milestone snapshot
audit after local 2D source-factor runs `169` and `170`.

## Output

```text
outputs/summary_tables/171_result_milestone_snapshot_audit_full_factorial_refresh
```

## Result

```text
milestones audited:       42
passed milestones:        42
failed milestones:        0
snapshot files audited:   80
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

Newly covered milestones include:

```text
168_result_milestone_snapshot_audit_source_factor_refresh
169_local_2d_source_factor_observed_coverage_audit
170_local_2d_source_factor_full_factorial_design_contract
```

## Decision

The milestone-freezing policy remains satisfied after the local 2D
full-factorial source-factor design refresh. Continue freezing scripts/tests at
major result-driven milestones and starting related future experiments from
duplicated run-specific scripts.

## Milestone Snapshot

This audit froze:

```text
run_result_milestone_snapshot_audit_full_factorial_refresh.py
sha256: cc9a2ba550c9b02c1ba23b76654a32d640fe2f956b7edf5fb75e3e70faf9318b

test_result_milestone_snapshot_audit_full_factorial_refresh.py
sha256: 1a6af8c2c5c6a17641331676f0ce600406faac34566eba34cb4440c5c915cb6b
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_full_factorial_refresh.py
2 passed
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. The next branch should test whether the nine required
counterfactual source-factor diagnostics can be generated from existing cached
optimizer artifacts or need a new bounded CPU diagnostic executor.
