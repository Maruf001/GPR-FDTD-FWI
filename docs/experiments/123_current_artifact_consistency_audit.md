# Experiment 123: Current Artifact Consistency Audit

## Purpose

Audit the current post-sparse-hardening state for manifest, artifact, tracker,
category-symlink, archive-checksum, queue-pointer, and adjacent
sparse-reporting consistency.

## 590: Current Artifact Consistency Audit

Output:

```text
outputs/experiments/590_current_artifact_consistency_audit
```

Command:

```text
Inspect run manifests and declared artifacts for runs 584-589.
Inspect docs/experiments/117-122 and infrastructure symlinks 584-589.
Validate the run 580 archive SHA-256 and tar entry count.
Review adjacent confidence-reporting code for remaining sparse-metadata gaps.
```

Artifacts:

```text
README.md
data/current_artifact_consistency_audit.json
run_manifest.json
```

Validation:

```text
run_manifest.json parses as JSON
data/current_artifact_consistency_audit.json parses as JSON
git diff --check: clean after run 590
```

## Interpretation

The current local handoff state is internally consistent. The audit did not
change the current restart, validation, commit-summary, archive, or GPU-work
pointers, so no queue refresh is required.

## Next Decision

Continue CPU-only manuscript, archive-handoff, or commit-preparation work unless
a concrete bounded GPU evidence gap is selected.
