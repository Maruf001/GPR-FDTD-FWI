# Experiment 156: Current Handoff Archive Manuscript Refresh

## Purpose

Package the refreshed current handoff archive after the run 622 audit showed
the run 616 archive no longer covered the current manuscript-validation state.

## 623: Current Handoff Archive Manuscript Refresh

Output:

```text
outputs/experiments/623_current_handoff_archive_manuscript_refresh
```

Command:

```text
tar -czf outputs/experiments/623_current_handoff_archive_manuscript_refresh/current_handoff_archive_manuscript_refresh.tar.gz -T outputs/experiments/622_current_manuscript_archive_size_audit/data/current_manuscript_archive_file_list.txt
```

Artifacts:

```text
README.md
current_handoff_archive_manuscript_refresh.tar.gz
data/current_handoff_archive_manuscript_refresh.json
data/current_handoff_archive_manuscript_refresh_file_list.txt
run_manifest.json
```

Validation:

```text
input paths: 195
archive entries: 742
compressed size: 64M
SHA-256: d60e899a45b3528d773b9125a0654686f0554bb8bdf6f2e6b02b7d3c24cbcc18
includes run 622 audit folder: true
includes run 623 self folder: false
includes previous run 616 archive folder: true
includes updated run 562 manuscript folder: true
git diff --check: clean after run 623
```

## Interpretation

Run 623 supersedes run 616 as the current packaged handoff archive for the
post-manuscript-validation state. It includes the run 622 audit folder,
preserves the previous archive folder, and contains the updated run 562
manuscript draft.

## Next Decision

Refresh commit-preparation and next-action queue pointers so optional archive
handoff points to run 623.
