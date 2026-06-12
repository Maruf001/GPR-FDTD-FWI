# Experiment 662: Field Experiment Archive Split

## Purpose

Create a separate, dataset-aware output root for measured, lab, public, and
benchmark-data experiments before starting the next synthetic marathon run.
This prevents the current 1100+ synthetic archive from absorbing field-data
QC/calibration work into the same flat numbered stream.

No FDTD, FWI, optimizer, or GPU simulation was launched for this work.

## Context

Read:

```text
data/data_resarch.md
```

The research note does not support one generic field-data bucket. It identifies
multiple future data families with different import and validation assumptions:
local GSSI 51600S DZT/DZX data, public lab rebar data, public raw IDS `.dt`
field data, bridge-deck data, controlled test-site radargrams, corrosion data,
and synthetic FWI benchmarks.

## Archive Policy

Added:

```text
outputs/field_experiments/
outputs/field_experiments/local_gssi_51600s_2026_06_09/
docs/field_experiments/
docs/field_experiments/local_gssi_51600s_2026_06_09/
```

Future field/lab/public data runs should use:

```text
outputs/field_experiments/<dataset_id>/NNN_run_name
```

Run numbering is local to each dataset/source family. The synthetic archive
remains:

```text
outputs/experiments/NNN_run_name
```

Historical run `1119_gssi51600s_dzt_qc` remains in `outputs/experiments/` as
the pre-split GSSI QC baseline.

Field trackers now mirror the field output hierarchy:

```text
docs/field_experiments/<dataset_id>/NNN_run_name.md
```

The first field tracker is:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc.md
```

## Code Change

Updated:

```text
run_gssi_dzt_qc.py
tests/test_gssi_dzt_qc.py
```

The GSSI DZT QC script now defaults to:

```text
--field-root outputs/field_experiments
--dataset-id local_gssi_51600s_2026_06_09
```

The explicit `--outdir` override is preserved for reproducible historical
backfills.

Focused tests cover normal dataset-root construction and rejection of unsafe
dataset IDs such as absolute paths or parent-directory segments.

## Command

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_gssi_dzt_qc.py
```

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/001_gssi51600s_dzt_qc
```

Imported four GSSI 51600S DZT channel records:

```text
PROJECT001C__013.DZT ch0: 807 traces x 510 samples, 2.686398 m, ok
PROJECT001C__014.DZT ch0: 274 traces x 510 samples, 0.909909 m, ok
PROJECT001C__015.DZT ch0: 814 traces x 510 samples, 2.709729 m, ok
PROJECT001C__016.DZT ch0: 274 traces x 510 samples, 0.910000 m, missing_dzx_sidecar
```

Artifacts include:

```text
data/gssi_dzt_inventory.csv
data/gssi_dzt_qc_summary.json
figures/field_profile_qc_context.png
figures/gssi_dzt_inventory.png
figures/*_bscan_qc.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Figure Validation

All generated PNGs were readable and nonblank:

```text
PROJECT001C__013_ch0_bscan_qc.png: 2312x903, unique_colors=966, nonwhite_fraction=0.5848
PROJECT001C__014_ch0_bscan_qc.png: 2312x903, unique_colors=939, nonwhite_fraction=0.5665
PROJECT001C__015_ch0_bscan_qc.png: 2312x903, unique_colors=961, nonwhite_fraction=0.5772
PROJECT001C__016_ch0_bscan_qc.png: 2312x903, unique_colors=927, nonwhite_fraction=0.5599
field_profile_qc_context.png: 2144x937, unique_colors=612, nonwhite_fraction=0.3137
gssi_dzt_inventory.png: 2059x835, unique_colors=260, nonwhite_fraction=0.3371
```

## Validation

Focused test:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_gssi_dzt_qc.py
10 passed
```

Full suite and diff checks:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
324 passed in 37.94s

git diff --check
passed

git diff --name-status --diff-filter=D
no tracked deletions
```

## Next Decision

Keep field-data work parked behind CPU import/QC, metadata extraction,
time-zero and velocity calibration, and dimensionality checks. The next GPU
synthetic step remains seed591286729879 target0 8-source control.
