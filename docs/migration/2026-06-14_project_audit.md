# Project Audit - 2026-06-14

Read-only audit baseline before migration-prep edits:

```text
Repository: /home/lam001/Documents/GPR-FDTD-FWI
Remote: https://github.com/Maruf001/GPR-FDTD-FWI.git
Local master: 1291a21f51623bddb45acd9f18cdfe081fb92a53
origin/master: 1291a21f51623bddb45acd9f18cdfe081fb92a53
Working tree: clean before migration-prep branch edits
Tracked files: 1432
Ignored files: 14769
Project size: about 2.7 GB
```

## Git Coverage

Git tracks source code, tests, documentation, field-data files, selected
presentations, field-QC outputs, and summary tables.

Git intentionally does not track the numbered synthetic output archive:

```text
outputs/experiments/
```

This is the main migration risk. Those files are real local research artifacts,
but a normal clone does not include them.

## Local Artifact Archive

Prepared archive directory:

```text
/home/lam001/Documents/GPR-FDTD-FWI_migration_2026-06-14
```

Prepared local artifact archive:

```text
GPR-FDTD-FWI_local_artifacts_2026-06-14.tar.zst
```

Archive contents:

```text
Archived ignored output files: 14538
Uncompressed archived bytes: 2026710978
Compressed archive size: about 1.6 GB
SHA256: 72cd8bafa419275421642d75f85d172f8f343cf2d92f9170f13a8dcadd9d790c
```

The archive keeps generated research outputs and excludes local caches/tool
state. The tracked file
`docs/migration/local_artifact_archive_inventory_2026-06-14.tsv` records the
archive decision for every ignored file.

## Experiment Output Coverage

Local output tree:

```text
outputs/experiments direct directories: 1219
numbered experiment directories: 1218
run_manifest.json files: 1214
```

Tracked experiment docs:

```text
docs/experiments numbered tracker files: 757
tracker range: 1-757
local output folders without individual tracked tracker docs: 758-1218
```

The late experiment range is still summarized in tracked reporting artifacts,
especially:

```text
docs/update/summary/005_2026-06-11_summary_update.md
docs/update/summary/004_2026-06-11_experiment_700_1218_holistic_evaluation.ipynb
outputs/summary_tables/experiment_700_1218_holistic_evaluation/
```

## Environment Observed

Current machine:

```text
Python base: 3.12.12
FNO environment Python: 3.13.12
NVIDIA driver: 580.95.05
CUDA shown by nvidia-smi: 13.0
nvcc: 13.0.88
Codex CLI: 0.139.0
Claude Code: 2.1.177
```

Notable package state:

```text
FNO has cupy-cuda12x 14.0.1, readgssi 0.0.22, pytest 9.0.3
FNO did not import numba during audit
```

Current source imports require the dependency files added in this migration
prep branch:

```text
requirements.txt
requirements-dev.txt
requirements-gpu.txt
environment.yml
```

## Cleanup Decisions

Temporary office lock files were removed from the Git index and are now ignored:

```text
outputs/.~lock.GPR_FDTD_FWI_SingleRebar_Next.pptx#
outputs/~$GPR_FDTD_FWI_SingleRebar_Next_v2.pptx
```

They remain local files on this machine until manually cleaned up, but they
should not migrate as versioned project artifacts.
