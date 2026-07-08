# Result Milestone Snapshot Audit: Numbered CPU Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `176`, a refreshed result-milestone snapshot
audit after local 2D source-factor runs `172` through `175`.

## Output

```text
outputs/summary_tables/176_result_milestone_snapshot_audit_numbered_cpu_refresh
```

## Result

```text
milestones audited:       47
passed milestones:        47
failed milestones:        0
snapshot files audited:   90
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

Newly covered milestones include:

```text
171_result_milestone_snapshot_audit_full_factorial_refresh
172_local_2d_source_factor_counterfactual_availability_audit
173_local_2d_source_factor_cpu_wrapper_command_design
174_local_2d_source_factor_cpu_wrapper_parse_smoke
175_local_2d_source_factor_numbered_cpu_command_design
```

## Decision

The milestone-freezing policy remains satisfied after the local 2D numbered CPU
command design. Continue freezing scripts/tests at major result-driven
milestones and starting related future experiments from duplicated
run-specific scripts.

## Milestone Snapshot

This audit froze:

```text
run_result_milestone_snapshot_audit_numbered_cpu_refresh.py
sha256: 57b3e0895a999f381a6df0b589b2754271670d1775808d9b3e33715c4d0e83f3

test_result_milestone_snapshot_audit_numbered_cpu_refresh.py
sha256: 663c999ae604f572ff8fa68ea551290259841a70d40fba881fe032a26ff4061c
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_numbered_cpu_refresh.py
2 passed
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. The next branch should decide whether to run one
numbered CPU smoke command or add one more execution preflight.
