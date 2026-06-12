# Experiment 270: Current Archive Coverage Refresh State Audit

## Purpose

Audit the archive-coverage, commit-summary, and next-action queue refresh chain
after runs 734-736.

## 737: Current Archive Coverage Refresh State Audit

Output:

```text
outputs/experiments/737_current_archive_coverage_refresh_state_audit
```

Command:

```text
Check run 734-736 manifests, declared artifacts, docs trackers,
infrastructure symlinks, archive coverage metrics, commit-summary pointers,
queue pointers, and planning-doc pointers.
```

Artifacts:

```text
README.md
data/current_archive_coverage_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 734 archive checks: 9/9
run 735 summary checks: 5/5
run 736 queue pointer checks: 11/11
planning doc pointer checks: 3/3
git diff --check: clean after run 737
```

## Interpretation

Runs 734-736 are internally consistent. The current queue points archive
coverage to run 734 and commit preparation to run 735 while preserving run 726
local validation, run 718 code self-review, run 730 manuscript validation, run
733 state audit, and run 633 as the checksum-valid but stale handoff archive.

## Next Decision

Use run 735 for commit preparation and run 736 as the live queue. Rebuild the
archive only for explicit external handoff.
