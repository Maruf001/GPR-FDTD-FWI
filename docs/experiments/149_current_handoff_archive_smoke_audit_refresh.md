# Experiment 149: Current Handoff Archive Smoke-Audit Refresh

## Purpose

Package the refreshed current handoff archive after the run 615 size audit
showed the run 595 archive no longer covered the current smoke/audit state.

## 616: Current Handoff Archive Smoke-Audit Refresh

Output:

```text
outputs/experiments/616_current_handoff_archive_smoke_audit_refresh
```

Command:

```text
tar -czf outputs/experiments/616_current_handoff_archive_smoke_audit_refresh/current_handoff_archive_smoke_audit_refresh.tar.gz -T outputs/experiments/615_current_smoke_audit_archive_size_audit/data/current_smoke_audit_archive_file_list.txt
```

Artifacts:

```text
README.md
current_handoff_archive_smoke_audit_refresh.tar.gz
data/current_handoff_archive_smoke_audit_refresh.json
data/current_handoff_archive_smoke_audit_refresh_file_list.txt
run_manifest.json
```

Validation:

```text
input paths: 181
archive entries: 696
compressed size: 32M
SHA-256: a88eaef65502afa60555c11ed7baa3876129161e4fc5cb7f7ce7d155cc5f7b98
includes run 615 audit folder: true
includes run 616 self folder: false
includes previous run 595 archive folder: true
git diff --check: clean after run 616
```

## Interpretation

Run 616 supersedes run 595 as the current packaged handoff archive for the
post-smoke-audit state. It includes the run 615 audit folder and preserves the
previous archive folder, but excludes its own folder to avoid self-reference.

## Next Decision

Refresh commit-preparation and next-action queue pointers so optional archive
handoff points to run 616.
