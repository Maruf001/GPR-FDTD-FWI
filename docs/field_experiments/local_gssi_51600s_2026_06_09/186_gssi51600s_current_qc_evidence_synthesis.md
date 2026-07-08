# Field Experiment 186: Current QC Evidence Synthesis

Date: 2026-06-27

## Purpose

Synthesize the current archive boundary and signal-quality evidence from runs
`183`, `184`, and `185` without promoting the current files into controlled
measured evidence.

This is a CPU-only evidence synthesis. It does not run field FWI, heavy GPU
work, field 3D/HPC work, DZT reprocessing beyond the upstream QC runs, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/186_gssi51600s_current_qc_evidence_synthesis
```

Key artifacts:

```text
data/field_current_qc_evidence_synthesis_rows.csv
data/field_current_qc_evidence_synthesis_summary.json
figures/field_current_qc_evidence_synthesis.png
docs/FIELD_CURRENT_QC_EVIDENCE_SYNTHESIS.md
scripts/script_snapshot_manifest.json
```

## Result

```text
evidence items:                     7
QC-context items:                   4
QC-context passes:                  4
controlled blocker items:           3
controlled blocking failures:       3
current archive QC context ready:   true
controlled evidence ready:          false
measured-field claim ready:         false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

Evidence rows:

| Item | Class | Status | Metric |
| --- | --- | --- | --- |
| archive_qc_gate | qc_context | pass | 4/4 QC gates pass |
| controlled_evidence_gate | controlled_blocker | fail | 6 blocking failures |
| finite_signal_fingerprint | qc_context | pass | min finite fraction=1.0 |
| same_shape_signal_pair | qc_context | pass | same-shape pair correlation=0.3740795978167496 |
| normalized_pairwise_signal_qc | qc_context | pass | max normalized correlation=0.3740795978167496 |
| controlled_repeat_evidence | controlled_blocker | fail | no current pair accepted as a controlled repeat |
| field_fwi_input_gate | controlled_blocker | fail | field FWI remains blocked |

## Interpretation

The current archive now has a concise evidence boundary. Inventory, sidecar
pairing, internal DZT/DZX consistency, finite signal fingerprints, and
normalized pairwise signal comparisons are valid QC context. They show that the
current files are readable and internally coherent enough for quality-control
description.

The same evidence does not close controlled collection requirements. The
current archive still lacks controlled file roles, controlled metadata,
surveyed profile geometry, target-truth provenance, measured time-zero
references, measured amplitude references, checksum/intake reruns, structural
reruns, and provenance reruns.

## Decision

Use the current archive as QC context only. Do not make measured-field claims,
run field FWI, launch heavy GPU work, launch field 3D/HPC work, or train neural
networks from the current archive until a real controlled archive satisfies the
acceptance gates.

## Validation

Focused test:

```text
tests/test_gssi_field_current_qc_evidence_synthesis.py
3 passed
```

Figure validation:

```text
field_current_qc_evidence_synthesis.png
1960x790, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_current_qc_evidence_synthesis.py
sha256=a22efae80d00992c3cebf684372128e225717a896806a1fa2064f309c8143928

tests/test_gssi_field_current_qc_evidence_synthesis.py
sha256=ebab98398ae086a44bd77f06a277b78958140d27fba429619d528bffcadfe070
```
