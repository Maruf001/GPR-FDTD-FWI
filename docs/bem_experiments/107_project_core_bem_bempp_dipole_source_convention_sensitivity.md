# BEM Experiment 107: Bempp Dipole Source-Convention Sensitivity

Date: 2026-06-27

## Purpose

Check how much the local 3D Bempp finite-rebar response changes when the source
dipole orientation or source height changes.

Run `106` showed that the selected `6x16` surface mesh is stable enough for the
current homogeneous 3D Bempp prototype. This run asks the next comparison-design
question:

```text
Can future paired 3D FDTD data treat source convention as approximate, or must
source position and polarization be locked explicitly?
```

This is a homogeneous frequency-domain BEM sensitivity audit. It does not run
3D FDTD, use measured field data, launch GPU/HPC work, or validate a layered 3D
GPR forward model.

## Output

```text
outputs/bem_experiments/107_project_core_bem_bempp_dipole_source_convention_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_dipole_source_convention_variants.csv
data/project_core_bem_bempp_dipole_source_convention_frequency_summary.csv
data/project_core_bem_bempp_dipole_source_convention_receivers.csv
data/project_core_bem_bempp_dipole_source_convention_comparisons.csv
data/project_core_bem_bempp_dipole_source_convention_sensitivity_summary.json
figures/project_core_bem_bempp_dipole_source_convention_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_DIPOLE_SOURCE_CONVENTION_SENSITIVITY.md
scripts/run_project_core_bem_bempp_dipole_source_convention_sensitivity.py
scripts/test_project_core_bem_bempp_dipole_source_convention_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source variants:                    5
frequencies checked:                2
receiver rows:                      310
comparison rows:                    8
finite all responses:               true
Bempp return codes all zero:         true
orientation max relative L2:         6.800743917312345
orientation max shape L2:            0.05525229526464649
height max relative L2:              0.14058934457504094
height max shape L2:                 0.004583210184517906
source metadata critical:            true
source convention lock ready:        true
3D FDTD validation ready:            false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Comparisons to the baseline y-oriented source at `[-0.04, 0.0, 0.09] m`:

| Frequency GHz | Variant | Group | Relative L2 | Shape L2 | Peak ratio |
| ---: | --- | --- | ---: | ---: | ---: |
| 0.5 | x_oriented_z090 | orientation | 6.80074392 | 0.05525230 | 7.34635921 |
| 0.5 | z_oriented_z090 | orientation | 2.57164073 | 0.05439005 | 3.36791952 |
| 0.5 | y_low_z075 | height | 0.13807758 | 0.00022297 | 1.13780333 |
| 0.5 | y_high_z105 | height | 0.10827408 | 0.00006585 | 0.89164318 |
| 1.5 | x_oriented_z090 | orientation | 0.29274844 | 0.03400241 | 1.24292891 |
| 1.5 | z_oriented_z090 | orientation | 0.77657839 | 0.05103310 | 0.23704788 |
| 1.5 | y_low_z075 | height | 0.14058934 | 0.00458321 | 1.14618332 |
| 1.5 | y_high_z105 | height | 0.09205898 | 0.00375239 | 0.90422476 |

## Interpretation

The local 3D Bempp response is highly sensitive to the source convention.
Changing the dipole orientation is a large change, not a small perturbation.
At 0.5 GHz, the x-oriented source is 6.80 relative L2 from the y-oriented
baseline and the vertical source is 2.57 relative L2 from baseline.

Source height is also material. Moving the y-oriented source by 15 mm changes
the receiver-line amplitude by roughly 9% to 14% in this bounded test. The
height variants preserve line shape much better than the orientation variants,
but the amplitude shift is large enough to require explicit metadata.

## Decision

Lock the current BEM-side comparison convention to a y-oriented electric dipole
at `[-0.04, 0.0, 0.09] m` unless a later paired FDTD design deliberately changes
it.

Treat source orientation, source position, and source height as required
metadata for any future 3D BEM/FDTD comparison.

This does not validate 3D BEM against FDTD and does not promote the result to a
layered 3D GPR model, field FWI input, or GPU/HPC workflow.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_bempp_dipole_source_convention_sensitivity.py
sha256: 625bdbf74cb863cbf7ab1938573eac96e5711e60e33bf19e67bf1cbc6efa21b6

test_project_core_bem_bempp_dipole_source_convention_sensitivity.py
sha256: d219124eb88ffd804d3cd32eca700e9f903f080669e00fca56ab6cebec824ebe
```

Subsequent Bempp 3D comparison-design experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_dipole_source_convention_sensitivity.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_dipole_source_convention_sensitivity.png
2716x848, dynamic range=255
```
