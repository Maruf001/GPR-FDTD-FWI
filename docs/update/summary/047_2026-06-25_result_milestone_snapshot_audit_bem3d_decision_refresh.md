# Result Milestone Snapshot Audit: BEM 3D Decision Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `153`, a refreshed audit of result-driven
milestone script snapshots after BEM run `099`.

The purpose is to enforce the project rule that major result-driven milestones
freeze the exact scripts and focused tests that produced them, and that related
future experiments start from duplicated run-specific scripts.

## Output

```text
outputs/summary_tables/153_result_milestone_snapshot_audit_bem3d_decision_refresh
```

Key artifacts:

```text
data/result_milestone_snapshot_audit.csv
data/result_milestone_snapshot_audit_summary.json
docs/RESULT_MILESTONE_SNAPSHOT_AUDIT.md
figures/result_milestone_snapshot_audit.png
scripts/run_result_milestone_snapshot_audit_bem3d_decision_refresh.py
scripts/test_result_milestone_snapshot_audit_bem3d_decision_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
milestones audited:       21
passed milestones:        21
failed milestones:        0
snapshot files audited:   38
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

Run `099` is included in the audited milestone set and passes with two frozen
snapshots.

## Decision

Keep the milestone-freezing rule active before starting subsequent related
runs. For related branches, duplicate the prior milestone script first, then
edit the duplicate. Do not edit frozen copies under output-local `scripts/`
folders.

## Milestone Snapshot

This audit is itself a result-driven process milestone. Its exact script and
focused test were frozen under the output-local `scripts/` folder:

```text
run_result_milestone_snapshot_audit_bem3d_decision_refresh.py
sha256: fb7e54c930933b50712533b5672a4f7c10685f6c4a96f7b8e7e443c9be6f767f

test_result_milestone_snapshot_audit_bem3d_decision_refresh.py
sha256: 877d86306157e52a143e31479487918190872b7ed8090dfc43e52f10d57e4e2d
```

## Validation

Focused tests:

```text
tests/test_result_milestone_snapshot_audit_bem3d_decision_refresh.py
2 passed
```

Figure check:

```text
result_milestone_snapshot_audit.png
1492x738, dynamic range=255
```

Marathon status: active. The next defensible branch is to refresh the
team-facing evidence brief or presentation pack with run `099`, then continue
to another bounded BEM, field, or local 2D task.
