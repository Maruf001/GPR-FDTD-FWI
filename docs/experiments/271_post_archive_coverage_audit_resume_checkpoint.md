# Experiment 271: Post-Archive-Coverage Audit Resume Checkpoint

## Purpose

Record a compact crash-recovery checkpoint after the manuscript validation and
archive coverage refresh chain.

## 738: Post-Archive-Coverage Audit Resume Checkpoint

Output:

```text
outputs/experiments/738_post_archive_coverage_audit_resume_checkpoint
```

Command:

```text
Record current pointers to validation, review, manuscript validation, archive
coverage, state audit, commit preparation, next-action queue, and handoff
archive.
```

Artifacts:

```text
README.md
data/post_archive_coverage_audit_resume_checkpoint.json
run_manifest.json
```

Validation:

```text
checkpoint status: ready
pointer count: 8
full pytest pointer: run 726
code self-review pointer: run 718
manuscript validation pointer: run 730
archive coverage pointer: run 734
state audit pointer: run 737
commit preparation pointer: run 735
queue pointer: run 736
handoff archive pointer: run 633
git diff --check: clean after run 738
```

## Interpretation

Run 738 supersedes run 648 as the current crash-recovery checkpoint while
preserving run 633 as the checksum-valid but stale external archive.

## Next Decision

Use run 735 for commit preparation and run 736 as the live queue. Rebuild the
archive only for explicit external handoff.
