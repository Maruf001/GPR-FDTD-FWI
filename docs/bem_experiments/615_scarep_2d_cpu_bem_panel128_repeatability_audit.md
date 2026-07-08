# BEM Experiment 615: scarep 2D CPU BEM 128-Panel Repeatability Audit

Date: 2026-06-30

## Purpose

Test whether the 128-panel scarep 2D CPU BEM high-accuracy endpoint is
repeatable when the same analytic-cylinder validation problem is solved three
times.

This is a real CPU BEM solve. It compares only against the scarep analytic
dielectric-cylinder reference. It does not compare against project FDTD
outputs, run 3D validation, launch GPU/HPC work, run field FWI, or train neural
networks.

## Output

```text
outputs/bem_experiments/615_scarep_2d_cpu_bem_panel128_repeatability_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_repeatability_audit_rows.csv
data/scarep_2d_cpu_bem_panel128_repeatability_audit_summary.json
figures/scarep_2d_cpu_bem_panel128_repeatability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source 128-panel extension ready:        true
source convergence ready:                true
source policy ready:                     true
source validation ready:                 true
source sensitivity ready:                true
panels:                                  128
repeats:                                  3
scan positions:                          11
frequencies:                             25
complex relative L2 min:                  0.00017926490798156493
complex relative L2 max:                  0.00017926490798156493
complex relative L2 mean:                 0.00017926490798156496
complex relative L2 std:                  2.710505431213761e-20
time-B-scan relative L2 min:              0.00013202484159666165
time-B-scan relative L2 max:              0.00013202484159666165
time-B-scan relative L2 mean:             0.00013202484159666165
time-B-scan relative L2 std:              0.0
wall seconds min:                        79.55734377005138
wall seconds max:                        79.60170355485752
wall seconds mean:                       79.57735419630383
wall seconds std:                         0.018367859195669373
response hash unique count:               1
time-B-scan hash unique count:            1
all complex errors below 2e-4:            true
all time-B-scan errors below 2e-4:        true
panel128 repeatability ready:             true
compared to project FDTD outputs:         false
real 3D validation ready:                 false
GPU/HPC ready:                            false
field FWI ready:                          false
```

## Interpretation

The 128-panel CPU BEM endpoint is repeatable for this scarep analytic-cylinder
validation problem. All three repeated solves produced identical frequency
response hashes and identical reconstructed time-B-scan hashes. The errors are
also identical and remain below the tighter `2e-4` target used for the
high-accuracy endpoint.

The runtime is stable over the three repeats: about `79.58` seconds on average
with about `0.018` seconds standard deviation. This confirms the endpoint is
reliable, but it is much more expensive than the 64-panel repeat-sweep default.

## Decision

Use 128 panels as the high-accuracy 2D scarep CPU BEM endpoint when the tighter
error target matters. Keep 64 panels as the repeat-sweep default. Keep
project-FDTD comparison, 3D validation, GPU/HPC, and field-FWI claims blocked
until matched comparisons are produced.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit.py

3 passed
```

Figure validation:

```text
2282x853, dynamic range=255
```
