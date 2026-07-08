# BEM Experiment 885: Panel-116 Worst-Bin Diagnostic Synthesis Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `884` diagnostic synthesis claim boundary.

The validator checks source readiness, diagnostic row stability, absence of a
physical target-passing repair, the nonphysical lower-bound condition, blocked
downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/885_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
diagnostic rows:                         7
worst frequency:                         2.3125 GHz
full relative L2:                        0.0020304660813910734
best physical candidate relative L2:     0.001195683569955468
nonphysical lower-bound relative L2:     0.0005793593752068725
physical candidate pass count:           0
nonphysical lower bound passes target:   true
source/receiver spatial phase required:  true
hard per-frequency endpoint ready:       false
correction promoted:                     false
project FDTD comparison ready:           false
field transfer ready:                    false
real 3D validation ready:                false
gpu priority:                            none
```

## Interpretation

The saved diagnostic synthesis is internally consistent and preserves the
claim boundary: no physical candidate reaches the target, while the only
passing row is a nonphysical lower bound.

## Decision

Use run `884` as a validated no-repair synthesis for the remaining 116-panel
worst high-band frequency bin.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_diagnostic_synthesis_claim_boundary_validator.py
3 passed
```

Figure check:

```text
2465x860, dynamic range=255
```

