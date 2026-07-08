# Field Experiment 050: GSSI 51600S Dataset Policy Through Interval QC

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the supported-interval visual
QC package in field experiment 049.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/050_gssi51600s_field_dataset_policy_synthesis
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
| Supported interval visual QC | `supported_interval_visual_qc_ready` | min corrected interval abs corr 0.909 | supported regions only |

Current field-data statement:

```text
The supported-interval visual-QC package is the preferred corrected-stack
figure endpoint because it shows only all-window-supported regions. The local
GSSI dataset remains 2D line-profile timing/QC evidence, not a 3D survey or
measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_supported_interval_visual_qc.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 9641x835,
nonwhite=0.2658, dynamic range=255
```
