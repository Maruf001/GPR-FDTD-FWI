# Experiment 824: Synthetic 2D Acquisition Tradeoff Map

Date: 2026-06-18

## Purpose

Synthesize the current acquisition-design evidence without launching new GPU
work. This combines the close-spacing resolution policy, archive Tx/Rx
acceptance table, archive source-count table, and current no-GPU next-question
matrix into a paper-facing tradeoff map.

## Output

```text
outputs/experiments/1311_synthetic_2d_acquisition_tradeoff_map_current
```

Artifacts:

```text
data/synthetic_2d_acquisition_tradeoff_rows.csv
data/synthetic_2d_acquisition_tradeoff_summary.json
data/figure_validation.csv
figures/synthetic_2d_acquisition_tradeoff_map.png
run_manifest.json
```

## Result

Policy label:

```text
synthetic_2d_acquisition_tradeoff_cpu_no_gpu
```

Summary:

```text
tradeoff rows:                         12
tight-spacing reference Tx/Rx:         45 mm
close14 minimum clean Tx/Rx:           45 mm
target1 source-density best setting:   target1 sources=5
target1 source-density status:         source_density_nonmonotonic
target2 archive best Tx/Rx setting:    target2 Tx/Rx=50 mm
nonmonotonic source-density targets:   3
conditional GPU candidates:            0
gpu priority:                          none_now
ready for manuscript acquisition table:true
```

## Interpretation

Existing evidence supports acquisition-specific wording, not a universal
acquisition law. Tx/Rx=45 mm is the current tight-spacing reference in the
close-spacing grid, Tx/Rx=35 mm supports mid-spacing branches, and archive
source-density effects are nonmonotonic across targets.

This does not justify a broad synthetic GPU sweep. Any future synthetic GPU
work should start from a new objective, geometry, acquisition hypothesis, or
narrow exception probe.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_acquisition_tradeoff_map.py
3 passed
```

Figure validation:

```text
synthetic_2d_acquisition_tradeoff_map.png: 2739x869,
nonwhite=0.4596, dynamic range=255
```
