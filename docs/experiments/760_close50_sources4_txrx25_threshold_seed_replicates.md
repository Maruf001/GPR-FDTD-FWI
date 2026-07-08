# Experiment 760: Close50 Sources4 Tx/Rx 25 mm Threshold Replicates

## Purpose

Resolve the unfinished close50 target2 acquisition branch around experiments
270-289. The earlier archive already showed that 4 sources at Tx/Rx 30, 35,
and 40 mm were exact across seeds 13, 21, and 34, while Tx/Rx 25 mm had only
one completed weak seed. This run fills the missing Tx/Rx 25 seed replicates
and aggregates the full 25/30/35/40 mm threshold.

This is a bounded synthetic 2D follow-up, not a broad new GPU sweep.

## Outputs

New completed runs:

```text
outputs/experiments/1219_coordinate_optimizer_close50_seed13_sources4_txrx25_objectives
outputs/experiments/1221_coordinate_optimizer_close50_seed21_sources4_txrx25_rerun_objectives
outputs/experiments/1222_coordinate_confidence_close50_sources4_txrx25_30_35_40_seed_replicates
```

Interrupted partial run excluded from the aggregate:

```text
outputs/experiments/1220_coordinate_optimizer_close50_seed21_sources4_txrx25_objectives
```

Aggregate artifact:

```text
outputs/experiments/1222_coordinate_confidence_close50_sources4_txrx25_30_35_40_seed_replicates/data/coordinate_confidence_aggregate.json
```

## Result

The completed aggregate has 30 confidence rows across target2, 4 sources, and
Tx/Rx offsets 25, 30, 35, and 40 mm.

| Tx/Rx offset | Rows | Truth geometry rows | X ambiguity rows | Min margin | Mean margin | Max margin |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 mm | 12 | 4 | 12 | 6.06e-05 | 3.31e-04 | 8.02e-04 |
| 30 mm | 6 | 6 | 0 | 1.70e-03 | 2.11e-03 | 2.30e-03 |
| 35 mm | 6 | 6 | 0 | 4.27e-03 | 5.19e-03 | 6.02e-03 |
| 40 mm | 6 | 6 | 0 | 4.82e-03 | 6.38e-03 | 8.14e-03 |

The Tx/Rx 25 mm replicate set is consistently ambiguous. Seed13 recovered the
truth radius but had a weak source-mismatch row; seed21 selected x=301 mm and
had one nominal row at 7.5 mm radius. All Tx/Rx 25 rows keep an ambiguity
interval spanning x=300-301 mm and radius 7.5-8.0 mm.

## Interpretation

For this close50 target2 setup with 4 sources:

```text
Tx/Rx 25 mm is below the robust acquisition threshold.
Tx/Rx 30 mm is the first tested offset that gives exact three-seed recovery.
Tx/Rx 35-40 mm increase confidence margin substantially.
```

This does not make 30 mm a universal resolution limit. It is a branch-specific
policy point for this geometry, source count, objective, and noise/mismatch
case set.

## Validation

```text
tests/test_coordinate_confidence_aggregate.py: 10 passed
aggregate figures validated nonblank:
  coordinate_confidence_aggregate.png nonwhite=0.1599
  coordinate_ambiguity_widths.png nonwhite=0.1131
```

The aggregate code was patched so mixed-era confidence rows with later
source-ringdown fields can be written safely using the union of row columns.

## Next Decision

Do not spend more local GPU time on this close50 target2 Tx/Rx 25 branch unless
the paper needs a finer acquisition-threshold bracket between 25 and 30 mm. The
next synthetic work should stay focused on unresolved target1 weak/exact
policy branches or field-to-synthetic calibration, not this now-closed target2
threshold.
