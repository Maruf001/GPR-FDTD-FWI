# Migration Guide

This guide records the migration state prepared on 2026-06-14 for moving the
project from the current DGX Spark to another DGX Spark.

## What Git Does And Does Not Contain

The Git repository contains source code, documentation, tests, field-data files,
selected reports, summary tables, presentation artifacts, and field-QC outputs.

The large numbered synthetic experiment output tree is intentionally ignored:

```text
outputs/experiments/
```

That means a normal Git clone will not include those local experiment folders.
They are not missing from the current machine; they are local artifacts that must
be restored from the migration artifact archive if the new machine needs an
exact working-copy replica.

## Transfer Directory

The migration archive directory on this machine is:

```bash
/home/lam001/Documents/GPR-FDTD-FWI_migration_2026-06-14
```

It contains:

```text
GPR-FDTD-FWI_local_artifacts_2026-06-14.tar.zst
GPR-FDTD-FWI_git_all_2026-06-14.bundle
local_artifacts_filelist_2026-06-14.txt
SHA256SUMS.txt
```

The local-artifacts archive contains generated research outputs that are ignored
by Git but needed for a faithful local replica. It excludes bytecode caches,
pytest cache, Matplotlib cache, editor lock files, and local Claude settings.

Archive inventory files tracked in this repository:

```text
docs/migration/experiment_output_inventory_2026-06-14.tsv
docs/migration/ignored_file_inventory_2026-06-14.tsv
docs/migration/local_artifact_archive_inventory_2026-06-14.tsv
```

## Restore On The New DGX Spark

Preferred path if GitHub access is working:

```bash
git clone https://github.com/Maruf001/GPR-FDTD-FWI.git
cd GPR-FDTD-FWI
git checkout master
tar --zstd -xf /path/to/GPR-FDTD-FWI_local_artifacts_2026-06-14.tar.zst
```

Offline path using the Git bundle:

```bash
git clone /path/to/GPR-FDTD-FWI_git_all_2026-06-14.bundle GPR-FDTD-FWI
cd GPR-FDTD-FWI
git switch master
git remote add origin https://github.com/Maruf001/GPR-FDTD-FWI.git
tar --zstd -xf /path/to/GPR-FDTD-FWI_local_artifacts_2026-06-14.tar.zst
```

Verify the transfer archive before extracting:

```bash
cd /path/to/GPR-FDTD-FWI_migration_2026-06-14
sha256sum -c SHA256SUMS.txt
```

Verify the restored experiment archive after extracting:

```bash
cd /path/to/GPR-FDTD-FWI
find outputs/experiments -maxdepth 1 -mindepth 1 -type d | wc -l
find outputs/experiments -maxdepth 2 -type f -name run_manifest.json | wc -l
```

Expected counts from this migration audit:

```text
outputs/experiments direct directories: 1219
numbered experiment directories: 1218
run_manifest.json files: 1214
artifact archive entries: 14538
```

## Git Workflow After Restore

On the new machine:

```bash
git status --short --branch --untracked-files=all
git remote -v
git branch -vv
```

If continuing from this migration branch:

```bash
git switch migration-prep-2026-06-14
```

If continuing from GitHub master after this branch is pushed and merged:

```bash
git switch master
git pull --ff-only origin master
```

Do not commit `outputs/experiments/` directly unless a small curated subset is
being promoted as a report artifact. Keep full experiment outputs in external
archives or object storage.

## Current Research State

The latest tracked project summary is:

```text
docs/update/summary/005_2026-06-11_summary_update.md
```

The strongest current synthetic workflow is the multi-rebar variable-depth and
variable-radius coordinate optimizer. The tracked holistic report for
experiments 700-1218 is:

```text
docs/update/summary/004_2026-06-11_experiment_700_1218_holistic_evaluation.ipynb
outputs/summary_tables/experiment_700_1218_holistic_evaluation/
```

Tracked experiment notes currently cover experiments 1-757. The local artifact
archive preserves output folders through 1218.

## What Was Deliberately Not Migrated In The Artifact Archive

The archive excludes files that can be regenerated or are machine-local:

```text
__pycache__/
.pytest_cache/
.claude/
outputs/.cache/
outputs/.matplotlib/
*.pyc
*.pid
.~lock.*#
~$*
```

The full ignored-file inventory still records these exclusions so they are
accounted for.
