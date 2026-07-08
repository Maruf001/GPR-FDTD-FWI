# BEM Experiment 947: Half-Space PEC 16-Panel Source/Receiver Fine Tolerance Sweep

Date: 2026-07-02

## Purpose

Refine the source/receiver geometry sensitivity result around the baseline
half-space PEC BEM case. Runs `941-943` showed that broad acquisition-geometry
changes dominate the previous depth/material perturbations. This run asks a
smaller tolerance question:

```text
Does a +/-5 mm source/receiver geometry perturbation still change the saved
16-panel BEM response enough to matter for matched BEM/FDTD comparison?
```

This is a CPU-only BEM screening run. It does not run project-core FDTD, field
FWI, 3D/HPC work, GPU kernels, or neural-network training.

## Output

```text
outputs/bem_experiments/947_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep
```

Key artifacts:

```text
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_case_rows.csv
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_summary.json
data/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep_arrays.npz
figures/scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep.png
scripts/
```

## Setup

The run uses the baseline half-space PEC case from the guarded
source/receiver-geometry block:

```text
target depth:                 0.35 m
lower half-space epsr:        6
panels:                       16
scan positions:               9
frequencies:                  41
time samples:                 2048
baseline Tx/Rx offset:        0.060 m
baseline antenna z:           0.000 m
tested Tx/Rx offsets:         0.055, 0.060, 0.065 m
tested antenna z values:      -0.005, 0.000, 0.005 m
```

## Result

```text
case count:                                   9
total BEM solve wall time:                    102.07082179305144 s
total wall time:                              102.26425944198854 s
peak offset span at antenna z=0:              0.6390875516677119 dB
peak antenna-z span at offset=0.060 m:        0.03372223150313066 dB
time offset span at antenna z=0:              0.029311187103077785 ns
time antenna-z span at offset=0.060 m:        0 ns
max relative L2 across offset at z=0:         0.16690749402586136
max relative L2 across antenna z at offset:   0.0708135992362416
max relative L2 across full fine grid:        0.18412007156743118
project-core FDTD matched:                    false
field transfer ready:                         false
real 3D validation ready:                     false
gpu priority:                                 none
```

## Interpretation

The fine tolerance sweep confirms that acquisition geometry remains material
at the millimeter scale tested here. A `+/-5` mm Tx/Rx offset perturbation
around the baseline produces a `0.6390875516677119` dB peak-amplitude span and
`0.16690749402586136` relative L2 change at antenna z `0`.

The tested antenna-z perturbation is smaller in peak amplitude
(`0.03372223150313066` dB at the baseline offset) but still visible in
waveform shape (`0.0708135992362416` relative L2). This supports the run
`944-946` acquisition-geometry lock policy: matched BEM/FDTD comparisons need
explicit Tx/Rx offset, antenna-z, coordinate convention, target/material case,
panel policy, and trace-shape metadata before residuals can be interpreted as
depth or material disagreement.

## Decision

Use run `947` as a preliminary tolerance-scale BEM result. Do not promote this
alone to a project-core FDTD match, field transfer, GPU escalation, or 3D
validation result. The next useful BEM branch is a selected higher-resolution
check of the same tolerance-scale cases.

## Validation

Focused test:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_fine_tolerance_sweep.py
3 passed
```

Figure validation:

```text
3040x866, dynamic range=255
```
