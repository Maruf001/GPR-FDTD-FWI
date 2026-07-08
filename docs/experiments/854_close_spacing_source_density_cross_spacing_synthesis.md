# Experiment 854: Close-Spacing Source-Density Cross-Spacing Synthesis

Date: 2026-06-18

## Purpose

Reconcile the completed close50 Tx/Rx40 source-count evidence with the
completed close14 Tx/Rx45 source3 evidence before making a manuscript claim
about source density.

This is a CPU-only synthesis of saved synthetic 2D coordinate-confidence
summary tables. It does not run FDTD, FWI, detector scoring, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/110_close_spacing_source_density_cross_spacing_synthesis
```

Key artifacts:

```text
data/close_spacing_source_density_cross_spacing_summary.json
data/close_spacing_source_density_cross_spacing_source_rows.csv
data/close_spacing_source_density_cross_spacing_comparisons.csv
data/close_spacing_source_density_cross_spacing_gates.csv
figures/close_spacing_source_density_cross_spacing_synthesis.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         close_spacing_source_density_cross_spacing_synthesis
source rows:                          6
comparison rows:                      6
families:                             close14, close50
source counts:                        3, 4, 5
matched seed values:                  13, 21, 34
close50 source3 replicated failure:   true
close50 source4/5 exact recovery:     true
close14 source3 near-exact context:   true
close14 source4/5 exact recovery:     true
source3 spacing-dependent contrast:   true
close50 source4 rescue supported:     true
close14 source4 cleanup supported:    true
universal source3 failure supported:  false
manuscript table ready:               true
cross-spacing generalization ready:   false
ready for broad GPU queue:            false
ready for detector-seeded FWI:        false
ready for field FWI:                  false
ready for 3D/HPC handoff:             false
gpu priority:                         none
```

Key comparison rows:

```text
close50 source3 -> source4:
  truth fraction +1.0000, weak fraction -1.0000, max x error -1.0 mm

close14 source3 -> source4:
  truth fraction +0.1667, weak fraction +0.0000, max x error -1.0 mm

close50 source3 -> close14 source3:
  truth fraction +0.8333, weak fraction -1.0000, replicated failure true -> false
```

## Interpretation

The close50 Tx/Rx40 source-density transition is now a clean three-seed result:
three sources fail across seeds 13/21/34, while four and five sources recover
the truth geometry across the same seeds.

The close14 Tx/Rx45 source3 evidence does not reproduce that failure. It is
strong, radius-exact, and near-exact across seeds 13/21/34, with one 1 mm
adjacent-x branch selection; source4 removes that residual branch but is not a
rescue from a replicated failure.

The manuscript-safe claim is therefore:

```text
Saved close-spacing evidence supports an acquisition/spacing interaction:
source density resolves a close50 Tx/Rx40 ambiguity, but the same three-source
failure should not be generalized to close14 Tx/Rx45.
```

This table is ready for manuscript source-density/claim-boundary use. It does
not justify broad GPU source-density sweeps, detector-seeded FWI, field FWI,
or 3D/HPC handoff.

## Validation

Focused test:

```text
tests/test_close_spacing_source_density_cross_spacing_synthesis.py
2 passed
```

Figure validation:

```text
close_spacing_source_density_cross_spacing_synthesis.png: 2365x903,
nonwhite=0.2286, dynamic range=255
```
