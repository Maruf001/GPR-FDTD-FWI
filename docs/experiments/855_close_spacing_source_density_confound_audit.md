# Experiment 855: Close-Spacing Source-Density Confound Audit

Date: 2026-06-19

## Purpose

Audit whether the close50-versus-close14 source-density comparison can be used
as a spacing-only causal claim, or whether it must be reported as a guarded
acquisition/geometry contrast.

This is a CPU-only synthesis of saved synthetic 2D summary tables and run
manifests. It does not run FDTD, FWI, detector scoring, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/111_close_spacing_source_density_confound_audit
```

Key artifacts:

```text
data/close_spacing_source_density_confound_summary.json
data/close_spacing_source_density_confound_family_summary.csv
data/close_spacing_source_density_confound_factors.csv
data/close_spacing_source_density_confound_claims.csv
data/close_spacing_source_density_confound_gates.csv
figures/close_spacing_source_density_confound_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         close_spacing_source_density_confound_audit
factor count:                         10
claim count:                           7
matched control factors:               5
intended spacing axes:                 1
acquisition confounds:                 1
geometry confounds:                    1
metadata gaps:                         1
context-only factors:                  1
close50 transition ready:              true
guarded cross-spacing contrast ready:  true
spacing-only causal claim ready:       false
ready for broad GPU queue:             false
ready for detector-seeded FWI:         false
ready for field FWI:                   false
ready for 3D/HPC handoff:              false
gpu priority:                          none
```

Matched controls:

```text
source3_seed_values
source3_replication_cases
source3_source_count
target_depths_and_radii
target0_target1_gap_mm
```

Non-matched factors:

```text
target1_target2_gap_mm: intended spacing axis, close50=50 mm, close14=14 mm
tx_rx_offset_mm:        acquisition confound, close50=40 mm, close14=45 mm
target2_absolute_x_mm:  geometry confound, close50=300 mm, close14=264 mm
receiver_sampling:      metadata caveat, older seed34 summaries omit the field
source5_context_scope:  context-only, close14 source5 is noise-boundary context
```

## Interpretation

The saved source-density evidence supports two manuscript-safe claims:

```text
1. Close50 Tx/Rx40 shows a within-family source-density transition:
   source3 fails across seeds 13/21/34, while source4 and source5 recover
   exact geometry.

2. Close14 Tx/Rx45 source3 is a strong near-exact three-seed context, so the
   close50 source3 failure should not be generalized to every close-spacing
   source3 acquisition.
```

The current archive does not support this stronger claim:

```text
Target spacing alone controls source3 success/failure across close14 and
close50.
```

That stronger spacing-only claim would require a deliberately matched narrow
probe, such as close14 source3 Tx/Rx40 seeds 13/21/34 or close50 source3
Tx/Rx45 seeds 13/21/34, run skip-existing and one family at a time. This audit
does not launch that probe and explicitly blocks broad GPU queues.

## Validation

Focused test:

```text
tests/test_close_spacing_source_density_confound_audit.py
2 passed
```

Figure validation:

```text
close_spacing_source_density_confound_audit.png: 2569x903,
nonwhite=0.2311, dynamic range=255
```
