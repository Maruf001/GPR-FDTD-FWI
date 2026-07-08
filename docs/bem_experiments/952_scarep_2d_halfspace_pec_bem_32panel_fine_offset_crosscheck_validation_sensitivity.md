# BEM Experiment 952: Half-Space PEC BEM 32-Panel Fine Offset Cross-Check Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `951` validator for the selected 32-panel fine offset
cross-check. The goal is to confirm that the exact saved 32-panel resolution
check passes, while damaged rows, damaged metrics, and premature downstream
promotion fail.

## Output

```text
outputs/bem_experiments/952_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validation_sensitivity_scenario_rows.csv
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validation_sensitivity_summary.json
figures/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                   true
scenario count:                           20
expected pass count:                      1
expected fail count:                      19
observed pass count:                      1
observed fail count:                      19
unexpected outcome count:                 0
damaged scenarios rejected:               19
case count:                               3
tested Tx/Rx offsets:                     0.055, 0.060, 0.065 m
reference panels:                         32
peak offset span at z=0:                  0.6390885783938787 dB
max relative L2 across offset at z=0:     0.16690711298912922
32/16 peak span ratio:                    1.000001606550095
32/16 relative L2 ratio:                  0.9999977170783472
project-core FDTD matched:                false
field transfer ready:                     false
real 3D validation ready:                 false
gpu priority:                             none
```

The exact validator state passes. The 19 damaged states fail as expected,
including missing rows, wrong offset/z values, wrong panel count,
scan/frequency/time-count damage, baseline metric damage, peak/L2 metric
damage, 32-panel/16-panel agreement damage, premature FDTD/field/3D/GPU
promotion, figure damage, and missing script snapshots.

## Interpretation

The selected 32-panel cross-check is now guarded against the main ways the
result could be accidentally over-accepted. Runs `950-952` support a narrow
resolution conclusion: the fine Tx/Rx offset signal survives a 32-panel
cross-check for the selected baseline-height cases.

## Decision

Use runs `950-952` as the guarded selected 32-panel fine-offset resolution
cross-check. This supports 16-panel preliminary sweeps plus selected 32-panel
final checks, while keeping matched FDTD, field transfer, GPU escalation, and
3D validation separate.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck.py
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator.py
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validation_sensitivity.py
10 passed
```

Figure validation:

```text
3311x889, dynamic range=255
```
