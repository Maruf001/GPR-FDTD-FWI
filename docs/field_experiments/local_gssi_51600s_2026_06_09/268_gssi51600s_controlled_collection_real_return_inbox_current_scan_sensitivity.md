# Field Experiment 268: Controlled Collection Real-Return Inbox Current Scan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `267` inbox-scan validator with controlled damage cases.

This run does not create placeholder DZT files, ingest real data into an
accepted archive, run DZT preprocessing, run field FWI, launch GPU/HPC work, or
promote controlled field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/268_gssi51600s_controlled_collection_real_return_inbox_current_scan_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_inbox_current_scan_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_inbox_current_scan_sensitivity_summary.json
figures/field_controlled_collection_real_return_inbox_current_scan_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         35
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        34
observed failure scenarios:        34
unexpected outcomes:               0
sensitivity ready:                 true
exact run 266 accepted:            true
damaged variants rejected:         true
provenance acceptance ready:       false
real archive acceptance ready:     false
field FWI ready:                   false
gpu priority:                      none
```

Damage families rejected:

| Damage family | Examples |
| --- | --- |
| Required-file drift | removed file slot, false file presence, placeholder flag |
| Metadata drift | removed metadata row, filled metadata value |
| Checksum drift | removed checksum row, filled checksum |
| Unexpected files | extra staged file row |
| Summary drift | count drift, false source guard, false scan readiness |
| Downstream promotion | provenance, archive, evidence, FWI, and 3D/HPC flags forced true |
| Artifact drift | missing/weak figure validation and missing script snapshot hashes |

## Interpretation

The inbox-scan validator accepts the exact run `266` artifact set and rejects
every damaged variant. The current field intake status is now guarded: the
real-return inbox has no required DZT files, no measured metadata values, no
checksums, and no unexpected files.

## Decision

Use runs `266-268` as the guarded current field intake status checkpoint. Real
files, metadata, checksums, provenance acceptance, archive acceptance,
controlled evidence, field FWI, field 3D/HPC, and GPU escalation remain
blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_inbox_current_scan_sensitivity.py
3 passed
```

Figure validation:

```text
4211x919, dynamic range=255
```
