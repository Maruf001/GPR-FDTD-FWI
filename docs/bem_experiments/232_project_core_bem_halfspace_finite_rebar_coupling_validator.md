# BEM Experiment 232: Half-Space Finite-Rebar Coupling Validator

Date: 2026-06-28

## Purpose

Validate the scalar finite-rebar half-space coupling smoke from run `231` from
a downstream consumer perspective.

Run `231` showed that the scalar half-space incident field can be coupled to a
simple finite-rebar scattering proxy with a centered peak response, finite
nonzero fields, symmetry, and residual accounting. This run checks whether
those properties are strong enough to become a guarded intermediate result.

This is a CPU-only validator. It does not implement full 3D Maxwell BEM, compare
against FDTD returns, run inversion, launch GPU/HPC work, run field FWI, or
promote field transfer.

## Output

```text
outputs/bem_experiments/232_project_core_bem_halfspace_finite_rebar_coupling_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_coupling_validation_checks.csv
data/project_core_bem_halfspace_finite_rebar_coupling_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_coupling_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_COUPLING_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
validation passes:                  7
blocking failures:                  0
validation ready:                   true
source peak scan x:                 0.13 m
source scattered norm:              861.5238734513172
source max symmetry imbalance:      7.108390876697042e-16
source max residual:                1.4210854715202004e-14
inversion-scale half-space ready:   false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The seven checks confirm:

| Check | Outcome |
| --- | --- |
| Coupling shape matches the kernel contract | Pass |
| Rebar weights are normalized and centered | Pass |
| Scattered response peaks at the target center | Pass |
| Fields are finite and scattered response is nonzero | Pass |
| Symmetry and residual tolerances pass | Pass |
| Coupling smoke is ready but inversion remains blocked | Pass |
| Real comparison, field transfer, GPU, and field FWI remain blocked | Pass |

## Interpretation

The run `231` scalar finite-rebar coupling smoke is internally consistent. The
proxy has a centered rebar response, normalized target weights, finite nonzero
fields, symmetry at machine precision scale, and exact residual accounting
within numerical tolerance.

This still does not make the model a full 3D electromagnetic BEM solver. The
current result is a guarded scalar coupling step that can support sensitivity
testing and later comparison design.

## Decision

Use run `232` as the consumer validator for the finite-rebar coupling smoke.
The next BEM step is a negative-control sensitivity run that perturbs the shape,
weights, peak location, field validity, residuals, symmetry, and downstream
readiness flags. Do not promote inversion-scale half-space BEM, real BEM/FDTD
comparison, 3D validation, field transfer, GPU/HPC work, or field FWI from this
validator alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_coupling_validator.py
6 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_coupling_validator.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_coupling_validator.py: pass
```

Figure check:

```text
2465x840, dynamic range=255
```
