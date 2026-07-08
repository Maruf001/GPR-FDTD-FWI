# Experiment 848: Close50 Tx/Rx40 Source-Count Three-Seed Synthesis

Date: 2026-06-18

## Purpose

Close the narrow source-count question opened by the branch-preservation
readiness scorecard. The specific question is whether the old close50 target2
Tx/Rx40 `sources3` seed34 failure is seed-specific, or whether three sources
are genuinely too sparse for this setup while four and five sources remain
clean.

This is a bounded synthetic 2D follow-up. It is not a broad GPU queue, field
work, detector-seeded FWI, 3D/HPC work, or neural-network training.

## Output

New bounded GPU runs:

```text
outputs/experiments/1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives
outputs/experiments/1345_coordinate_optimizer_close50_seed21_sources3_txrx40_objectives
```

Synthesis outputs:

```text
outputs/summary_tables/097_close50_branch_preservation_probe_readiness
outputs/summary_tables/098_close50_source_count_replicate_synthesis
outputs/summary_tables/099_close50_source_count_replicate_synthesis
```

Run `099` is the closed synthesis after seed21 was added.

## Result

```text
source3 seed13 final:        x=299 mm, z=90 mm, r=7.5 mm
source3 seed21 final:        x=299 mm, z=90 mm, r=7.5 mm
source3 seed34 final:        x=299 mm, z=90 mm, r=7.5 mm
source3 truth fraction:      0/6 rows
source3 weak rows:           6/6 rows
source4 truth fraction:      6/6 rows
source4 strong rows:         6/6 rows
source5 truth fraction:      6/6 rows
source5 strong rows:         6/6 rows
source3 seeds:               13,21,34
source-count transition:     supported
additional GPU ready:        false
broad GPU queue ready:       false
detector-seeded FWI ready:   false
gpu priority:                none
```

Run times:

```text
1344 seed13: 1521.50 s
1345 seed21: 1493.55 s
```

## Interpretation

The source3 result is now replicated across the same seeds used by the clean
source4/source5 comparisons. At close50 target2 with Tx/Rx40, three sources
consistently select the nearby wrong branch `x=299 mm, r=7.5 mm`, while the
saved source4 and source5 three-seed evidence selects the exact
`x=300 mm, r=8.0 mm` branch with strong confidence.

This is useful publication evidence because it is not just another close50
spacing threshold. It isolates source density as an acquisition-design control:
the same Tx/Rx offset can be clean with four or five sources but not with three
sources.

No more GPU replication is justified for this local source-count question.

## Validation

Focused tests:

```text
tests/test_close50_source_count_replicate_synthesis.py
tests/test_close50_branch_preservation_probe_readiness.py
tests/test_gssi_field_controlled_acquisition_design.py
6 passed
```

Final synthesis figure validation:

```text
close50_source_count_replicate_synthesis.png: 2263x869,
nonwhite=0.3227, dynamic range=255
```
