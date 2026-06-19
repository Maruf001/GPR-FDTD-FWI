# Experiment 859: Close14 Source3 Tx/Rx40 Matched Three-Seed Aggregate

Date: 2026-06-19

## Purpose

Complete and aggregate the close14 source3 Tx/Rx40 matched-control family from
experiment `856`. This records the guarded seed `34` optimizer run and the
three-seed confidence aggregate across seeds `13`, `21`, and `34`.

This is a narrow synthetic 2D matched-control result. It is not a broad GPU
queue, field work, detector-seeded FWI, 3D/HPC work, or neural-network
training.

## Output

Seed34 optimizer run:

```text
outputs/experiments/1350_coordinate_optimizer_close14_seed34_sources3_txrx40_objectives
```

Seed34 resource guard:

```text
outputs/resource_guards/1350_close14_seed34_sources3_txrx40_monitor.jsonl
outputs/resource_guards/1350_close14_seed34_sources3_txrx40_guard_summary.json
```

Three-seed aggregate:

```text
outputs/experiments/1351_coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
```

Refreshed queue endpoint:

```text
outputs/summary_tables/117_close_spacing_matched_source3_probe_queue
```

## Seed34 Result

```text
run name:                    coordinate_optimizer_close14_seed34_sources3_txrx40_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                40 mm
target2 truth:               x=264 mm, z=90 mm, r=8 mm
target2 final:               x=264 mm, z=90 mm, r=8 mm
elapsed optimizer time:       1172.64 s
case count:                  2
strong-confidence cases:      2
minimum radius margin abs:    0.003307
maximum ambiguity x width:    2.0 mm
truth selected all cases:     true
```

Resource guard:

```text
return code:                  0
aborted:                      false
sample count:                 237
max observed GPU utilization: 84%
max observed RAM use:         14.80%
RAM cap:                      80%
GPU utilization cap:          90%
```

## Aggregate Result

The three close14 Tx/Rx40 matched seeds produce six confidence rows because
each seed has a nominal and a source-mismatch case.

```text
aggregate output:             outputs/experiments/1351_coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
row count:                    6
truth geometry rows:          6
confidence label counts:      strong=6
fallback warnings:            0
minimum radius margin abs:    0.003136
mean radius margin abs:       0.003478
maximum radius margin abs:    0.003864
maximum ambiguity x width:    2.0 mm
maximum ambiguity z width:    0.0 mm
maximum ambiguity radius width: 0.0 mm
x-ambiguity rows:             6
```

Queue refresh:

```text
queue status:                 partially_complete_ready_skip_existing
existing seed probes:         3
missing seed probes:          3
missing probes:               close50 Tx/Rx45 seeds 13/21/34
estimated remaining runtime:  71.57 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

The close14 source3 Tx/Rx40 matched family is now complete and internally
consistent: all three seeds select the exact target2 geometry in both nominal
and source-mismatch cases with strong radius confidence.

This is meaningful evidence against the idea that close14 fails merely when
Tx/Rx is moved from `45 mm` to `40 mm`. It also sharpens the source-density
comparison because close50 source3 Tx/Rx40 failure now has a matched close14
Tx/Rx40 contrast.

It still does not complete a spacing-only causal claim. The reciprocal
close50 Tx/Rx45 family remains missing, and the completed close14 family still
has near-best x competitors within `1-2 mm` even though radius and depth are
clean. Use this as a guarded matched-control result, not as proof that spacing
alone controls success/failure.

## Validation

Figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.2433, dynamic range=255

coordinate_confidence_aggregate.png: 1719x971,
nonwhite=0.2670, dynamic range=255

coordinate_confidence_margins.png: 1804x665,
nonwhite=0.4607, dynamic range=238
```
