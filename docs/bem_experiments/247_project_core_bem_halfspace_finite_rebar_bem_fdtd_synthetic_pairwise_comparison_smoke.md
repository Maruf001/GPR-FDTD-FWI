# BEM Experiment 247: Half-Space Finite-Rebar BEM/FDTD Synthetic Pairwise Comparison Smoke

Date: 2026-06-28

## Purpose

Build the first end-to-end synthetic pairwise comparison between the BEM export
and FDTD-like frequency bins recovered by the synthetic extractor.

This run connects two already guarded pieces:

```text
run 238: BEM-side scalar frequency export
run 244: synthetic FDTD-side frequency extraction smoke
```

It does not run real FDTD, compare real paired FDTD files, implement full 3D
Maxwell BEM, launch GPU/HPC work, run field FWI, or promote inversion-scale
half-space BEM.

## Output

```text
outputs/bem_experiments/247_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_rows.csv
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_peak_rows.csv
data/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_FDTD_SYNTHETIC_PAIRWISE_COMPARISON_SMOKE.md
scripts/run_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke.py
scripts/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke.py
```

## Result

```text
source BEM exporter ready:                  true
source synthetic FDTD extractor ready:      true
BEM role keys:                              117
FDTD keys:                                  117
paired keys:                                117
frequency peak rows:                        9
missing BEM keys:                           0
missing FDTD keys:                          0
duplicate BEM role keys:                    0
duplicate FDTD keys:                        0
max background abs error:                   5.6676640744313346e-14
max scattered abs error:                    7.105427357601002e-13
max total abs error:                        6.793026388275575e-13
max scattered relative error:               2.1699084408491636e-13
normalized L2 error:                        2.459587752743292e-15
max peak x error:                           0.0 m
max peak index error:                       0
key completeness ready:                     true
receiver-frequency key match ready:         true
complex scattered residual ready:           true
scan peak location error ready:             true
synthetic pairwise comparison ready:        true
real FDTD frequency extraction ready:        false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

Every frequency has the same BEM and synthetic-FDTD peak receiver:

| Frequency range | Peak receiver | Peak x location | Peak error |
| --- | ---: | ---: | ---: |
| 0.375-2.999 GHz | 6 | 0.13 m | 0.0 m |

## Interpretation

The scalar comparison path now has a complete synthetic smoke test. The BEM
export and the synthetic FDTD-like extracted bins share all 117
receiver-frequency keys, have no duplicate or missing keys, and agree to near
machine precision on the complex scattered field.

This is a mechanics result, not a real BEM/FDTD agreement result. The FDTD-side
bins were generated from synthetic traces built from the BEM spectra, so this
only validates the comparison plumbing: key pairing, residual accounting,
normalized error reporting, and scan peak-location checks.

## Decision

Use run `247` as the synthetic pairwise comparison smoke for the scalar
half-space finite-rebar path. Real FDTD extraction, real BEM/FDTD comparison,
3D validation, inversion-scale use, field transfer, GPU/HPC readiness, and
field FWI remain blocked until real paired FDTD traces are available and pass
the same key, residual, and peak-location checks.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_bem_fdtd_synthetic_pairwise_comparison_smoke.png
2589x845, dynamic range=255
```
