# Field Experiment 038: GSSI 51600S Dataset Policy Through Content Time-Zero Anchors

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the content time-zero anchor
policy in field experiment 037.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/038_gssi51600s_field_dataset_policy_synthesis
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
| Content time-zero anchors | `short_profile_content_time_zero_anchor_supported_for_visual_qc` | supported content anchors = 2/2 | time-zero visual QC only |

Current field-data statement:

```text
The local GSSI 51600S dataset remains 2D line-profile QC and timing evidence.
The short pair 014/016 is the strongest repeat/timing anchor. The two
repeat-content events are supported as measured-data time-zero and visual-QC
anchors only. The dataset is still not a 3D survey, field geometry inversion,
or measured-data FWI benchmark.
```

## Interpretation

This refresh makes the dataset-level policy current through experiment 037.
The new anchor evidence strengthens the measured-data QC story but does not
move the dataset into field inversion or 3D territory.

## Validation

Focused tests:

```text
tests/test_gssi_field_content_time_zero_anchor_policy.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 5833x835, nonwhite=0.2657, dynamic range=255
```
