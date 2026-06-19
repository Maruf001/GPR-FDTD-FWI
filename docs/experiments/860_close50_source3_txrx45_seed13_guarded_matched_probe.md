# Experiment 860: Close50 Source3 Tx/Rx45 Seed13 Guarded Matched Probe

Date: 2026-06-19

## Purpose

Run the first reciprocal close50 source3 Tx/Rx45 matched-control seed from
experiment `856`. This tests whether the close50 source3 failure pattern at
Tx/Rx `40 mm` is rescued when Tx/Rx is moved to the close14 matched-control
offset of `45 mm`.

This is a single bounded synthetic 2D GPU run. It is not a broad GPU queue,
field work, detector-seeded FWI, 3D/HPC work, or neural-network training.

## Output

Optimizer run:

```text
outputs/experiments/1352_coordinate_optimizer_close50_seed13_sources3_txrx45_objectives
```

Resource guard:

```text
outputs/resource_guards/1352_close50_seed13_sources3_txrx45_monitor.jsonl
outputs/resource_guards/1352_close50_seed13_sources3_txrx45_guard_summary.json
```

Refreshed queue endpoint:

```text
outputs/summary_tables/118_close_spacing_matched_source3_probe_queue
```

## Result

Optimizer result:

```text
run name:                    coordinate_optimizer_close50_seed13_sources3_txrx45_objectives
backend:                     gpu-cpml
sources:                     3
Tx/Rx offset:                45 mm
target2 truth:               x=300 mm, z=90 mm, r=8 mm
target2 final:               x=299 mm, z=90 mm, r=7.5 mm
elapsed optimizer time:       1157.83 s
case count:                  2
strong-confidence cases:      1
minimum radius margin abs:    0.000774
truth selected all cases:     false
```

Per-case confidence:

```text
noise10_seed13:                 best=(299, 90, 7.5), moderate, radius margin=0.000774
source_mismatch_noise10_seed13: best=(299, 90, 7.5), strong,   radius margin=0.001100
```

Resource guard result:

```text
return code:                  0
aborted:                      false
sample count:                 234
max observed GPU utilization: 84%
max observed RAM use:         14.61%
RAM cap:                      80%
GPU utilization cap:          90%
```

Queue refresh:

```text
queue status:                 partially_complete_ready_skip_existing
existing seed probes:         4
missing seed probes:          2
missing probes:               close50 Tx/Rx45 seeds 21/34
estimated remaining runtime:  47.72 min
ready for spacing-only claim: false
ready for broad GPU queue:    false
```

## Interpretation

This first reciprocal close50 Tx/Rx45 seed is a near-truth but wrong-branch
result. Moving close50 source3 from Tx/Rx `40 mm` to `45 mm` does not rescue
seed `13` to the exact target2 geometry; both cases select `x=299 mm` and
`r=7.5 mm` instead of the truth `x=300 mm` and `r=8 mm`.

The result strengthens the matched-control contrast with the completed close14
Tx/Rx40 family, where all three seeds selected the exact target2 geometry. It
still cannot be generalized alone: close50 Tx/Rx45 seeds `21` and `34` remain
missing.

## Validation

Figure validation:

```text
close_spacing_matched_source3_probe_queue.png: 2314x852,
nonwhite=0.2100, dynamic range=255

coordinate_confidence_margins.png: 1804x665,
nonwhite=0.4063, dynamic range=238

coordinate_radius_decision_panel.png: 2126x1583,
nonwhite=0.2257, dynamic range=238
```
