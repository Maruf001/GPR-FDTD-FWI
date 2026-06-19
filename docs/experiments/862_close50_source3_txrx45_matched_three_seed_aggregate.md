# Experiment 862: Close50 Source3 Tx/Rx45 Matched Three-Seed Aggregate

Date: 2026-06-19

## Purpose

Complete and aggregate the reciprocal close50 source3 Tx/Rx45 matched-control
family from experiment `856`. This records the guarded seed `34` optimizer run
and the three-seed confidence aggregate across seeds `13`, `21`, and `34`.

This is a narrow synthetic 2D matched-control result. It is not a broad GPU
queue, field work, detector-seeded FWI, 3D/HPC work, or neural-network
training.

## Output

Seed34 optimizer run:

```text
outputs/experiments/1354_coordinate_optimizer_close50_seed34_sources3_txrx45_objectives
```

Seed34 resource guard:

```text
outputs/resource_guards/1354_close50_seed34_sources3_txrx45_monitor.jsonl
outputs/resource_guards/1354_close50_seed34_sources3_txrx45_guard_summary.json
```

Three-seed aggregate:

```text
outputs/experiments/1355_coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
```

Refreshed queue endpoint:

```text
outputs/summary_tables/120_close_spacing_matched_source3_probe_queue
```

## Seed34 Result

```text
run name:                    coordinate_optimizer_close50_seed34_sources3_txrx45_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                45 mm
target2 truth:               x=300 mm, z=90 mm, r=8 mm
target2 final:               x=299 mm, z=90 mm, r=7.5 mm
elapsed optimizer time:       1080.08 s
case count:                  2
strong-confidence cases:      0
minimum radius margin abs:    0.000741
truth selected all cases:     false
```

Per-case confidence:

```text
noise10_seed34:                 best=(299, 90, 7.5), moderate, radius margin=0.000741
source_mismatch_noise10_seed34: best=(299, 90, 7.5), moderate, radius margin=0.000975
```

Resource guard:

```text
return code:                  0
aborted:                      false
sample count:                 218
max observed GPU utilization: 84%
max observed RAM use:         14.55%
RAM cap:                      80%
GPU utilization cap:          90%
```

## Aggregate Result

The three close50 Tx/Rx45 matched seeds produce six confidence rows because
each seed has a nominal and a source-mismatch case.

```text
aggregate output:             outputs/experiments/1355_coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
row count:                    6
truth geometry rows:          0
confidence label counts:      moderate=4, strong=2
fallback warnings:            0
minimum radius margin abs:    0.000733
mean radius margin abs:       0.000906
maximum radius margin abs:    0.001110
maximum ambiguity x width:    0.0 mm
maximum ambiguity z width:    0.0 mm
maximum ambiguity radius width: 0.0 mm
x-ambiguity rows:             0
```

All six rows select the same near-truth wrong branch:

```text
truth target2:        x=300 mm, z=90 mm, r=8 mm
selected target2:     x=299 mm, z=90 mm, r=7.5 mm
selected error:       x error=1.0 mm, radius error=0.5 mm
```

Queue refresh:

```text
queue status:                 complete_ready_for_aggregation
existing seed probes:         6
missing seed probes:          0
estimated remaining runtime:  0.00 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

The reciprocal close50 source3 Tx/Rx45 matched family is now complete and
replicated. Moving close50 source3 from Tx/Rx `40 mm` to `45 mm` does not
rescue the exact target2 geometry. Seeds `13`, `21`, and `34` all select
`x=299 mm`, `z=90 mm`, `r=7.5 mm` in both nominal and source-mismatch cases.

Together with experiment `859`, the matched-control result is sharper than the
previous confounded comparison:

```text
close14 source3 Tx/Rx40: 6/6 truth rows, strong=6
close50 source3 Tx/Rx45: 0/6 truth rows, moderate=4, strong=2
```

This supports a guarded acquisition/geometry-aware source-density contrast. It
does not justify a simple spacing-only causal claim, because the close14 and
close50 families still differ in absolute target2 position and the close50
result is a stable near-truth wrong branch rather than an ambiguous truth
selection. The next synthetic decision should be a synthesis/manuscript policy
step before launching any new GPU branch.

## Validation

Figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.0423, dynamic range=255

coordinate_confidence_margins.png: 1802x665,
nonwhite=0.4176, dynamic range=238

coordinate_radius_decision_panel.png: 2126x1583,
nonwhite=0.2155, dynamic range=241

coordinate_confidence_aggregate.png: 1719x971,
nonwhite=0.2490, dynamic range=255
```
