# BEM Experiment 696: 116-Panel Receiver-Grid Worst-Case Audit

Date: 2026-06-30

## Purpose

Test whether the guarded 116-panel analytic BEM policy survives changes in
receiver/scan count on the controlling material/geometry transfer case.

The target case is `radius_75mm_baseline_eps`, the larger-radius case that
sets the tightest 116-panel margin in the current analytic policy. This run
solves that case at 9, 11, and 13 scan positions for 116 and 128 panels.

This is CPU-only analytic-cylinder BEM validation. It does not compare against
project FDTD outputs, run 3D Maxwell BEM, launch GPU/HPC work, or promote field
transfer.

## Output

```text
outputs/bem_experiments/696_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_scan_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
target case:                               radius_75mm_baseline_eps
target relative L2:                        0.001
tested scan counts:                        9, 11, 13
tested panel counts:                       116, 128
scan-count rows:                           3
solve rows:                                6
frequency count:                           25
116-panel pass count:                      3 / 3
128-panel pass count:                      3 / 3
116-panel max high-band relative L2:       0.0009518291083452528
116-panel mean high-band relative L2:      0.0009503906606159754
128-panel max high-band relative L2:       0.0007799559785944232
116-panel receiver-grid transfer ready:    true
128-panel endpoint ready:                  true
project-FDTD comparison ready:             false
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

Per-scan high-band errors:

| Scan positions | 116-panel high-band L2 | 128-panel high-band L2 | 116 pass |
| ---: | ---: | ---: | --- |
| 9 | 0.0009487257978779168 | 0.0007774015935020926 | true |
| 11 | 0.0009506170756247567 | 0.0007789581648464677 | true |
| 13 | 0.0009518291083452528 | 0.0007799559785944232 | true |

## Interpretation

The 116-panel endpoint stays below the `0.001` high-band relative L2 target
when the receiver/scan count changes from 9 to 13 on the larger-radius
controlling case. The margin remains tight and narrows slightly as scan count
increases.

This supports 116 panels as a guarded analytic-cylinder endpoint for this
receiver-grid perturbation. It does not create a project-FDTD, 3D, GPU/HPC, or
field-transfer claim.

## Decision

Keep 116 panels as receiver-grid robust for this analytic worst-case check.
Preserve the existing claim boundary: analytic BEM only, with project-FDTD,
real 3D, GPU/HPC, field transfer, and field FWI still blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit.py
4 passed
```

Figure check:

```text
2500x853, dynamic range=255
```
