# Field Experiment 181: Current DZX Sidecar Metadata Audit

Date: 2026-06-27

## Purpose

Extract acquisition and profile metadata from the four current local GSSI DZX
sidecars and decide what those sidecars can and cannot support.

This run does not relabel current files as controlled evidence, run DZT
preprocessing, run field FWI, launch GPU/HPC work, make a measured-field claim,
or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/181_gssi51600s_current_dzx_sidecar_metadata_audit
```

Key artifacts:

```text
data/field_current_dzx_sidecar_metadata_rows.csv
data/field_current_dzx_sidecar_profile_groups.csv
data/field_current_dzx_sidecar_metadata_audit_summary.json
figures/field_current_dzx_sidecar_metadata_audit.png
docs/FIELD_CURRENT_DZX_SIDECAR_METADATA_AUDIT.md
scripts/run_gssi_field_current_dzx_sidecar_metadata_audit.py
scripts/test_gssi_field_current_dzx_sidecar_metadata_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
DZX sidecars:                             4
paired DZT files:                         4
uniform acquisition-setting fields:       12
profile scan-interval groups:             3
scan interval counts:                     273, 806, 813
max waypoint/scan-length ratio:           0.0036615384615384613
waypoints recover profile length:         false
sidecar metadata useful for QC:           true
sidecar metadata sufficient for geometry: false
controlled archive acceptance ready:      false
provenance acceptance ready:              false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

Profile groups:

| Scan intervals | Files | Mean scan-derived length (m) | Mean waypoint length (m) |
| ---: | ---: | ---: | ---: |
| 273 | 2 | 0.91 | 0.003332 |
| 806 | 1 | 2.6866666666666665 | 0.003332 |
| 813 | 1 | 2.71 | 0.003332 |

## Interpretation

The DZX sidecars are useful current-archive quality-control metadata. They
consistently record the SIR4K system, software version, antenna identity,
display dielectric setting, scan spacing, samples per scan, scan rate, transmit
rate, and depth range.

They do not recover controlled profile geometry. The scan ranges imply profile
lengths around `0.91 m`, `2.69 m`, and `2.71 m`, while the waypoint coordinate
span is only `0.003332 m` in each file. That is about one scan step, not the
full profile length. The sidecars therefore cannot replace a surveyed
profile-geometry artifact.

## Decision

Use the DZX sidecars as current-archive QC metadata only. Do not use them as a
substitute for controlled profile geometry, target truth, checksum ledger,
provenance notes, or measured reference files.

The current archive still does not satisfy the run `176` real-archive
acceptance contract. Measured-field claims, field FWI, heavy GPU work, field
3D/HPC, and neural-network training remain blocked.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_dzx_sidecar_metadata_audit.py
sha256: e3de61e7a628fc15c7bf59af0394e5fe8417e611b494f716f17af64cbf40a3aa

test_gssi_field_current_dzx_sidecar_metadata_audit.py
sha256: 806f1e81d14d06508060cba43bd336cbf7704fad54cbad46a8504dbe0ef150d0
```

Subsequent related field experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_dzx_sidecar_metadata_audit.py
4 passed
```

Figure check:

```text
field_current_dzx_sidecar_metadata_audit.png
2680x845, dynamic range=255
```
