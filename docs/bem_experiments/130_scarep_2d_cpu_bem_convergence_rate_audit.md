# BEM Experiment 130: scarep 2D CPU BEM Convergence Rate Audit

Date: 2026-06-27

## Purpose

Estimate convergence and runtime scaling from the run `129`
8/16/32/64-panel scarep CPU BEM validation.

This run compares only against the scarep analytic dielectric-cylinder
reference. It does not compare against `outputs/experiments`, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/130_scarep_2d_cpu_bem_convergence_rate_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_convergence_rate_rows.csv
data/scarep_2d_cpu_bem_convergence_doubling_rows.csv
data/scarep_2d_cpu_bem_convergence_rate_audit_summary.json
figures/scarep_2d_cpu_bem_convergence_rate_audit.png
docs/SCAREP_2D_CPU_BEM_CONVERGENCE_RATE_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
panel values:                    [8, 16, 32, 64]
best panels:                     64
best complex relative L2:         0.0007053747139208214
best time-B-scan relative L2:     0.0005202399688500149
complex error order:              1.9956212230756902
time-B-scan error order:          1.9882322328508204
wall-time cost exponent:          1.620278753154497
complex error R2:                 0.999712306748834
time-B-scan error R2:             0.9995990787212937
convergence rate ready:           true
compared to scarep analytic ref:  true
compared to project FDTD archive: false
```

Fitted rates:

| Metric | Type | Exponent | R2 |
| --- | --- | ---: | ---: |
| complex_spectrum_error | error | 1.9956212230756902 | 0.999712306748834 |
| time_bscan_error | error | 1.9882322328508204 | 0.9995990787212937 |
| wall_seconds | cost | 1.620278753154497 | 0.9961084848597935 |

Panel-doubling ratios:

| From panels | To panels | Complex error reduction | Time error reduction | Wall-time ratio |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 16 | 3.719345927775734 | 3.6579428766963193 | 2.560151280081724 |
| 16 | 32 | 4.147185987306131 | 4.138606233381054 | 3.2138406301415117 |
| 32 | 64 | 4.0582136210776065 | 4.067704590756066 | 3.479714468414636 |

## Interpretation

The panel sweep shows approximately second-order error reduction for both the
complex spectrum and reconstructed time B-scan. Over this small panel range,
CPU wall time grows with a fitted exponent of about `1.62`.

This strengthens the colleague-provided scarep CPU BEM method-validation
evidence, but it remains an analytic dielectric-cylinder validation rather
than a direct comparison to the project FDTD archive.

## Decision

Use this as quantitative convergence-rate evidence for the scarep 2D CPU BEM
path. Keep project FDTD comparison, 3D validation, GPU/HPC, and field FWI
blocked until a matched setup is used.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_convergence_rate_audit.py
5 passed
```

Figure validation:

```text
scarep_2d_cpu_bem_convergence_rate_audit.png
2769x839, dynamic range=255
```

Script snapshots:

```text
run_scarep_2d_cpu_bem_convergence_rate_audit.py
sha256=6cb5479512b57b2c57fafdb0ecf9a85c1b9e7a08874c294efeacd1e67f4de965

tests/test_scarep_2d_cpu_bem_convergence_rate_audit.py
sha256=797d90c4ecc859c95870de5758b61e5e5c3cad0046f545171a8e1fc05022508a
```
