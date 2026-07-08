# BEM Experiment 878: Panel-116 Worst-Bin Receiver-Pair Symmetry Audit

Date: 2026-07-01

## Purpose

Check whether the worst remaining 116-panel high-band residual is a one-sided
receiver-amplitude artifact or a paired spatial-shape effect.

This run reads saved receiver residual rows from run `869` and the guarded
aperture-trim block from runs `872-874`. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/878_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_pair_rows.csv
data/scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_summary.json
figures/scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source spatial audit ready:             true
source aperture scorecard ready:        true
source validation ready:                true
source sensitivity ready:               true
receiver rows:                          13
receiver pairs:                         6
center scan order:                      7
frequency:                              2.3125 GHz
source complex relative L2:             0.0020304660813910734
center total energy fraction:           0.08141503241185702
symmetric pair energy fraction:         0.2888732114593446
antisymmetric pair energy fraction:     0.7111267885406554
antisymmetric-dominant pair count:      5
symmetric-dominant pair count:          1
maximum pair magnitude delta fraction:  0.05160289316381502
mean pair magnitude delta fraction:     0.022844479581813487
balanced pair magnitudes:               true
antisymmetric residual dominant:        true
one-sided amplitude artifact:           false
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

Mirrored receiver pairs have balanced residual magnitudes, but most paired
residual energy is antisymmetric. Five of six mirrored pairs are
antisymmetric-dominant, and the maximum pair magnitude difference is only about
5.2%.

This rules out a simple one-sided amplitude artifact. The remaining mismatch
looks more like a spatial-shape or phase-structure effect across the aperture.

## Decision

Keep this as diagnostic evidence only. Do not promote receiver-pair symmetry
correction, hard per-frequency acceptance, project-FDTD comparison, field
transfer, or 3D/HPC claims from this result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit.py
3 passed
```

Figure check:

```text
2464x854, dynamic range=255
```
