# Experiment 266: Current Manuscript Validation Refresh State Audit

## Purpose

Audit the manuscript-validation, commit-summary, and next-action queue refresh
chain after runs 730-732.

## 733: Current Manuscript Validation Refresh State Audit

Output:

```text
outputs/experiments/733_current_manuscript_validation_refresh_state_audit
```

Command:

```text
Check run 730-732 manifests, declared artifacts, docs trackers, infrastructure
symlinks, manuscript validation metrics, commit-summary pointers, queue
pointers, and planning-doc pointers.
```

Artifacts:

```text
README.md
data/current_manuscript_validation_refresh_state_audit.json
run_manifest.json
```

Validation:

```text
status: pass
manifest parse failures: 0
missing declared artifacts: 0
missing docs: 0
missing symlinks: 0
run 730 manuscript checks: 7/7
run 731 summary checks: 5/5
run 732 queue pointer checks: 11/11
planning doc pointer checks: 3/3
git diff --check: clean after run 733
```

## Interpretation

Runs 730-732 are internally consistent. The current queue points manuscript
validation to run 730 and commit preparation to run 731 while preserving run
726 local validation, run 718 code self-review, run 729 state audit, run 722
archive coverage, and run 633 as the checksum-valid but stale handoff archive.

## Next Decision

Use run 731 for commit preparation and run 732 as the live queue. Rebuild the
archive only for explicit external handoff.
