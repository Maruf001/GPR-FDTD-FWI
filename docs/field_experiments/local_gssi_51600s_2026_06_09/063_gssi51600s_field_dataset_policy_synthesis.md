# Field Experiment 063: GSSI 51600S Dataset Policy Through Publication Evidence

Date: 2026-06-17

## Purpose

CPU-only refresh of the dataset-level field policy after the long-profile
pattern visual QC, holdout QC, time-window sensitivity, spatial-width
sensitivity, and refreshed publication claim bundle.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/063_gssi51600s_field_dataset_policy_synthesis
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

Newly incorporated evidence:

```text
057 long pattern visual QC:              6 / 6 stable anchors supported
058 long pattern holdout QC:             8 / 8 candidate anchors supported
060 long holdout time-window sensitivity:24 / 24 rows supported
061 long holdout spatial-width sensitivity:24 / 24 rows supported
062 field publication claim bundle:      7 figure rows, 6 claim boundaries
```

Key policy metrics:

```text
survey classification:                   independent_2d_line_profiles
embedded segment candidate count:         0
long profile 013 phase-anchor picks:      missing
publication bundle ready:                 true
publication bundle gpu priority:          none
```

## Interpretation

The local GSSI 51600S field data now have a stronger long-profile pattern-QC
chain for the +0.06 ns pattern shift, including holdout and sensitivity
evidence. The dataset-level policy does not change: this remains measured 2D
line-profile QC, not a 3D survey or measured-data FWI benchmark. A heavy field
GPU/FWI run is still not justified without external survey-layout metadata and
a new measured-data objective.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py: 2 passed
```

Figure validation:

```text
field_dataset_policy.png: 12259x835,
nonwhite=0.2570, dynamic range=255
```
