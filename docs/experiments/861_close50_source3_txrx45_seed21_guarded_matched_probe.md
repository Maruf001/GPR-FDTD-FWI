# Experiment 861: Close50 Source3 Tx/Rx45 Seed21 Guarded Matched Probe

Date: 2026-06-19

## Purpose

Run the second reciprocal close50 source3 Tx/Rx45 matched-control seed from
experiment `856`. This follows experiment `860`, which found a near-truth but
wrong branch for seed `13`.

This is a single bounded synthetic 2D GPU run. It is not a broad GPU queue,
field work, detector-seeded FWI, 3D/HPC work, or neural-network training.

## Output

Optimizer run:

```text
outputs/experiments/1353_coordinate_optimizer_close50_seed21_sources3_txrx45_objectives
```

Resource guard:

```text
outputs/resource_guards/1353_close50_seed21_sources3_txrx45_monitor.jsonl
outputs/resource_guards/1353_close50_seed21_sources3_txrx45_guard_summary.json
```

Refreshed queue endpoint:

```text
outputs/summary_tables/119_close_spacing_matched_source3_probe_queue
```

## Result

Optimizer result:

```text
run name:                    coordinate_optimizer_close50_seed21_sources3_txrx45_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                45 mm
target2 truth:               x=300 mm, z=90 mm, r=8 mm
target2 final:               x=299 mm, z=90 mm, r=7.5 mm
elapsed optimizer time:       1153.98 s
case count:                  2
strong-confidence cases:      1
minimum radius margin abs:    0.000733
truth selected all cases:     false
```

Per-case confidence:

```text
noise10_seed21:                 best=(299, 90, 7.5), moderate, radius margin=0.000733
source_mismatch_noise10_seed21: best=(299, 90, 7.5), strong,   radius margin=0.001110
```

Resource guard result:

```text
return code:                  0
aborted:                      false
sample count:                 233
max observed GPU utilization: 84%
max observed RAM use:         14.77%
RAM cap:                      80%
GPU utilization cap:          90%
```

Queue refresh:

```text
queue status:                 partially_complete_ready_skip_existing
existing seed probes:         5
missing seed probes:          1
missing probes:               close50 Tx/Rx45 seed34
estimated remaining runtime:  23.86 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

Seed `21` repeats seed `13`: both cases select `x=299 mm` and `r=7.5 mm`
instead of the truth `x=300 mm` and `r=8 mm`. The reciprocal close50 Tx/Rx45
family is therefore trending toward a replicated near-truth wrong-branch
result, but seed `34` is still required before aggregation.

## Validation

Figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.1787, dynamic range=255

coordinate_confidence_margins.png: 1804x665,
nonwhite=0.3973, dynamic range=238

coordinate_radius_decision_panel.png: 2126x1583,
nonwhite=0.2221, dynamic range=238
```
