# BEM Experiment 872: Panel-116 Worst-Bin Aperture Trim Scorecard

Date: 2026-07-01

## Purpose

Check whether trimming receiver-aperture edges repairs the worst remaining
116-panel high-band frequency bin.

This run reads the saved run `869` receiver residual rows. It does not rerun
BEM, FDTD, field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/872_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_score_rows.csv
data/scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_summary.json
figures/scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source spatial audit ready:             true
source validation ready:                true
source sensitivity ready:               true
receiver rows:                          13
score rows:                             6
frequency:                              2.3125 GHz
target relative L2:                     0.001
full aperture relative L2:              0.002030466081391074
strict-center relative L2:              0.001938978012629881
edge-quarters relative L2:              0.0021015204146441102
best subset:                            strict_center_non_edge
best subset relative L2:                0.001938978012629881
any aperture subset passes target:      false
edge trim repairs worst bin:            false
worst-bin mismatch survives interior:   true
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The edge quarters are slightly worse than the center, but aperture trimming
does not repair the worst high-band bin. The strict-center subset is the best
subset, yet its complex relative L2 remains about `0.00194`, above the target
of `0.001`.

This means the remaining mismatch is not just an edge-receiver artifact. The
next explanation must involve the source/receiver spatial model, the
high-frequency boundary response, or another shape-related effect.

## Decision

Keep this as no-repair diagnostic evidence. Do not promote aperture trimming,
hard per-frequency acceptance, project-FDTD comparison, field transfer, or
3D/HPC claims from this result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard.py
3 passed
```

Figure check:

```text
2644x850, dynamic range=255
```
