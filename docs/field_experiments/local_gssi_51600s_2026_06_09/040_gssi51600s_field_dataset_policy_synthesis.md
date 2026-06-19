# Field Experiment 040: GSSI 51600S Dataset Policy Through Trace Alignment

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the measured content-anchor
trace-alignment packet in field experiment 039.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/040_gssi51600s_field_dataset_policy_synthesis
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
| Content anchor trace alignment | `content_anchor_field_trace_alignment_improves_after_time_zero` | mean abs corr 0.301 -> 0.964 | measured trace time-zero QC only |

Current field-data statement:

```text
The local GSSI 51600S dataset remains 2D line-profile QC and timing evidence.
The relative time-zero transfer improves measured 014/016 trace agreement at
the two repeat-content anchors, but the dataset is still not a 3D survey, field
geometry inversion, or measured-data FWI benchmark.
```

## Interpretation

This refresh strengthens the field timing story with a direct measured-trace
before/after check. It does not change the dataset boundary: the evidence is
for phase/time-zero anchoring and visual QC, not inversion.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_anchor_trace_alignment.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 6445x835, nonwhite=0.2675, dynamic range=255
```
