# Experiment 243: Current State Archive Coverage Audit Refresh

## Purpose

Refresh the archive coverage audit for the current local state through run 709
without building a new archive.

## 710: Current State Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/710_current_state_archive_coverage_audit_refresh
```

Command:

```text
Compare the run 633 archive file list and tarball contents against the current
base path list through outputs/experiments/709 and docs/experiments/242.
```

Artifacts:

```text
README.md
data/current_state_archive_coverage_audit_refresh.json
data/current_state_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 371
archive input paths: 372
base files: 947
base total size: 262.0 MiB
missing paths: 0
paths not covered by run 633 archive: 156
files missing from run 633 archive: 364
files changed since run 633 archive: 8
run 633 archive SHA-256: verified
run 633 archive entry count: 805
archive recommended for external handoff: true
git diff --check: clean after run 710
```

## Interpretation

Run 633 remains checksum-valid but stale. A refreshed archive is justified only
when an external handoff is needed; otherwise keep run 633 as the current
packaged archive and avoid repeated 128M archive churn.

## Next Decision

Refresh commit-preparation and next-action queue pointers so archive coverage
points to run 710.

