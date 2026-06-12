# Experiment 128: Current Handoff Archive Refresh

## Purpose

Package the current manuscript, validation, commit-preparation, queue, and
handoff dependency set after the run 594 size and coverage audit.

## 595: Current Handoff Archive Refresh

Output:

```text
outputs/experiments/595_current_handoff_archive_refresh
```

Command:

```text
tar -czf outputs/experiments/595_current_handoff_archive_refresh/current_handoff_archive_refresh.tar.gz \
  -T outputs/experiments/595_current_handoff_archive_refresh/data/current_handoff_archive_refresh_file_list.txt
sha256sum outputs/experiments/595_current_handoff_archive_refresh/current_handoff_archive_refresh.tar.gz
tar -tzf outputs/experiments/595_current_handoff_archive_refresh/current_handoff_archive_refresh.tar.gz | wc -l
```

Artifacts:

```text
current_handoff_archive_refresh.tar.gz
data/current_handoff_archive_refresh.json
data/current_handoff_archive_refresh_file_list.txt
run_manifest.json
```

Validation:

```text
input paths: 139
archive entries: 554
compressed size: 16M
sha256: a55cbf6c6540223bdb01874ca51bb2ab1063057833006e06a318f66ce84be280
sha256 check: OK
includes run 594 audit folder: yes
includes run 595 self folder: no
```

## Interpretation

The refreshed archive supersedes run 580 for optional current external handoff.
It includes the previous run 580 archive folder and adds current
post-archive/post-manuscript-validation artifacts through run 594 while
avoiding self-reference.

## Next Decision

Refresh the action queue so optional current archive handoff points to run 595.
