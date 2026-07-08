# BEM Experiment 194: Deeper-Offset Tabulated Surface Probe

Date: 2026-06-27

## Purpose

Test whether a direct tabulated FDTD field surface can repair the known deeper
`z_plus_2p5mm` 35 mm larger-radius BEM/FDTD near miss.

Runs `192` and `193` ruled out two simpler explanations: target rasterization
alone and low-order layer-aware operator-basis terms. This run keeps the best
run `192` target support (`outer_shell_18mm_linear_radial`) and replaces the
analytic/proxy surface with a direct tabulated background field surface.

This is a CPU-only local project-core FDTD/BEM adapter run. It does not compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/194_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe_summary.json
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_arrays.npz
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_TABULATED_SURFACE_PROBE.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.py
```

## Result

```text
surface policies:                   3
ready policies:                     2
Sommerfeld/radial baseline L2:      0.7525645647728268
operator-basis baseline L2:         0.9606924830049194
full surface sample count:          37
minimum ready sample count:         19
best surface policy:                dense_5mm_plus_exact
best surface sample count:          37
best leave-one L2:                  0.5654888528068279
best acceptance margin:             0.18451114719317208
best vs Sommerfeld improvement:     0.18707571196599893
tabulated-surface repair ready:     true
depth repair validation ready:      true
contract refresh ready:             false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

Policy results:

| Policy | Samples | Holdout extrapolated | Leave-one L2 | Ready |
| --- | ---: | ---: | ---: | --- |
| exact_source_receiver_only | 10 | 4 | 1.1118749417965836 | false |
| dense_10mm_plus_exact | 19 | 0 | 0.6131125861743153 | true |
| dense_5mm_plus_exact | 37 | 0 | 0.5654888528068279 | true |

## Interpretation

This is the first branch in the deeper-offset repair sequence that closes the
`0.75` leave-one gate. The failure is not repaired by shell thickness, radial
weights alone, target rasterization, or a low-order analytic operator basis.
It is repaired by directly tabulating the FDTD background field surface densely
enough to avoid held-out source/receiver extrapolation.

The result should be interpreted carefully. It is a practical tabulated-surface
repair candidate and an upper-bound diagnostic for the missing operator
information. It is not an analytic BEM repair, not a field-data result, and not
a 3D validation result.

## Decision

Treat run `194` as a candidate practical repair path. Validate it and add
negative-control sensitivity before any claim refresh. Do not refresh the
analytic shell-support contract from this single case. Keep field transfer, 3D
validation, GPU/HPC, field FWI, and synthetic `outputs/experiments` promotion
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.py
3 passed
```

Figure validation:

```text
project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.png
2608x833, dynamic range=255
```
