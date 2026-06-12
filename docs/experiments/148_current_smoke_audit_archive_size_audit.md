# Experiment 148: Current Smoke-Audit Archive Size Audit

## Purpose

Audit whether the run 595 handoff archive covers the current run 614 queue,
run 613 commit-preparation, run 612 state audit, and run 609/run 611 CLI smoke
state.

## 615: Current Smoke-Audit Archive Size Audit

Output:

```text
outputs/experiments/615_current_smoke_audit_archive_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Build current handoff dependency list from the run 595 archive input list plus
docs/experiments/127-147 and outputs/experiments/595-614; compare with the run
595 archive file list and verify the run 595 archive checksum/entry count.
PY
```

Artifacts:

```text
README.md
data/current_smoke_audit_archive_size_audit.json
data/current_smoke_audit_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 180
archive input paths: 181
base files: 507
base total size: 38.1 MiB
missing paths: 0
paths not covered by run 595 archive: 41
archive recommended: true
git diff --check: clean after run 615
```

## Interpretation

The run 595 archive is stale for the current post-smoke-audit handoff. A
refreshed archive is justified and remains small enough for safe CPU-only
packaging.

## Next Decision

Create the refreshed current handoff archive from the audited file list while
excluding the archive run's own folder to avoid self-reference.
