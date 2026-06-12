# Field Experiment 001: Local GSSI 51600S DZT QC

## Purpose

CPU-only import and QC baseline for the local reinforced-concrete GSSI model
51600S field data. This is a parser, metadata, and B-scan inspection run, not
a 2D or 3D FWI experiment.

## Data Source

```text
data/2026-06-09_GSSI_model_51600S
```

Field archive dataset family:

```text
local_gssi_51600s_2026_06_09
```

## Command

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_gssi_dzt_qc.py \
  --input-dir data/2026-06-09_GSSI_model_51600S \
  --field-root outputs/field_experiments \
  --dataset-id local_gssi_51600s_2026_06_09 \
  --outdir outputs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc
```

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc
```

Historical pre-split baseline:

```text
outputs/experiments/1119_gssi51600s_dzt_qc
```

## Results

Imported four DZT channel records with `readgssi` 0.0.22:

```text
PROJECT001C__013.DZT ch0: 807 traces x 510 samples, 2.686398 m, ok
PROJECT001C__014.DZT ch0: 274 traces x 510 samples, 0.909909 m, ok
PROJECT001C__015.DZT ch0: 814 traces x 510 samples, 2.709729 m, ok
PROJECT001C__016.DZT ch0: 274 traces x 510 samples, 0.909909 m, ok
```

The 2026-06-11 refresh includes `PROJECT001C__016.DZX`; missing DZX sidecars
are now `none`. The only remaining sidecar-level caveat is that no `.DZG`
GPS/position file is present.

Artifacts:

```text
data/gssi_dzt_inventory.csv
data/gssi_dzt_qc_summary.json
figures/field_profile_qc_context.png
figures/gssi_dzt_inventory.png
figures/*_bscan_qc.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Interpretation

The import path is usable for profile-level QC and future velocity/time-zero
calibration. The available metadata do not reconstruct a full 3D survey
geometry, so this field dataset stays parked behind CPU QC and calibration
before any measured-data FWI claim.
