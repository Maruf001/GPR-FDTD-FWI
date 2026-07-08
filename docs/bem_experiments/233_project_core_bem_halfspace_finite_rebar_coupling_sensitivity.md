# BEM Experiment 233: Half-Space Finite-Rebar Coupling Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `232` scalar finite-rebar half-space coupling validator with
negative controls.

Run `232` confirmed that the finite-rebar coupling smoke from run `231` is
internally consistent. This run asks whether the validator rejects plausible
damage to the same inputs and decision flags.

This is a CPU-only sensitivity run. It does not implement full 3D Maxwell BEM,
compare against FDTD returns, run inversion, launch GPU/HPC work, run field FWI,
or promote field transfer.

## Output

```text
outputs/bem_experiments/233_project_core_bem_halfspace_finite_rebar_coupling_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_coupling_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_coupling_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_coupling_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_COUPLING_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
expected failure scenarios:        24
observed pass scenarios:           1
observed failure scenarios:        24
unexpected outcomes:               0
sensitivity ready:                 true
boundary-ready for next design:    true
inversion-scale half-space ready:  false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU ready:                         false
field FWI ready:                   false
```

The exact run `231` result passes. The damaged scenarios fail as expected for:

| Damage family | Validator response |
| --- | --- |
| Surface, target, and frequency shape drift | Rejected |
| Target-weight normalization or centering drift | Rejected |
| Missing, duplicated, or off-center peak response | Rejected |
| Nonfinite or zero scattered field state | Rejected |
| Excessive symmetry imbalance | Rejected |
| Excessive residual-accounting error | Rejected |
| Source guard or coupling-readiness drift | Rejected |
| False promotion to inversion, 3D, field, GPU, or field FWI readiness | Rejected |

## Interpretation

The finite-rebar coupling validator is guarded against the most important
internal failure modes. It accepts the exact coupling smoke and rejects
controlled damage to geometry shape, target weights, peak centering, field
validity, symmetry, residual accounting, source guards, and downstream promotion
flags.

This gives a defensible scalar coupling package for the current half-space BEM
track. It is still not a full 3D electromagnetic BEM result and not a
FDTD-validated result.

## Decision

Use runs `231`-`233` as the guarded scalar finite-rebar half-space coupling
package. The next useful BEM branch is to define the bounded claim and objective
boundary for this coupling layer: what it demonstrates, what it does not
demonstrate, and which comparison or 3D solver step is required next.

Do not launch inversion-scale half-space BEM, real BEM/FDTD comparison, 3D
validation, field transfer, GPU/HPC work, or field FWI from this scalar proxy
alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_coupling_sensitivity.py
7 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_coupling_sensitivity.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_coupling_sensitivity.py: pass
```

Figure check:

```text
3329x891, dynamic range=255
```
