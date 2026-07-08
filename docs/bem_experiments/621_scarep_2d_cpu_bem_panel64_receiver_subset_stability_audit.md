# BEM Experiment 621: scarep 2D CPU BEM 64-Panel Receiver-Subset Stability Audit

Date: 2026-06-30

## Purpose

Test whether the validated 64-panel scarep CPU BEM default remains stable when
the receiver/scan line is cropped or thinned.

Runs `612-620` established that 64 panels are the repeat-sweep default and 128
panels are the high-accuracy endpoint for the analytic-cylinder validation
case. This run asks whether that 64-panel default still stays below the
`1e-3` relative-error target for practical scan subsets.

This is one real CPU BEM solve against the scarep analytic-cylinder reference.
It does not compare against project FDTD outputs, run 3D validation, launch
GPU/HPC work, transfer to field work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/621_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_subset_rows.csv
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_summary.json
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_arrays.npz
figures/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
panels:                              64
scan positions:                      11
frequencies:                         25
subset cases:                        10
minimum subset scan count:            3
full-scan complex relative L2:        0.0007053747139208214
full-scan time-B-scan relative L2:    0.0005202399688500149
worst subset complex relative L2:     0.0007704118971318319
worst subset time-B-scan relative L2: 0.0005678637768138664
complex subsets below 1e-3:           10
time-B-scan subsets below 1e-3:       10
wall seconds:                         20.819425830850378
stability ready:                      true
```

Subset outcomes:

| Subset | Scan count | Complex relative L2 | Time-B-scan relative L2 | Pass |
| --- | ---: | ---: | ---: | --- |
| full_11 | 11 | 0.0007053747139208214 | 0.0005202399688500149 | yes |
| center_9 | 9 | 0.0007252473952158805 | 0.0005349099351339755 | yes |
| center_7 | 7 | 0.0007435702839337277 | 0.0005483356823750578 | yes |
| center_5 | 5 | 0.000759086218785013 | 0.0005595933212456438 | yes |
| center_3 | 3 | 0.0007704118971318319 | 0.0005678637768138664 | yes |
| alternating_even_6 | 6 | 0.0006959713903660319 | 0.0005132749890318248 | yes |
| alternating_odd_5 | 5 | 0.0007164907988738678 | 0.0005284759345502413 | yes |
| left_9 | 9 | 0.0007245488595820476 | 0.0005343853794532517 | yes |
| right_9 | 9 | 0.0007163869729802666 | 0.0005282913683724522 | yes |
| every_third_4 | 4 | 0.0006978585132381554 | 0.0005145104737617585 | yes |

## Interpretation

The 64-panel CPU BEM default is not only repeatable on the full 11-position
scan; it also remains under the `1e-3` analytic-cylinder error target after
center cropping, one-sided cropping, alternating-position thinning, and sparse
every-third-position thinning.

The worst tested subset is the three-position center crop, and it still stays
below the threshold. This supports using 64 panels for receiver-line
sensitivity studies on the scarep 2D analytic-cylinder setup.

## Decision

Keep 64 panels as the default for repeated receiver-line and scan-subset BEM
studies on the scarep 2D analytic-cylinder problem. Keep project-FDTD
comparison, 3D validation, GPU/HPC work, field transfer, and field FWI blocked
until matched comparison evidence is produced.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit.py

4 passed
```

Figure validation:

```text
2356x870, dynamic range=255
```
