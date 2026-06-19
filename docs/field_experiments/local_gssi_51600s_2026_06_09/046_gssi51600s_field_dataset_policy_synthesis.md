# Field Experiment 046: GSSI 51600S Dataset Policy Through Stack Sensitivity

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the corrected short-profile
B-scan stack sensitivity analysis in field experiment 045.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/046_gssi51600s_field_dataset_policy_synthesis
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
| Corrected stack sensitivity | `corrected_profile_stack_window_robust` | 3/3 robust windows | B-scan time-zero QC only |

Current field-data statement:

```text
The corrected stack window-sensitivity check shows that the B-scan-level
relative time-zero improvement survives the tested shallow windows. The
dataset remains 2D line-profile timing/QC evidence, not a 3D survey or
measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_profile_stack_sensitivity.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 8349x835,
nonwhite=0.2698, dynamic range=255
```
