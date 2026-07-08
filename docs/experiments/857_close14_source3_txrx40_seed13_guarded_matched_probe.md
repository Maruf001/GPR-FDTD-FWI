# Experiment 857: Close14 Source3 Tx/Rx40 Seed13 Guarded Matched Probe

Date: 2026-06-19

## Purpose

Run the first priority-1 matched source3 control from experiment `856` under a
live resource guard. This tests close14 target2 with source count `3` and
Tx/Rx `40 mm`, matching the close50 Tx/Rx40 source3 failure family while
retaining the close14 target spacing.

This is a single bounded synthetic 2D GPU run. It is not a broad GPU queue,
field work, detector-seeded FWI, 3D/HPC work, or neural-network training.

## Output

Optimizer run:

```text
outputs/experiments/1348_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives
```

Resource guard:

```text
outputs/resource_guards/1348_close14_seed13_sources3_txrx40_monitor.jsonl
outputs/resource_guards/1348_close14_seed13_sources3_txrx40_guard_summary.json
```

Refreshed queue endpoint:

```text
outputs/summary_tables/115_close_spacing_matched_source3_probe_queue
```

## Result

Optimizer result:

```text
run name:                    coordinate_optimizer_close14_seed13_sources3_txrx40_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                40 mm
target2 truth:               x=264 mm, z=90 mm, r=8 mm
target2 final:               x=264 mm, z=90 mm, r=8 mm
elapsed optimizer time:       1177.50 s
case count:                  2
strong-confidence cases:      2
minimum radius margin abs:    0.003136
maximum ambiguity x width:    2.0 mm
truth selected all cases:     true
```

Resource guard result:

```text
return code:                  0
aborted:                      false
sample count:                 238
max observed GPU utilization: 83%
max observed RAM use:         14.85%
RAM cap:                      80%
GPU utilization cap:          90%
```

Queue refresh:

```text
queue status:                 partially_complete_ready_skip_existing
existing seed probes:         1
missing seed probes:          5
missing probes:               close14 Tx/Rx40 seeds 21/34;
                              close50 Tx/Rx45 seeds 13/21/34
estimated remaining runtime:  109.78 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

This first matched close14 Tx/Rx40 seed does not reproduce the close50 Tx/Rx40
source3 failure. Seed13 selects the exact close14 target2 branch in both the
nominal and source-mismatch cases with strong radius confidence.

This is meaningful evidence, but it is not enough for a paper-level
spacing-only causal claim. The matched family still needs seeds `21` and `34`,
and the reciprocal close50 Tx/Rx45 family still needs seeds `13`, `21`, and
`34`. Continue skip-existing and one seed at a time if this claim is needed.

## Validation

Focused guard/queue tests:

```text
tests/test_resource_guarded_command.py
tests/test_close_spacing_matched_source3_probe_queue.py
9 passed
```

Queue figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.3617, dynamic range=255
```
