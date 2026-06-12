# Experiment 166: Current Handoff Archive Resume Refresh

## Purpose

Package the refreshed current handoff archive after the run 632 archive-size
audit found that run 623 does not cover the current resume/audit handoff state.

## 633: Current Handoff Archive Resume Refresh

Output:

```text
outputs/experiments/633_current_handoff_archive_resume_refresh
```

Command:

```text
tar -czf outputs/experiments/633_current_handoff_archive_resume_refresh/current_handoff_archive_resume_refresh.tar.gz \
  -T outputs/experiments/632_current_resume_archive_size_audit/data/current_resume_archive_file_list.txt
```

Artifacts:

```text
README.md
current_handoff_archive_resume_refresh.tar.gz
data/current_handoff_archive_resume_refresh.json
data/current_handoff_archive_resume_refresh_file_list.txt
run_manifest.json
```

Validation:

```text
input paths: 215
archive entries: 805
compressed size: 128M
sha256: 00637efb4a579591b0f529f693a7e722b94361b0a3ea129cde5695ba35e49aef
git diff --check: clean after run 633
```

## Interpretation

Run 633 is the current external handoff archive. It includes the run 632 audit
folder, the updated resume/audit/queue checkpoints through run 631, and the
previous run 623 archive folder. It excludes the run 633 self folder to avoid
self-reference.

## Next Decision

Refresh commit-preparation and next-action queue pointers so archive handoff
points to run 633.
