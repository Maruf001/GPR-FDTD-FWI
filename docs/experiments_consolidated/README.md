# Consolidated Experiment Trackers

This folder holds append-only bundles for numbered experiment tracker documents.
These bundles are quick-audit views only: they do not allocate experiment IDs,
and the original files under `docs/experiments/` remain canonical.

## Full Tracker Bundles

The current full-audit bundle set uses 100 tracker IDs per file.

- `tracker_bundle_100_199.md`: 100 source docs
- `tracker_bundle_200_299.md`: 100 source docs
- `tracker_bundle_300_399.md`: 100 source docs
- `tracker_bundle_400_499.md`: 100 source docs
- `tracker_bundle_500_599.md`: 100 source docs
- `tracker_bundle_600_662.md`: 64 source docs

Manifest:

```text
docs/experiments_consolidated/tracker_bundle_manifest.json
```

## Historical Admin Bundles

The older admin-only bundles are retained for compatibility with the post-crash archive audit.

- `admin_tracker_bundle_101_140.md`
- `admin_tracker_bundle_141_180.md`
- `admin_tracker_bundle_181_220.md`
- `admin_tracker_bundle_221_271.md`

Historical manifest:

```text
docs/experiments_consolidated/admin_tracker_bundle_manifest.json
```

## Source Audit

```text
docs/archive_resolution/post535_735_resolution_audit.md
outputs/archive_resolution/post535_735_resolution_audit/tracker_doc_100_271_classification.csv
```
