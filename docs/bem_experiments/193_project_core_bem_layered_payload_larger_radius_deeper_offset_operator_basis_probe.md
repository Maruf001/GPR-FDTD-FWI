# BEM Experiment 193: Deeper-Offset Operator Basis Probe

Date: 2026-06-27

## Purpose

Test whether a richer layer-aware operator basis can repair the known deeper
`z_plus_2p5mm` 35 mm larger-radius BEM/FDTD near miss.

Run `192` showed that changing target rasterization does not close the gate.
This run fixes the target support to the best run `192` support
(`outer_shell_18mm_linear_radial`) and varies only the operator basis: optical
path terms, direct air/concrete terms, interface-reflected terms, and cardinal
image terms.

This is a CPU-only local project-core FDTD/BEM adapter run. It does not compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/193_project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe_summary.json
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_OPERATOR_BASIS_PROBE.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe.py
```

## Result

```text
variants checked:                  108
ready variants:                      0
source best support mode:            outer_shell_18mm_linear_radial
source best leave-one L2:            0.7525645647728268
best source z m:                     0.038
best lower index scale:              0.9
best basis set:                      layer_mix_cardinal
best component count:                8
best all-scan L2:                    0.6763874300267784
best leave-one L2:                   0.9606924830049194
best acceptance margin:             -0.21069248300491938
best vs source improvement:         -0.20812791823209253
operator-basis repair ready:         false
depth repair validation ready:       false
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

The best rows were:

| Rank | Source z m | Index scale | Basis | Field LOO L2 | Scattering LOO L2 | Ready |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 1 | 0.038 | 0.9 | layer_mix_cardinal | 1.2199650607442114 | 0.9606924830049194 | false |
| 2 | 0.036 | 0.9 | layer_mix_cardinal | 1.2221985646155504 | 0.9627862875089482 | false |
| 3 | 0.036 | 1.15 | layer_mix_cardinal | 1.2823261716369576 | 0.9919349834946877 | false |
| 4 | 0.038 | 1.15 | layer_mix_cardinal | 1.282610973851392 | 0.9976143705789308 | false |
| 5 | 0.036 | 1.1 | layer_mix_cardinal | 1.2678216625982797 | 1.003063053544568 | false |

## Interpretation

The tested low-order layer-aware operator basis does not repair the
deeper-offset failure. It is much worse than the run `192` Sommerfeld
transmitted-surface baseline. The best operator-basis row has leave-one L2
`0.9606924830049194`, compared with the previous best `0.7525645647728268`.

This rules out a simple low-order image or optical-path basis as the repair for
this particular failure. The next credible BEM repair should use either a true
layered Green function path or a denser tabulated FDTD field-surface model.

## Decision

Do not refresh the BEM shell-support contract from this operator-basis probe.
Keep the run `181` scoped local 2D BEM/FDTD contract and the run `188`
depth-boundary failure. Continue toward a true layered Green function or denser
tabulated field-surface branch. Keep field transfer, 3D validation, GPU/HPC,
field FWI, and synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_subcell_rasterization_repair.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe.py
8 passed
```

Figure validation:

```text
project_core_bem_layered_payload_larger_radius_deeper_offset_operator_basis_probe.png
2428x1097, dynamic range=255
```
