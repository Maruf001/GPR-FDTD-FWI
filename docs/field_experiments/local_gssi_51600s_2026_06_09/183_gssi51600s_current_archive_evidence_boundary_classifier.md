# Field Experiment 183: Current Archive Evidence Boundary Classifier

Date: 2026-06-27

## Purpose

Classify what the current local GSSI archive can support after the current
data inventory, DZX sidecar, and DZT/DZX consistency audits.

This run does not relabel current files as controlled evidence, run field FWI,
launch GPU/HPC work, make a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/183_gssi51600s_current_archive_evidence_boundary_classifier
```

Key artifacts:

```text
data/field_current_archive_evidence_boundary_rows.csv
data/field_current_archive_evidence_boundary_classifier_summary.json
figures/field_current_archive_evidence_boundary_classifier.png
docs/FIELD_CURRENT_ARCHIVE_EVIDENCE_BOUNDARY_CLASSIFIER.md
scripts/run_gssi_field_current_archive_evidence_boundary_classifier.py
scripts/test_gssi_field_current_archive_evidence_boundary_classifier.py
scripts/script_snapshot_manifest.json
```

## Result

```text
gate count:                         10
QC-supported gates:                 4
QC-supported passes:                4
controlled blocker gates:           6
controlled blocking failures:       6
current archive QC ready:           true
controlled evidence ready:          false
measured-field claim ready:         false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

Gate classification:

| Gate | Class | Status | Detail |
| --- | --- | --- | --- |
| raw_file_inventory | qc_supported | pass | 4 DZT files and 4 DZX sidecars |
| sidecar_pairing | qc_supported | pass | all current DZT files have DZX sidecars |
| acquisition_setting_qc | qc_supported | pass | 12 uniform acquisition settings |
| dzt_dzx_internal_consistency | qc_supported | pass | trace counts, scan spacing, profile lengths, and time-zero sample offset are internally consistent |
| controlled_file_roles | controlled_blocker | fail | no current DZT files are accepted as controlled profile, time-zero, or amplitude-reference files |
| controlled_metadata_artifacts | controlled_blocker | fail | required controlled metadata artifacts are absent |
| controlled_profile_geometry | controlled_blocker | fail | DZX waypoints do not recover controlled profile geometry |
| target_truth_provenance | controlled_blocker | fail | target truth and provenance artifact are not present in the current archive |
| checksum_and_provenance_rerun | controlled_blocker | fail | checksum ledger, intake manifest, structural rerun, and provenance rerun are still required |
| field_fwi_input | controlled_blocker | fail | field FWI remains blocked until controlled archive acceptance passes |

## Interpretation

The current archive is internally readable and useful for quality-control
context. It has a complete four-file DZT/DZX inventory, consistent sidecar
pairing, uniform acquisition settings, matching DZT/DZX trace counts, matching
profile lengths, and a consistent two-sample time-zero offset.

That is still not controlled measured evidence. The archive has no accepted
controlled file roles, no controlled metadata artifacts, no recoverable
controlled profile geometry from the DZX waypoints, no target-truth provenance,
and no checksum/intake/structural/provenance rerun.

## Decision

Use the current archive as QC context only. Keep measured-field claims, field
FWI, heavy GPU work, field 3D/HPC, and neural-network training blocked until a
real controlled archive satisfies the acceptance gates.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_archive_evidence_boundary_classifier.py
sha256: 81683fc45fe3eb1cb29995b65c117ba8a01d27ce4d267a408514e9509e468ffd

test_gssi_field_current_archive_evidence_boundary_classifier.py
sha256: 1824702ab597cf337b37015e8f04310e87a4453d2c0b94550b447d595bdb9969
```

Subsequent related field experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_archive_evidence_boundary_classifier.py
3 passed
```

Figure check:

```text
field_current_archive_evidence_boundary_classifier.png
2140x844, dynamic range=255
```
