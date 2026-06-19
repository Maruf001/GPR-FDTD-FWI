# Field Experiment 052: GSSI 51600S Dataset Policy Through Long Transfer Audit

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the long-profile transfer
audit in field experiment 051.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/052_gssi51600s_field_dataset_policy_synthesis
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
| Long-pair short-correction transfer audit | `long_profile_short_correction_transfer_not_supported` | matrix abs corr 0.763 -> 0.732 | 0/6 stable anchor windows improved |

Current field-data statement:

```text
The supported short-pair correction remains useful for 014/016 visual QC, but
it should not be generalized to the 015/013 long pair. The local GSSI dataset
remains 2D line-profile timing/QC evidence, not a 3D survey or measured-data
FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_transfer_audit.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 10287x835,
nonwhite=0.2605, dynamic range=255
```
