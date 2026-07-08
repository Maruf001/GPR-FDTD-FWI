# BEM Experiment 949: Half-Space PEC 16-Panel Source/Receiver Fine Tolerance Sweep Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `948` validator for the fine source/receiver tolerance
sweep. The goal is to make sure the validator accepts the exact saved result
but rejects damaged grids, damaged metrics, and premature downstream
promotion.

## Output

```text
outputs/bem_experiments/949_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validation_sensitivity_scenario_rows.csv
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validation_sensitivity_summary.json
figures/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                         true
scenario count:                                 25
expected pass count:                            1
expected fail count:                            24
observed pass count:                            1
observed fail count:                            24
unexpected outcome count:                       0
damaged scenarios rejected:                     24
case count:                                     9
tested Tx/Rx offsets:                           0.055, 0.060, 0.065 m
tested antenna z values:                        -0.005, 0.000, 0.005 m
preliminary panels:                             16
peak offset span at antenna z=0:                0.6390875516677119 dB
max relative L2 across full fine grid:          0.18412007156743118
project-core FDTD matched:                      false
field transfer ready:                           false
real 3D validation ready:                       false
gpu priority:                                   none
```

The exact saved result passes. The 24 damaged cases fail as expected,
including row removal, offset/z-value damage, baseline damage, panel-policy
damage, scan/frequency/time-count damage, baseline metric damage, peak/timing
metric damage, relative-L2 metric damage, premature FDTD/field/3D/GPU
promotion, figure damage, and missing script snapshots.

## Interpretation

The fine tolerance result is now guarded against the main failure modes that
could otherwise make a small geometry perturbation look accepted when the grid,
metrics, or downstream scope had drifted.

Runs `947-949` support a narrow but useful conclusion: even within a `+/-5` mm
local geometry window, Tx/Rx offset changes are visible in the saved 16-panel
BEM response. The result should guide geometry control and selected
higher-resolution checks, not direct field transfer or 3D escalation.

## Decision

Use runs `947-949` as the guarded fine source/receiver tolerance block. The
next BEM experiment should run selected higher-resolution checks on the
tolerance-scale cases.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_validation_sensitivity.py
10 passed
```

Figure validation:

```text
3617x878, dynamic range=255
```
