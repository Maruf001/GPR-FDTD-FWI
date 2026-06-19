# Field Experiment 048: GSSI 51600S Dataset Policy Through Spatial Support

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the corrected-stack spatial
support mask in field experiment 047.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/048_gssi51600s_field_dataset_policy_synthesis
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
| Corrected stack spatial support | `corrected_stack_spatial_support_sparse` | 105/249 majority-supported columns | Spatial mask limits visual QC |

Current field-data statement:

```text
The corrected stack improves aggregate B-scan agreement and is window-robust,
but the spatial support mask is sparse. Use supported intervals only for
visual QC. The dataset remains 2D line-profile timing/QC evidence, not a 3D
survey or measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_stack_spatial_support.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 8995x835,
nonwhite=0.2662, dynamic range=255
```
