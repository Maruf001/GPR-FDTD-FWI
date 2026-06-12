# Local GSSI 51600S 2026-06-09

Dataset family for the local reinforced-concrete GSSI model 51600S data:

```text
data/2026-06-09_GSSI_model_51600S
```

This family is for CPU-only import/QC, metadata inventory, B-scan inspection,
velocity or time-zero calibration, and later field-to-synthetic comparison.
It is not a 3D FWI archive by itself.

The first historical QC run was written before the archive split:

```text
outputs/experiments/1119_gssi51600s_dzt_qc
```

Future runs should use this dataset-local sequence:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/NNN_run_name
```
