# Field Experiment 182: Current DZT/DZX Consistency Audit

Date: 2026-06-27

## Purpose

Cross-check the current DZT import records from the original QC run against the
current DZX sidecar metadata from run `181`.

This run does not relabel current files as controlled evidence, run field FWI,
launch GPU/HPC work, make a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/182_gssi51600s_current_dzt_dzx_consistency_audit
```

Key artifacts:

```text
data/field_current_dzt_dzx_consistency_rows.csv
data/field_current_dzt_dzx_consistency_audit_summary.json
figures/field_current_dzt_dzx_consistency_audit.png
docs/FIELD_CURRENT_DZT_DZX_CONSISTENCY_AUDIT.md
scripts/run_gssi_field_current_dzt_dzx_consistency_audit.py
scripts/test_gssi_field_current_dzt_dzx_consistency_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
profile count:                         4
trace-count matches:                   4
sample delta matches time-zero offset: 4
warning rows:                          0
max scan-spacing difference (m):       0.0
max profile-length difference (m):     0.0
sample delta values:                   [2]
current archive internal consistency:  true
sidecar metadata useful for QC:        true
controlled archive acceptance ready:   false
provenance acceptance ready:           false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

File-level consistency:

| File | DZT traces | DZX trace count | Read samples | DZX samples | Sample delta | Profile length match |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| PROJECT001C__013.DZT | 807 | 807 | 510 | 512 | 2 | true |
| PROJECT001C__014.DZT | 274 | 274 | 510 | 512 | 2 | true |
| PROJECT001C__015.DZT | 814 | 814 | 510 | 512 | 2 | true |
| PROJECT001C__016.DZT | 274 | 274 | 510 | 512 | 2 | true |

## Interpretation

The current DZT files and DZX sidecars are internally consistent for basic
profile QC. Trace counts match exactly, scan-derived profile lengths match, and
the two-sample difference between DZX/header samples per scan and read profile
samples matches the stored time-zero sample offset.

This strengthens the current-archive QC interpretation. It does not create
controlled measured evidence because file roles, target truth, surveyed
geometry, checksum ledger, provenance notes, and measured reference files are
still missing.

## Decision

Treat the current archive as internally readable and useful for QC. Do not
promote it to controlled measured evidence, measured-field claims, field FWI,
heavy GPU work, field 3D/HPC, or neural-network training.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_dzt_dzx_consistency_audit.py
sha256: 55b38996c2ac30dd1083f91b16b24ee0085a5d2eba0c74925bcb7b31730a1cb3

test_gssi_field_current_dzt_dzx_consistency_audit.py
sha256: 8f6f5319b0c3c8cd86cfcc64c693e77260fb0cba3f75421ee79992cd4f772847
```

Subsequent related field experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_dzt_dzx_consistency_audit.py
3 passed
```

Figure check:

```text
field_current_dzt_dzx_consistency_audit.png
2680x846, dynamic range=255
```
