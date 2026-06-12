# Experiment 231: Current Coordinate Default Smoke State Audit

## Purpose

Audit the coordinate confidence metadata/default hardening chain after runs
694-697.

## 698: Current Coordinate Default Smoke State Audit

Output:

```text
outputs/experiments/698_current_coordinate_default_smoke_state_audit
```

Command:

```text
Audit runs 694-697 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_coordinate_default_smoke_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 694 status: pass
run 694 full pytest: 268 passed in 24.43 s
run 695 status: pass
run 695 invalid defaults rejected: 3/3
run 695 invalid output dirs created: 0
run 695 valid-control non-finite numerics: 0
run 695 valid-control plots nonblank: 2/2
run 697 queue pointer checks: 13/13
run 696 summary pointer checks: 4/4
planning doc pointer checks: 3/3
git diff --check: clean after run 698
```

## Interpretation

Runs 694-697 are internally consistent. The aggregate default Tx/Rx offset
hardening has focused-test coverage, full-suite validation, and a real CLI
smoke showing `nan`, `inf`, and negative defaults fail before output
allocation while a finite default still produces strict aggregate artifacts.

## Next Decision

Refresh commit-preparation and next-action queue pointers so the current state
audit points to run 698.

