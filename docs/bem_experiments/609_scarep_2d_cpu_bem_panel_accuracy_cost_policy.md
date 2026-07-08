# BEM Experiment 609: scarep 2D CPU BEM Panel Accuracy-Cost Policy

Date: 2026-06-30

## Purpose

Turn the 8-128 panel convergence ladder from runs `607-608` into a practical
accuracy/cost policy.

This run compares only against the `scarep` analytic dielectric-cylinder
reference. It does not compare against `outputs/experiments`, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/609_scarep_2d_cpu_bem_panel_accuracy_cost_policy
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_rows.csv
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_summary.json
figures/scarep_2d_cpu_bem_panel_accuracy_cost_policy.png
scripts/script_snapshot_manifest.json
```

## Result

```text
panel values:                       [8, 16, 32, 64, 128]
thresholds tested:                  6
thresholds met:                     5
thresholds unmet:                   1
repeat-sweep default threshold:      0.001
repeat-sweep default panels:         64
repeat-sweep default wall seconds:   20.652381618972868
high-accuracy threshold:             0.0002
high-accuracy panels:                128
high-accuracy wall seconds:          79.30079158884473
strict threshold:                    0.0001
strict threshold met:                false
complex error order:                 1.9961624062950216
time-B-scan error order:             1.9918880456546393
wall-time cost exponent:             1.6952684551080672
policy ready:                        true
```

Threshold policy:

| Threshold | Met | Selected panels | Complex relative L2 | Time-B-scan relative L2 | Wall seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.01 | true | 32 | 0.0028625612719971973 | 0.0021161825095859987 | 5.942273576045409 |
| 0.005 | true | 32 | 0.0028625612719971973 | 0.0021161825095859987 | 5.942273576045409 |
| 0.001 | true | 64 | 0.0007053747139208214 | 0.0005202399688500149 | 20.652381618972868 |
| 0.0005 | true | 128 | 0.00017926490798156493 | 0.00013202484159666165 | 79.30079158884473 |
| 0.0002 | true | 128 | 0.00017926490798156493 | 0.00013202484159666165 | 79.30079158884473 |
| 0.0001 | false | n/a | 0.00017926490798156493 | 0.00013202484159666165 | 79.30079158884473 |

## Interpretation

The 64-panel solve is the practical repeat-sweep default for a `1e-3`
relative-L2 target. The 128-panel solve is justified for a tighter `2e-4`
validation endpoint, but it costs about `3.84x` the 64-panel wall time.

The current 8-128 panel ladder does not satisfy a `1e-4` target for both the
complex spectrum and reconstructed time B-scan.

## Decision

Use 64 panels for repeated 2D `scarep` CPU BEM sweeps unless a tighter
validation endpoint is needed. Use 128 panels for high-accuracy checks.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel_accuracy_cost_policy.py

3 passed
```

Figure validation:

```text
2284x846, dynamic range=255
```
