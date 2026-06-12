# Experiment 221: Current Manuscript/Archive State Audit

## Purpose

Audit the archive coverage and manuscript validation refresh chain after runs
682-687.

## 688: Current Manuscript/Archive State Audit

Output:

```text
outputs/experiments/688_current_manuscript_archive_state_audit
```

Command:

```text
Audit runs 682-687 for manifest, declared artifact, docs tracker, symlink,
validation, and queue-pointer consistency.
```

Artifacts:

```text
README.md
data/current_manuscript_archive_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 682 archive coverage status: pass
run 682 missing base paths: 0
run 685 lint status: pass
run 685 balance status: pass
run 687 queue pointer checks: 10/10
run 686 summary pointer checks: 3/3
planning doc pointer checks: 3/3
git diff --check: clean after run 688
```

## Interpretation

Runs 682-687 are internally consistent. The current queue correctly points
manuscript validation to run 685, archive coverage to run 682, and commit
preparation to run 686.

## Next Decision

Refresh commit-preparation and next-action queue pointers so the current state
audit points to run 688.

