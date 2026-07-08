# BEM Experiment 608: scarep 2D CPU BEM 128-Panel Convergence Rate Audit

Date: 2026-06-30

## Purpose

Recompute the `scarep` 2D CPU BEM convergence and runtime scaling after adding
the 128-panel endpoint from run `607`.

This run compares only against the `scarep` analytic dielectric-cylinder
reference. It does not compare against `outputs/experiments`, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/608_scarep_2d_cpu_bem_convergence_rate_panel128_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_convergence_rate_panel128_audit_rows.csv
data/scarep_2d_cpu_bem_convergence_rate_panel128_audit_doubling_rows.csv
data/scarep_2d_cpu_bem_convergence_rate_panel128_audit_summary.json
figures/scarep_2d_cpu_bem_convergence_rate_audit.png
docs/SCAREP_2D_CPU_BEM_CONVERGENCE_RATE_PANEL128_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
panel values:                    [8, 16, 32, 64, 128]
best panels:                     128
best complex relative L2:         0.00017926490798156493
best time-B-scan relative L2:     0.00013202484159666165
complex error order:              1.9961624062950216
time-B-scan error order:          1.9918880456546393
wall-time cost exponent:          1.6952684551080672
complex error R2:                 0.9998561371855837
time-B-scan error R2:             0.9997968671698853
wall-time R2:                     0.9956574936225762
panel128 convergence ready:       true
compared to project FDTD archive: false
```

Fitted rates:

| Metric | Type | Exponent | R2 |
| --- | --- | ---: | ---: |
| complex_spectrum_error | error | 1.9961624062950216 | 0.9998561371855837 |
| time_bscan_error | error | 1.9918880456546393 | 0.9997968671698853 |
| wall_seconds | cost | 1.6952684551080672 | 0.9956574936225762 |

Panel-doubling ratios:

| From panels | To panels | Complex error reduction | Time error reduction | Wall-time ratio |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 16 | 3.719345927775734 | 3.6579428766963193 | 2.5616209521579107 |
| 16 | 32 | 4.147185987306131 | 4.138606233381054 | 3.149124673701103 |
| 32 | 64 | 4.0582136210776065 | 4.067704590756066 | 3.475501650113702 |
| 64 | 128 | 3.9348175940455676 | 3.9404703126958314 | 3.839789185184963 |

## Interpretation

Adding the 128-panel endpoint preserves the nearly second-order error trend.
The complex-spectrum and time-B-scan fits both remain close to order `2.0`
with high log-fit R2.

The cost fit steepens relative to the earlier 8-64 panel audit, and the
64-to-128 step costs about `3.84x` more wall time. That makes 128 panels a good
high-accuracy validation endpoint, not the default setting for repeated sweeps.

## Decision

Use the 8-128 panel fit as the current `scarep` CPU BEM convergence summary.
Keep project FDTD comparison, 3D validation, GPU/HPC, field transfer, and field
FWI blocked until a matched setup is used.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_convergence_rate_panel128_audit.py

3 passed
```

Figure validation:

```text
scarep_2d_cpu_bem_convergence_rate_audit.png
2769x839, dynamic range=255
```

Script snapshots:

```text
run_scarep_2d_cpu_bem_convergence_rate_panel128_audit.py
run_scarep_2d_cpu_bem_convergence_rate_audit.py
tests/test_scarep_2d_cpu_bem_convergence_rate_panel128_audit.py
```
