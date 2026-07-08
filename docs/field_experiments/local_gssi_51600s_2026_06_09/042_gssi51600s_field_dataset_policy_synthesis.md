# Field Experiment 042: GSSI 51600S Dataset Policy Through Trace Sensitivity

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the content-anchor
trace-alignment sensitivity analysis in field experiment 041.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/042_gssi51600s_field_dataset_policy_synthesis
```

Artifacts:

```text
data/field_dataset_policy_evidence.csv
data/field_dataset_policy_summary.json
data/figure_validation.csv
figures/field_dataset_policy.png
run_manifest.json
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Key added evidence:

| Evidence | Status | Key metric | Limitation |
| --- | --- | ---: | --- |
| Content anchor trace alignment sensitivity | `content_anchor_trace_alignment_window_robust` | 6/6 pair-window rows improved | window-robust time-zero QC only |

Current field-data statement:

```text
The relative time-zero transfer improves measured 014/016 trace agreement at
the two repeat-content anchors, and that improvement survives the tested short,
nominal, and wider windows. The dataset remains 2D line-profile timing/QC
evidence, not a 3D survey or measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_content_anchor_trace_alignment_sensitivity.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 7057x835, nonwhite=0.2712, dynamic range=255
```
