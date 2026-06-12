# Experiment 155: Current Manuscript Archive Size Audit

## Purpose

Audit whether the run 616 handoff archive covers the current run 619 manuscript
validation, run 620 commit-preparation, and run 621 action-queue state,
including content drift in already-covered files.

## 622: Current Manuscript Archive Size Audit

Output:

```text
outputs/experiments/622_current_manuscript_archive_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Build current handoff dependency list from the run 616 archive input list plus
docs/experiments/148-154 and outputs/experiments/616-621; compare path
coverage and file SHA-256 hashes against the run 616 archive.
PY
```

Artifacts:

```text
README.md
data/current_manuscript_archive_size_audit.json
data/current_manuscript_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 194
archive input paths: 195
base files: 540
base total size: 69.9 MiB
missing paths: 0
paths not covered by run 616 archive: 13
files missing from run 616 archive: 37
files changed since run 616 archive: 4
archive recommended: true
git diff --check: clean after run 622
```

## Interpretation

The run 616 archive is stale for the current manuscript-refresh handoff. A
refreshed archive is justified because the manuscript draft changed after run
616 and runs 619-621 plus their trackers are not packaged.

## Next Decision

Create the refreshed current handoff archive from the audited file list while
excluding the archive run's own folder to avoid self-reference.
