# BEM Experiment 234: Half-Space Finite-Rebar Claim Boundary Audit

Date: 2026-06-28

## Purpose

Define the claim boundary for the guarded scalar finite-rebar half-space
coupling package from runs `231`-`233`.

Runs `231`-`233` created, validated, and stress-tested a scalar finite-rebar
coupling proxy. This run converts that package into explicit supported and
blocked claims so the next branch does not overstate what the proxy proves.

This is a CPU-only audit. It does not implement full 3D Maxwell BEM, compare
against FDTD returns, run inversion, launch GPU/HPC work, run field FWI, or
promote field transfer.

## Output

```text
outputs/bem_experiments/234_project_core_bem_halfspace_finite_rebar_claim_boundary_audit
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_claim_boundary_rows.csv
data/project_core_bem_halfspace_finite_rebar_claim_boundary_next_stages.csv
data/project_core_bem_halfspace_finite_rebar_claim_boundary_summary.json
figures/project_core_bem_halfspace_finite_rebar_claim_boundary_audit.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_CLAIM_BOUNDARY_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
claim rows:                         13
supported claims:                   6
blocked claims:                     7
unexpected claim failures:          0
claim boundary ready:               true
surface samples:                    13
target points:                      31
frequencies:                        9
one-candidate kernel floor:         3627
1000-candidate kernel floor:        3627000
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

Supported by the current package:

| Supported item | Evidence |
| --- | --- |
| Bounded scalar surface sampling | `grid_15mm_only` with `outer_shell_11mm_binary`, 13 samples |
| Scalar half-space kernel smoke shape | 13 surface samples, 31 targets, 9 frequencies |
| Homogeneous-limit recovery | relative L2 `1.3693101062433268e-16` |
| Single-interface sanity trend | normal-incidence transmission decreases with larger lower-half-space permittivity |
| Scalar finite-rebar coupling proxy | centered peak at `x=0.13 m`, finite nonzero response, residual `1.4210854715202004e-14` |
| Negative-control guard | 25 scenarios, zero unexpected outcomes |

Still blocked:

| Blocked item | Reason |
| --- | --- |
| Full 3D Maxwell BEM | Current package is scalar and proxy-based |
| Real BEM/FDTD comparison | Comparison contract has not been written or executed |
| Inversion-scale half-space BEM | Current result is forward-model smoke evidence only |
| Field transfer | Measured field provenance and real comparison gates remain separate |
| GPU/HPC escalation | No decision-changing GPU/HPC question is open from this package |
| Field FWI | No validated field-forward/inversion connection exists |
| Broadband antenna and time-domain reconstruction | Current package uses frequency-domain scalar smoke quantities |

## Interpretation

The current BEM evidence supports a guarded scalar half-space finite-rebar
coupling package. It combines a bounded surface-sampling support, scalar
half-space kernel smoke, homogeneous-limit and interface sanity checks, centered
finite-rebar proxy response, and negative-control sensitivity.

It does not support full 3D Maxwell BEM, real BEM/FDTD agreement, inversion,
field transfer, GPU/HPC escalation, or field FWI.

## Decision

Use run `234` as the claim boundary for runs `231`-`233`. The next BEM task can
write a real BEM/FDTD comparison contract from this boundary, while keeping real
comparison, 3D validation, inversion, field transfer, GPU/HPC, and field FWI
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_claim_boundary_audit.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_claim_boundary_audit.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_claim_boundary_audit.py: pass
```

Figure check:

```text
2932x843, dynamic range=255
```
