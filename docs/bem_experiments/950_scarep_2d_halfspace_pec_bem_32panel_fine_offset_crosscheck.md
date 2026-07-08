# BEM Experiment 950: Half-Space PEC BEM 32-Panel Fine Offset Cross-Check

Date: 2026-07-02

## Purpose

Run a selected higher-resolution cross-check for the fine source/receiver
tolerance result from runs `947-949`.

The guarded 16-panel fine sweep showed that a `+/-5` mm Tx/Rx offset
perturbation is measurable. This run checks whether that fine offset signal
survives when the target boundary is increased from 16 panels to 32 panels for
the three baseline-height offset cases.

This is a CPU-only BEM resolution cross-check. It does not run project-core
FDTD, field FWI, 3D/HPC work, GPU kernels, or neural-network training.

## Output

```text
outputs/bem_experiments/950_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_case_rows.csv
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_summary.json
data/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck_arrays.npz
figures/scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck.png
scripts/
```

## Setup

```text
source guarded block:           runs 947-949
target depth:                   0.35 m
lower half-space epsr:          6
reference panels:               32
scan positions:                 9
frequencies:                    41
time samples:                   2048
antenna z:                      0.000 m
tested Tx/Rx offsets:           0.055, 0.060, 0.065 m
baseline Tx/Rx offset:          0.060 m
```

## Result

```text
case count:                                      3
total BEM solve wall time:                       113.66555803199299 s
total wall time:                                 113.81222130497918 s
16-panel peak offset span at z=0:                0.6390875516677119 dB
32-panel peak offset span at z=0:                0.6390885783938787 dB
32/16 peak span ratio:                           1.000001606550095
16-panel max relative L2 across offset at z=0:   0.16690749402586136
32-panel max relative L2 across offset at z=0:   0.16690711298912922
32/16 relative L2 ratio:                         0.9999977170783472
32-panel time offset span at z=0:                0.029311187103077785 ns
project-core FDTD matched:                       false
field transfer ready:                            false
real 3D validation ready:                        false
gpu priority:                                    none
```

## Interpretation

The selected 32-panel cross-check preserves the fine offset signal almost
exactly. The 32-panel peak-amplitude span is `1.000001606550095x` the
16-panel value, and the 32-panel relative-L2 offset metric is
`0.9999977170783472x` the 16-panel value.

This is a useful resolution check: the fine Tx/Rx offset sensitivity observed
in the 16-panel run is not an artifact of the lower panel count for these
three selected cases. The result strengthens the geometry-control requirement
before matched BEM/FDTD comparison.

## Decision

Use run `950` as a selected 32-panel resolution cross-check for the guarded
fine-tolerance block. It supports keeping the 16-panel setting for preliminary
fine geometry sweeps while using selected 32-panel checks for final comparison
points.

Do not promote this result to project-core FDTD matching, field transfer, GPU
escalation, or 3D validation.

## Validation

Focused test:

```text
tests/test_scarep_2d_halfspace_pec_bem_32panel_fine_offset_crosscheck.py
3 passed
```

Figure validation:

```text
2410x845, dynamic range=255
```
