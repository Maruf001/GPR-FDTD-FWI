# BEM Experiment 231: Half-Space Finite-Rebar Coupling Smoke

Date: 2026-06-28

## Purpose

Couple the scalar half-space incident field from run `228` to a simple
finite-rebar scattering proxy.

This run checks whether the scalar half-space kernel can produce a stable
centered scattering response with symmetry and exact residual accounting:

```text
total = background + scattered
```

It does not implement full 3D Maxwell BEM, compare against FDTD returns,
launch GPU/HPC work, run field FWI, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/231_project_core_bem_halfspace_finite_rebar_coupling_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_coupling_scan_response.csv
data/project_core_bem_halfspace_finite_rebar_coupling_symmetry.csv
data/project_core_bem_halfspace_finite_rebar_coupling_residuals.csv
data/project_core_bem_halfspace_finite_rebar_coupling_weights.csv
data/project_core_bem_halfspace_finite_rebar_coupling_fields.npz
data/project_core_bem_halfspace_finite_rebar_coupling_smoke_summary.json
figures/project_core_bem_halfspace_finite_rebar_coupling_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_COUPLING_SMOKE.md
```

## Result

```text
source kernel smoke sensitivity ready:    true
surface samples:                          13
target points:                            31
frequency count:                          9
rebar weight sum:                         1.0
peak scan x:                              0.13
target center x:                          0.13
peak center error:                        0.0
scattered norm:                           861.5238734513172
background norm:                          79.84542089533166
total norm:                               851.7384636025118
scattered/background norm ratio:          10.78989707600988
max symmetry pair imbalance:              7.108390876697042e-16
max total-background-scattered residual:  1.4210854715202004e-14
all fields finite:                        true
scattered field nonzero:                  true
peak scan centered:                       true
coupling smoke ready:                     true
ready for coupling validator:             true
kernel validated for inversion:           false
inversion-scale half-space ready:         false
real BEM/FDTD comparison ready:           false
3D validation ready:                      false
field transfer ready:                     false
GPU work ready:                           false
field FWI ready:                          false
```

## Interpretation

The scalar finite-rebar half-space coupling smoke is numerically stable. The
scattered response is finite and nonzero, peaks at the target center, remains
symmetric around the target, and satisfies total-background-scattered residual
accounting to numerical precision.

This is a meaningful next step after the scalar half-space kernel smoke, but it
is still a proxy. It is not full 3D Maxwell BEM and it is not validated against
FDTD returns.

## Decision

Use run `231` as a scalar finite-rebar coupling smoke only. It can be validated
and stress-tested next, but inversion-scale half-space BEM, real BEM/FDTD
comparison, 3D validation, field transfer, GPU/HPC, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_coupling_smoke.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_coupling_smoke.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_coupling_smoke.py: pass
```

Figure check:

```text
project_core_bem_halfspace_finite_rebar_coupling_smoke.png
3076x863, dynamic range=255
```
