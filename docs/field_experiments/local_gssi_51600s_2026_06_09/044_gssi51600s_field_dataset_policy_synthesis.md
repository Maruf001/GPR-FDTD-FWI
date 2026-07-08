# Field Experiment 044: GSSI 51600S Dataset Policy Through Corrected Stack

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the corrected short-profile
B-scan stack in field experiment 043.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/044_gssi51600s_field_dataset_policy_synthesis
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
| Corrected short-profile stack | `corrected_profile_stack_time_zero_supported` | matrix abs corr 0.536 -> 0.812 | B-scan time-zero QC only |

Current field-data statement:

```text
The corrected short-profile stack extends the relative time-zero correction
from content-anchor traces to the spatially aligned 014/016 B-scan window and
improves measured profile-level agreement. The dataset remains 2D line-profile
timing/QC evidence, not a 3D survey or measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_profile_stack.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 7703x835,
nonwhite=0.2701, dynamic range=255
```
