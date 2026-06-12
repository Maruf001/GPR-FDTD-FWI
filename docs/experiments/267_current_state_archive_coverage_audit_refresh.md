# Experiment 267: Current State Archive Coverage Audit Refresh

## Purpose

Refresh the archive-coverage audit after the run 730-733 manuscript-validation
refresh chain without rebuilding the handoff archive.

## 734: Current State Archive Coverage Audit Refresh

Output:

```text
outputs/experiments/734_current_state_archive_coverage_audit_refresh
```

Command:

```text
Compare the run 633 archive file list and tarball contents against the current
base path list through outputs/experiments/733 and docs/experiments/266.
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
base dependency paths: 419
archive input paths: 420
base files: 1060
base total size: 262.9 MiB
missing paths: 0
paths not covered by run 633 archive: 204
files missing from run 633 archive: 477
files changed since run 633 archive: 8
run 633 archive SHA-256: verified
run 633 archive entry count: 805
archive recommended for external handoff: true
git diff --check: clean after run 734
```

## Interpretation

Run 633 remains checksum-valid but stale for current local state through run
733 and docs/experiments/266. Rebuild the archive only for explicit external
handoff; otherwise continue local reporting/commit work.

## Next Decision

Refresh commit-preparation and next-action queue pointers only if archive
coverage must be made current in the live queue.
