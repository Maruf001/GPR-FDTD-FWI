# Experiment 858: Close14 Source3 Tx/Rx40 Seed21 Guarded Matched Probe

Date: 2026-06-19

## Purpose

Run the second priority-1 matched source3 control from experiment `856` under
the live resource guard. This extends experiment `857` from seed `13` to seed
`21` for the close14 target2 spacing at source count `3` and Tx/Rx `40 mm`.

This is a single bounded synthetic 2D GPU run. It is not a broad GPU queue,
field work, detector-seeded FWI, 3D/HPC work, or neural-network training.

## Output

Optimizer run:

```text
outputs/experiments/1349_coordinate_optimizer_close14_seed21_sources3_txrx40_objectives
```

Resource guard:

```text
outputs/resource_guards/1349_close14_seed21_sources3_txrx40_monitor.jsonl
outputs/resource_guards/1349_close14_seed21_sources3_txrx40_guard_summary.json
```

Refreshed queue endpoint:

```text
outputs/summary_tables/116_close_spacing_matched_source3_probe_queue
```

## Result

Optimizer result:

```text
run name:                    coordinate_optimizer_close14_seed21_sources3_txrx40_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                40 mm
target2 truth:               x=264 mm, z=90 mm, r=8 mm
target2 final:               x=264 mm, z=90 mm, r=8 mm
elapsed optimizer time:       1172.03 s
case count:                  2
strong-confidence cases:      2
minimum radius margin abs:    0.003490
maximum ambiguity x width:    2.0 mm
truth selected all cases:     true
```

Per-case confidence:

```text
noise10_seed21:                 best=(264, 90, 8), strong, radius margin=0.003490, ambiguity x=263-265 mm
source_mismatch_noise10_seed21: best=(264, 90, 8), strong, radius margin=0.003683, ambiguity x=264-265 mm
```

Resource guard result:

```text
return code:                  0
aborted:                      false
sample count:                 237
max observed GPU utilization: 84%
max observed RAM use:         14.68%
RAM cap:                      80%
GPU utilization cap:          90%
```

Queue refresh:

```text
queue status:                 partially_complete_ready_skip_existing
existing seed probes:         2
missing seed probes:          4
missing probes:               close14 Tx/Rx40 seed34;
                              close50 Tx/Rx45 seeds 13/21/34
estimated remaining runtime:  90.67 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

Seed `21` agrees with seed `13`: close14 target2 at source count `3` and
Tx/Rx `40 mm` selects the exact target2 branch in both nominal and
source-mismatch cases with strong radius confidence.

The close14 matched family is now two-thirds complete, but the matched control
is still not sufficient for a spacing-only causal claim. The remaining close14
seed `34` is needed before the close14 Tx/Rx40 family can be aggregated, and
the reciprocal close50 Tx/Rx45 family remains entirely missing.

## Validation

Resource guard:

```text
returncode=0, aborted=false, max_gpu_util_percent=84.0, max_ram_used_percent=14.6755
```

Queue figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.3026, dynamic range=255
```
