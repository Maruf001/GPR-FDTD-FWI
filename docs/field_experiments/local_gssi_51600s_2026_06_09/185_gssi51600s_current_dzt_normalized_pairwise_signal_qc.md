# Field Experiment 185: Current DZT Normalized Pairwise Signal QC

Date: 2026-06-27

## Purpose

Compare current DZT profiles after median-background removal and trace-axis
normalization.

This run does not relabel current files as controlled repeats, run field FWI,
launch GPU/HPC work, make a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/185_gssi51600s_current_dzt_normalized_pairwise_signal_qc
```

Key artifacts:

```text
data/field_current_dzt_normalized_pairwise_signal_qc_rows.csv
data/field_current_dzt_normalized_pairwise_signal_qc_summary.json
figures/field_current_dzt_normalized_pairwise_signal_qc.png
docs/FIELD_CURRENT_DZT_NORMALIZED_PAIRWISE_SIGNAL_QC.md
scripts/run_gssi_field_current_dzt_normalized_pairwise_signal_qc.py
scripts/test_gssi_field_current_dzt_normalized_pairwise_signal_qc.py
scripts/script_snapshot_manifest.json
```

## Result

```text
pair count:                         6
normalized comparable pairs:        6
same-shape pairs:                   1
max normalized correlation:         0.3740795978167496
min normalized correlation:         -0.06546123409781655
min normalized symmetric L2:        1.11957899163086
max normalized symmetric L2:        1.5047709692568112
best correlation pair:              PROJECT001C__014.DZT::PROJECT001C__016.DZT
normalized pairwise QC ready:       true
controlled repeat evidence ready:   false
controlled archive ready:           false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

Pairwise QC:

| File A | File B | Normalized traces | Correlation | Symmetric L2 | Controlled repeat |
| --- | --- | ---: | ---: | ---: | --- |
| PROJECT001C__013.DZT | PROJECT001C__014.DZT | 274 | -0.0034501302817570236 | 1.4557117644192208 | false |
| PROJECT001C__013.DZT | PROJECT001C__015.DZT | 807 | 0.0661424860603232 | 1.366655170329219 | false |
| PROJECT001C__013.DZT | PROJECT001C__016.DZT | 274 | -0.033521515430483095 | 1.4834270576781452 | false |
| PROJECT001C__014.DZT | PROJECT001C__015.DZT | 274 | -0.05005950835712479 | 1.4869660342631694 | false |
| PROJECT001C__014.DZT | PROJECT001C__016.DZT | 274 | 0.3740795978167496 | 1.11957899163086 | false |
| PROJECT001C__015.DZT | PROJECT001C__016.DZT | 274 | -0.06546123409781655 | 1.5047709692568112 | false |

## Interpretation

Trace-axis normalization makes all current profiles comparable for signal QC.
The resulting correlations and symmetric L2 values are descriptive QC metrics
only. The best pair is still weak compared with what would be expected from a
controlled repeat, and the archive lacks controlled profile roles and surveyed
geometry.

## Decision

Use normalized pairwise metrics as current-archive QC context. Do not treat
them as controlled repeat evidence, measured-field proof, field FWI readiness,
heavy GPU readiness, field 3D/HPC readiness, or neural-network training
readiness.

## Milestone Snapshot

This result-driven field milestone froze:

```text
run_gssi_field_current_dzt_normalized_pairwise_signal_qc.py
sha256: b61b1df75a1219ae7166913f3cc050bd35213a24cc3cfef4c52b6bf95aedbb4b

test_gssi_field_current_dzt_normalized_pairwise_signal_qc.py
sha256: a5120d73c26331a26e5f9fd0501d42c27e0dd9e7c19df2d8107593b3218342f1
```

Subsequent related field experiments should start from a duplicated
run-specific script.

## Validation

Focused signal-QC tests:

```text
tests/test_gssi_field_current_dzt_signal_fingerprint_qc.py
tests/test_gssi_field_current_dzt_normalized_pairwise_signal_qc.py
10 passed
```

Figure check:

```text
field_current_dzt_normalized_pairwise_signal_qc.png
2680x846, dynamic range=255
```
