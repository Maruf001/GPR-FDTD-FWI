# Experiment 84: Commit And Archive Inventory

## Purpose

Summarize the dirty worktree after the reporting checkpoint and separate code,
documentation, and ignored output artifacts for cleanup planning.

## 551: Commit And Archive Inventory

Output:

```text
outputs/experiments/551_commit_archive_inventory
```

Command:

```text
git diff --name-only
git ls-files --others --exclude-standard docs/experiments
find outputs/experiments -maxdepth 1 -type d -regex '.*/5[2-5][0-9].*' -printf '%f\n'
git status --ignored --short outputs/experiments/543_compact_objective_summary_figure outputs/experiments/550_archive_status_checkpoint
```

Artifacts:

```text
README.md
data/commit_archive_inventory.json
run_manifest.json
```

Result:

```text
tracked modified files: 8
new experiment trackers: docs/experiments/55 through docs/experiments/83
outputs/experiments: ignored by git
commit made: false
```

## Interpretation

The code/test changes are separable from the research/reporting documentation
and the ignored output archive. Do not force-add output artifacts unless an
explicit archive policy calls for it.

## Next Decision

Choose between code/docs commit preparation, separate output archiving, or
continued manuscript editing.
