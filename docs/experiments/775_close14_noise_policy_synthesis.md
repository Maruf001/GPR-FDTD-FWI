# Experiment 775: Close14 Noise Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only synthesis of the archived close14 acquisition/noise branch. This run
summarizes existing aggregate outputs and the existing Tx/Rx50 scalar
noise-boundary summary. It does not run FDTD, FWI, optimizer, or GPU kernels.

## Output

```text
outputs/experiments/1243_close14_noise_policy_synthesis
```

Artifacts:

```text
data/close14_noise_policy_rows.csv
data/close14_noise_policy_by_txrx.csv
data/close14_noise_policy_summary.json
data/figure_validation.csv
figures/close14_noise_policy_synthesis.png
run_manifest.json
```

## Inputs

The synthesis reads 17 close14 aggregate artifacts:

```text
Tx/Rx45: runs 335, 341, 349, 356
Tx/Rx50: runs 360, 364, 368, 372, 376, 381, 385, 390, 394, 399, 403, 408, 412
boundary: run 418
```

## Result

Tx/Rx policy:

| Tx/Rx | Aggregates | Seed-replicated aggregates | Max seed-replicated clean noise | Minimum replicated clean margin |
| ---: | ---: | ---: | ---: | ---: |
| 45 mm | 4 | 3 | 15.3125% RMS | 2.401827e-3 |
| 50 mm | 13 | 13 | 19.642333984375% RMS | 1.977030e-3 |

Important correction: the Tx/Rx45 run at 15.361328125% RMS is seed34-only and
source-count mixed (`4,5,7` sources), not a seed-replicated clean result. The
replicated Tx/Rx45 claim should therefore stop at 15.3125% RMS.

Tx/Rx50 boundary from run 418:

```text
seed-replicated clean aggregate:       19.642333984375% RMS
single-seed clean maximum:             19.642333984375% RMS
single-seed ambiguous upper point:     19.642372131347656% RMS
bracket width:                         3.814697265625e-05% RMS
ambiguous upper experiment:            417
ambiguous upper margin to cutoff:     -7.419559550081445e-10
```

## Interpretation

The close14 branch already has a strong archived noise-boundary statement:

```text
For close14 at Tx/Rx50 with 4 sources, the archived evidence is seed-replicated
clean through 19.642333984375% RMS. The scalar seed34 boundary becomes
point-correct but x-ambiguous by 19.642372131347656% RMS.
```

This is more useful than running new close14 GPU probes immediately. The next
GPU work should only happen if the paper needs either a new spacing below
close14, a new acquisition offset, or a replicated boundary above 19.642333984375%
RMS.

## Validation

```text
tests/test_close14_noise_policy_synthesis.py: 4 passed
close14_noise_policy_synthesis.png: nonwhite=0.2255, dynamic range=255
```
