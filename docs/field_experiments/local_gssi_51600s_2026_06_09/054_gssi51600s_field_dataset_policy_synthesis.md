# Field Experiment 054: GSSI 51600S Dataset Policy Through Long Shift Scan

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the long-profile shift scan in
field experiment 053.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/054_gssi51600s_field_dataset_policy_synthesis
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
| Long-pair pattern shift scan | `long_profile_shift_scan_rejects_short_transfer` | best matrix abs corr 0.939 at +0.060 ns | pattern-only, no phase-anchor picks |

Current field-data statement:

```text
The long pair has a strong pattern-only shift near +0.06 ns, but the inherited
014/016 short-pair offset is worse than zero for 015/013. The local GSSI
dataset remains 2D line-profile timing/QC evidence, not a 3D survey or
measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_shift_scan.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 10933x835,
nonwhite=0.2602, dynamic range=255
```
