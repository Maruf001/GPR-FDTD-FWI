# Experiment 113: Current Handoff Archive

## Purpose

Package the current manuscript and handoff dependency set after the run 579
size and coverage audit.

## 580: Current Handoff Archive

Output:

```text
outputs/experiments/580_current_handoff_archive
```

Command:

```text
tar -czf outputs/experiments/580_current_handoff_archive/current_handoff_archive.tar.gz \
  -T outputs/experiments/580_current_handoff_archive/data/current_handoff_archive_file_list.txt
sha256sum outputs/experiments/580_current_handoff_archive/current_handoff_archive.tar.gz
tar -tzf outputs/experiments/580_current_handoff_archive/current_handoff_archive.tar.gz | wc -l
```

Artifacts:

```text
current_handoff_archive.tar.gz
data/current_handoff_archive.json
data/current_handoff_archive_file_list.txt
run_manifest.json
```

Validation:

```text
input paths: 116
archive entries: 487
compressed size: 7.9M
sha256: 72778e0b0e1998fbee83a28d0132010ade4729af2c7429bcbb253631e4d4cc22
```

## Interpretation

The current handoff archive supersedes run 555 for optional current external
handoff. It includes the run 579 audit folder but intentionally excludes the
run580 folder to avoid a self-referential archive.

## Next Decision

Refresh the action queue so optional archive handoff points to run 580.
