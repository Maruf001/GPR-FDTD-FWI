# BEM Experiment 699: 116-Panel Dense-Frequency Receiver-Grid Worst-Case Audit

Date: 2026-06-30

## Purpose

Check whether the 116-panel receiver-grid result from run `696` survives
denser frequency sampling on the same larger-radius controlling case.

Run `696` tested 9, 11, and 13 scan positions on the 25-frequency grid. This
run repeats the same 116-panel receiver-grid check on a 49-frequency grid. It
does not rerun the 128-panel endpoint.

This is CPU-only analytic-cylinder BEM validation. It does not compare against
project FDTD outputs, run 3D Maxwell BEM, launch GPU/HPC work, or promote field
transfer.

## Output

```text
outputs/bem_experiments/699_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_scan_rows.csv
data/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit_summary.json
figures/scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
target case:                               radius_75mm_baseline_eps
target relative L2:                        0.001
tested scan counts:                        9, 11, 13
tested panel count:                        116
scan-count rows:                           3
solve rows:                                3
frequency count:                           49
116-panel pass count:                      3 / 3
116-panel max high-band relative L2:       0.0007643703508458867
116-panel mean high-band relative L2:      0.000762905583718239
116-panel minimum margin to target:        0.00023562964915411328
dense-frequency receiver-grid ready:       true
project-FDTD comparison ready:             false
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

Per-scan dense-frequency high-band errors:

| Scan positions | 116-panel high-band L2 | Margin to 0.001 | Pass |
| ---: | ---: | ---: | --- |
| 9 | 0.0007612039408853491 | 0.0002387960591146509 | true |
| 11 | 0.0007631424594234813 | 0.0002368575405765187 | true |
| 13 | 0.0007643703508458867 | 0.00023562964915411328 | true |

## Interpretation

The 116-panel endpoint remains below the `0.001` aggregate high-band relative
L2 target for all three scan counts on the 49-frequency grid. The aggregate
margin is substantially wider than the 25-frequency receiver-grid check, which
is consistent with the earlier finding that the aggregate metric changes with
frequency-grid sampling.

This supports receiver-grid robustness for the guarded 116-panel analytic BEM
policy under the 49-frequency aggregate metric. It still does not supersede the
per-frequency diagnostic caution from run `684`, and it does not create a
project-FDTD, 3D, GPU/HPC, or field-transfer claim.

## Decision

Keep 116 panels as receiver-grid robust under dense-frequency sampling for this
analytic worst-case check. Preserve the analytic-only claim boundary.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_dense_frequency_receiver_grid_worst_case_audit.py
3 passed
```

Figure check:

```text
2464x853, dynamic range=255
```
