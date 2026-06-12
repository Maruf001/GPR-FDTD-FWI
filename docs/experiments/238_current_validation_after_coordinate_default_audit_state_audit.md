# Experiment 238: Current Validation After Coordinate Default Audit State Audit

## Purpose

Audit the validation/commit/queue refresh chain after runs 702-704.

## 705: Current Validation After Coordinate Default Audit State Audit

Output:

```text
outputs/experiments/705_current_validation_after_coordinate_default_audit_state_audit
```

Command:

```text
Audit runs 702-704 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_validation_after_coordinate_default_audit_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 702 status: pass
run 702 full pytest: 268 passed in 24.60 s
run 703 inventory status: inventory_ready
run 704 queue pointer checks: 14/14
run 703 summary pointer checks: 4/4
planning doc pointer checks: 3/3
git diff --check: clean after run 705
```

## Interpretation

Runs 702-704 are internally consistent. The current queue points local
validation to run 702, state audit to run 701, and commit preparation to run
703.

## Next Decision

Use run 703 for code/docs review or commit preparation. Rebuild the external
archive only if handoff packaging is requested.

