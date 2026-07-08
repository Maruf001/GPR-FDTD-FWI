# BEM Experiment 618: scarep 2D CPU BEM 64-vs-128 Panel Repeatability Tradeoff Scorecard

Date: 2026-06-30

## Purpose

Convert the validated 64-panel and 128-panel repeatability audits into a
simple operational scorecard.

This run does not rerun BEM solves. It reads the guarded repeatability results
from runs `612-617` and summarizes when to use 64 panels versus 128 panels.
It compares only against the scarep analytic dielectric-cylinder reference. It
does not compare against project FDTD outputs, run 3D validation, launch
GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/618_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_rows.csv
data/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard_summary.json
figures/scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source 64-panel audit ready:              true
source 64-panel validation ready:         true
source 64-panel sensitivity ready:        true
source 128-panel audit ready:             true
source 128-panel validation ready:        true
source 128-panel sensitivity ready:       true
score rows:                                2
repeat default panels:                    64
high-accuracy panels:                    128
64-panel complex relative L2 mean:         0.0007053747139208214
128-panel complex relative L2 mean:        0.00017926490798156496
64-panel time-B-scan relative L2 mean:     0.0005202399688500149
128-panel time-B-scan relative L2 mean:    0.00013202484159666165
64-panel wall seconds mean:               20.594270388983812
128-panel wall seconds mean:              79.57735419630383
complex error reduction 64 to 128:         3.9348175940455667
time-B-scan error reduction 64 to 128:     3.9404703126958314
wall-time ratio 128 to 64:                 3.8640530930812176
64-panel repeat default confirmed:         true
128-panel high-accuracy endpoint confirmed:true
compared to project FDTD outputs:          false
real 3D validation ready:                  false
GPU/HPC ready:                             false
field FWI ready:                           false
scorecard ready:                           true
```

## Interpretation

The 128-panel endpoint reduces the analytic-cylinder error by about four times,
but it also costs about four times more wall time than the 64-panel setting.
Both settings are repeatable and hash-stable.

## Decision

Use 64 panels for repeated 2D scarep CPU BEM sweeps. Reserve 128 panels for
high-accuracy endpoint confirmation when the tighter error target is worth the
runtime.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_128_repeatability_tradeoff_scorecard.py

3 passed
```

Figure validation:

```text
2284x853, dynamic range=255
```
