# BEM Experiment 948: Half-Space PEC 16-Panel Source/Receiver Fine Tolerance Sweep Validator

Date: 2026-07-02

## Purpose

Validate the saved fine source/receiver tolerance sweep from run `947`.

This validator checks that the run is the intended 9-case `+/-5` mm geometry
grid, that the saved summary metrics are recomputable from the saved case
rows, and that the result remains a BEM-only tolerance-scale result.

## Output

```text
outputs/bem_experiments/948_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator_validation_rows.csv
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator_summary.json
figures/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator.png
scripts/
```

## Result

```text
validation checks:                             6
passed checks:                                 6
failed checks:                                 0
case count:                                    9
tested Tx/Rx offsets:                          0.055, 0.060, 0.065 m
tested antenna z values:                       -0.005, 0.000, 0.005 m
preliminary panels:                            16
peak offset span at antenna z=0:               0.6390875516677119 dB
peak antenna-z span at offset=0.060 m:         0.03372223150313066 dB
max relative L2 across offset at z=0:          0.16690749402586136
max relative L2 across antenna z at offset:    0.0708135992362416
max relative L2 across full fine grid:         0.18412007156743118
project-core FDTD matched:                     false
field transfer ready:                          false
real 3D validation ready:                      false
gpu priority:                                  none
```

The six checks cover:

| Order | Check |
| ---: | --- |
| 1 | sweep identity and readiness |
| 2 | fine-grid shape and 16-panel policy |
| 3 | baseline and metric consistency |
| 4 | fine-geometry signal boundary |
| 5 | downstream scope remains blocked |
| 6 | figure and script snapshots are valid |

## Interpretation

The run `947` tolerance result is internally consistent. The saved rows
reproduce the peak-amplitude, timing, and relative-L2 metrics, and all
downstream promotion flags remain closed.

The validated result supports the current geometry-control decision: even
small Tx/Rx spacing changes are measurable in the saved 16-panel BEM response,
so matched BEM/FDTD comparison should keep source/receiver geometry explicit
before interpreting residuals as depth or material disagreement.

## Decision

Use runs `947-948` as the guarded fine-tolerance BEM geometry block. The next
useful BEM step is a selected higher-resolution check of the same tolerance
scale, not field transfer or 3D escalation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator.py
7 passed
```

Figure validation:

```text
2681x862, dynamic range=255
```
