# Experiment 187: Current State Archive Coverage Audit

## Purpose

Audit whether the run 633 handoff archive covers the current post-archive
state through run 653 without rebuilding the archive.

## 654: Current State Archive Coverage Audit

Output:

```text
outputs/experiments/654_current_state_archive_coverage_audit
```

Command:

```text
Build the current handoff dependency list from the run 633 archive file list,
add run 633 itself, local post-archive runs 634-653, and docs/experiments
166-186, then compare path coverage and file SHA-256 hashes against the run
633 archive.
```

Artifacts:

```text
README.md
data/current_state_archive_coverage_audit.json
data/current_state_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
base dependency paths: 257
base files: 682
base total size: 260.7 MiB
paths not covered by run 633 archive: 42
files missing from run 633 archive: 99
files changed since run 633 archive: 6
archive recommended: true for external handoff
git diff --check: clean after run 654
```

## Interpretation

Run 633 remains checksum-valid but no longer covers the current local state. A
refreshed archive is justified for an external handoff, but the audit stops
short of creating one to avoid repeated 128M archive churn during local
marathon work.

## Next Decision

Refresh commit-preparation and next-action queue pointers so they reference the
archive coverage audit. Keep run 633 as the packaged archive unless an external
handoff is needed.

