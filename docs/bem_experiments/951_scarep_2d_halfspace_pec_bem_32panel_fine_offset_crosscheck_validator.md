# BEM Experiment 951: Half-Space PEC BEM 32-Panel Fine Offset Cross-Check Validator

Date: 2026-07-02

## Purpose

Validate the selected 32-panel fine offset cross-check from run `950`.

The validator checks that the cross-check contains the intended three
baseline-height offset cases, uses 32 panels, reproduces the saved metrics from
the saved rows, agrees closely with the guarded 16-panel fine-tolerance result,
and does not promote FDTD, field, GPU, or 3D claims.

## Output

```text
outputs/bem_experiments/951_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator_validation_rows.csv
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator_summary.json
figures/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator.png
scripts/
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
case count:                              3
tested Tx/Rx offsets:                    0.055, 0.060, 0.065 m
reference panels:                        32
peak offset span at z=0:                 0.6390885783938787 dB
max relative L2 across offset at z=0:    0.16690711298912922
32/16 peak span ratio:                   1.000001606550095
32/16 relative L2 ratio:                 0.9999977170783472
project-core FDTD matched:               false
field transfer ready:                    false
real 3D validation ready:                false
gpu priority:                            none
```

The six checks cover:

| Order | Check |
| ---: | --- |
| 1 | cross-check identity and readiness |
| 2 | selected-grid shape and 32-panel policy |
| 3 | baseline and metric consistency |
| 4 | 32-panel/16-panel resolution agreement |
| 5 | downstream scope remains blocked |
| 6 | figure and script snapshots are valid |

## Interpretation

The selected 32-panel cross-check is internally consistent and agrees with the
16-panel fine offset signal to within about `0.001%` on both peak-span and
relative-L2 metrics. This supports the use of 16 panels for preliminary fine
source/receiver geometry sweeps, with selected 32-panel checks reserved for
final comparison points.

## Decision

Use runs `950-951` as the guarded selected 32-panel resolution cross-check for
the fine source/receiver offset signal. Do not promote this result to
project-core FDTD matching, field transfer, GPU escalation, or 3D validation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck.py
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_validator.py
7 passed
```

Figure validation:

```text
2591x859, dynamic range=255
```
