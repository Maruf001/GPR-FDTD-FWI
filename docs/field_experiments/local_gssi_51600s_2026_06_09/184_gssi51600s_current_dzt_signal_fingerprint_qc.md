# Field Experiment 184: Current DZT Signal Fingerprint QC

Date: 2026-06-27

## Purpose

Compute QC-only signal fingerprints from the current local GSSI DZT profiles.

This run does not relabel current files as controlled evidence, run field FWI,
launch GPU/HPC work, make a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/184_gssi51600s_current_dzt_signal_fingerprint_qc
```

Key artifacts:

```text
data/field_current_dzt_signal_fingerprint_rows.csv
data/field_current_dzt_signal_pair_similarity_rows.csv
data/field_current_dzt_signal_fingerprint_qc_summary.json
figures/field_current_dzt_signal_fingerprint_qc.png
docs/FIELD_CURRENT_DZT_SIGNAL_FINGERPRINT_QC.md
scripts/run_gssi_field_current_dzt_signal_fingerprint_qc.py
scripts/test_gssi_field_current_dzt_signal_fingerprint_qc.py
scripts/script_snapshot_manifest.json
```

## Result

```text
profile count:                    4
pair count:                       6
same-shape pair count:            1
minimum finite fraction:          1.0
minimum corrected RMS:            672555.0080031198
maximum corrected RMS:            1167517.21374859
maximum pair symmetric L2:        1.11957899163086
minimum pair correlation:         0.3740795978167496
signal fingerprint QC ready:      true
controlled archive ready:         false
provenance acceptance ready:      false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

Profile fingerprints:

| File | Traces | Corrected RMS | 0-1 ns RMS | 1-3 ns RMS | 3-5 ns RMS | Peak time ns |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PROJECT001C__013.DZT | 807 | 1156650.7348844311 | 1161151.9123371332 | 1615220.6052828769 | 248048.02111539256 | 1.1100196463654224 |
| PROJECT001C__014.DZT | 274 | 710274.7493624398 | 1022959.7076876392 | 843274.1651265053 | 163984.6017426554 | 0.9724950884086444 |
| PROJECT001C__015.DZT | 814 | 1167517.21374859 | 1568250.8591824467 | 1457378.8791880014 | 232556.51964987264 | 1.0510805500982319 |
| PROJECT001C__016.DZT | 274 | 672555.0080031198 | 707829.4858481648 | 928743.3897073531 | 133229.21050598723 | 1.0903732809430255 |

Same-shape QC pair:

| File A | File B | Corrected correlation | Corrected symmetric L2 |
| --- | --- | ---: | ---: |
| PROJECT001C__014.DZT | PROJECT001C__016.DZT | 0.3740795978167496 | 1.11957899163086 |

## Interpretation

The current DZT profiles are finite and suitable for signal-level QC. The
fingerprints quantify median-removed amplitude, time-window energy, and
same-shape short-profile similarity.

The same-shape pair is a QC comparison only. Its moderate correlation and large
symmetric L2 do not make it a controlled repeat, and the current archive still
lacks controlled file roles, surveyed geometry, target truth, time-zero
references, amplitude references, checksum ledger, and provenance reruns.

## Decision

Use these fingerprints as current-archive QC context. Keep controlled archive
acceptance, measured-field claims, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until a real controlled archive satisfies the
acceptance gates.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_dzt_signal_fingerprint_qc.py
sha256: 36b9053bfa30e25d33449363f2faf66e6163c9d0bfd5585fded1f30119f897e6

test_gssi_field_current_dzt_signal_fingerprint_qc.py
sha256: 3a11c5975697fe1895c47fadd0c92ff0121e40eaf6603cd7035039d311cdc2d9
```

Subsequent related field experiments should start from a duplicated
run-specific script.

## Validation

Focused field tests:

```text
tests/test_gssi_field_current_archive_evidence_boundary_classifier.py
tests/test_gssi_field_current_dzt_signal_fingerprint_qc.py
9 passed
```

Figure check:

```text
field_current_dzt_signal_fingerprint_qc.png
2680x846, dynamic range=255
```
