# Experiment 127: Current Handoff Archive Refresh Size Audit

## Purpose

Audit whether the run 580 handoff archive covers the current run 591 manuscript
validation, run 592 commit-preparation, and run 593 action-queue state.

## 594: Current Handoff Archive Refresh Size Audit

Output:

```text
outputs/experiments/594_current_handoff_archive_refresh_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Build current handoff dependency list from run 591 manuscript lint, docs,
runtime scripts/tests, run 592 commit summary, run 593 action queue, and the
run 580 archive state; compare with the run 580 archive file list.
PY
```

Artifacts:

```text
README.md
data/current_handoff_archive_refresh_size_audit.json
data/current_handoff_archive_refresh_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 138
archive input paths: 139
base files: 402
base total size: 21.6 MiB
missing paths: 0
paths not covered by run 580 archive: 27
archive recommended: true
```

## Interpretation

The run 580 archive is stale for the current post-manuscript-validation
handoff. A refreshed archive is justified and remains small enough for safe
CPU-only packaging.

## Next Decision

Create the refreshed current handoff archive from the audited file list while
excluding the archive run's own folder to avoid self-reference.
