# BEM Experiment 612: scarep 2D CPU BEM 64-Panel Repeatability Audit

Date: 2026-06-30

## Purpose

Test whether the 64-panel scarep 2D CPU BEM setting selected by run `609` is
repeatable when the same analytic-cylinder validation problem is solved three
times.

This is a real CPU BEM solve. It compares only against the scarep analytic
dielectric-cylinder reference. It does not compare against project FDTD
outputs, run 3D validation, launch GPU/HPC work, run field FWI, or train neural
networks.

## Output

```text
outputs/bem_experiments/612_scarep_2d_cpu_bem_panel64_repeatability_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_repeatability_audit_rows.csv
data/scarep_2d_cpu_bem_panel64_repeatability_audit_summary.json
figures/scarep_2d_cpu_bem_panel64_repeatability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source policy ready:                    true
source validation ready:                true
source sensitivity ready:               true
panels:                                 64
repeats:                                 3
scan positions:                         11
frequencies:                            25
complex relative L2 min:                 0.0007053747139208214
complex relative L2 max:                 0.0007053747139208214
complex relative L2 mean:                0.0007053747139208214
complex relative L2 std:                 0.0
time-B-scan relative L2 min:             0.0005202399688500149
time-B-scan relative L2 max:             0.0005202399688500149
time-B-scan relative L2 mean:            0.0005202399688500149
time-B-scan relative L2 std:             0.0
wall seconds min:                       20.57575093698688
wall seconds max:                       20.603669724892825
wall seconds mean:                      20.594270388983812
wall seconds std:                        0.013095726214485306
response hash unique count:              1
time-B-scan hash unique count:           1
all complex errors below 1e-3:           true
all time-B-scan errors below 1e-3:       true
panel64 repeatability ready:             true
compared to project FDTD outputs:        false
real 3D validation ready:                false
GPU/HPC ready:                           false
field FWI ready:                         false
```

## Interpretation

The 64-panel CPU BEM default is repeatable for this scarep analytic-cylinder
validation problem. All three repeated solves produced identical frequency
response hashes and identical reconstructed time-B-scan hashes. The numerical
errors are also identical and remain below the `1e-3` target used for the
repeat-sweep default.

The runtime is stable over the three repeats: about `20.59` seconds on average
with about `0.013` seconds standard deviation.

## Decision

Use 64 panels as the repeat-sweep default for scarep 2D CPU BEM studies. Keep
project-FDTD comparison, 3D validation, GPU/HPC, and field-FWI claims blocked
until matched comparisons are produced.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit.py

3 passed
```

Figure validation:

```text
2282x853, dynamic range=255
```
