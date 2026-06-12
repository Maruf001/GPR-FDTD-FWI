# Experiment 165: Current Resume Archive Size Audit

## Purpose

Audit whether the run 623 handoff archive covers the current resume, audit,
commit-preparation, and action-queue state.

## 632: Current Resume Archive Size Audit

Output:

```text
outputs/experiments/632_current_resume_archive_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Build current handoff dependency list from the run 623 archive input list plus
docs/experiments/155-164 and outputs/experiments/623-631; compare path
coverage and file SHA-256 hashes against the run 623 archive.
PY
```

Artifacts:

```text
README.md
data/current_resume_archive_size_audit.json
data/current_resume_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 214
archive input paths: 215
base files: 586
base total size: 133.6 MiB
missing paths: 0
paths not covered by run 623 archive: 19
files missing from run 623 archive: 49
files changed since run 623 archive: 3
archive recommended: true
git diff --check: clean after run 632
```

## Interpretation

The run 623 archive is stale for the current resume/audit handoff. A refreshed
archive is justified because the active restart/queue/audit pointers changed
after run 623 and runs 624-631 plus their trackers are not packaged.

## Next Decision

Create the refreshed current handoff archive from the audited file list while
excluding the archive run's own folder to avoid self-reference.
