# BEM Experiment 095: Grid-Aware Layered Smoke Design Contract

Date: 2026-06-25

## Purpose

Connect the new run `093`/`094` grid-aware adapter payload path to the existing
layered-media evidence from runs `066` and `067`.

Run `094` showed that the reusable adapter survives three fresh homogeneous
cases. Run `066` showed that the scalar two-layer Sommerfeld proxy survives a
fresh layered stress ladder. Run `067` promoted that proxy as the active
layered 2D replacement candidate inside the tested project-core envelope.
This run turns those prerequisites into an explicit design contract for the
next executable layered payload smoke.

This is CPU-only contract synthesis. It does not rerun FDTD, use field data,
launch GPU kernels, run FWI, perform 3D/HPC work, train neural networks, or use
the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/095_project_core_grid_aware_layered_smoke_design_contract
```

Key artifacts:

```text
data/project_core_grid_aware_layered_smoke_design_contract_summary.json
data/project_core_grid_aware_layered_smoke_interface.csv
data/project_core_grid_aware_layered_smoke_gates.csv
figures/project_core_grid_aware_layered_smoke_design_contract.png
docs/PROJECT_CORE_GRID_AWARE_LAYERED_SMOKE_DESIGN_CONTRACT.md
scripts/run_project_core_grid_aware_layered_smoke_design_contract.py
scripts/test_project_core_grid_aware_layered_smoke_design_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
interface items:                    12
gates:                              5
homogeneous prerequisite L2:        0.6662947067388982
layered prerequisite L2:            0.6497571611891657
layered replacement contract ready: true
layered smoke design ready:         true
ready for layered payload smoke:    true
ready for half-space promotion:     false
ready for outputs/experiments promo: false
ready for field transfer:           false
ready for 3D validation:            false
ready for GPU work:                 false
```

The layered smoke interface extends the eight run `092`/`093` adapter items
with four layer-specific requirements:

```text
layer_interface_geometry
upper_lower_material_properties
layered_field_provider_policy
layered_leave_one_gate
```

Gate summary:

| Gate | Source run | Value | Status |
| --- | --- | ---: | --- |
| homogeneous fresh-case adapter | 094 | 0.6662947067388982 | pass |
| layered Sommerfeld stress | 066 | 0.6497571611891657 | pass |
| layered replacement contract | 067 | true | pass |
| layered payload smoke | 095 | - | blocked |
| field/3D/GPU/outputs promotion | - | - | blocked |

## Interpretation

The BEM track now has the prerequisites for a layered payload smoke: a saved
grid-aware adapter payload path and a passing scalar Sommerfeld layered proxy.
The missing artifact is an executable run that emits the actual layered
payload arrays and leave-one-scan gate table.

This run does not promote half-space, field transfer, 3D validation, GPU work,
FWI, or `outputs/experiments` claims.

## Decision

Proceed to a duplicated-script layered payload smoke. Keep promotion blocked
until that executable payload smoke passes.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_grid_aware_layered_smoke_design_contract.py
scripts/test_project_core_grid_aware_layered_smoke_design_contract.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_grid_aware_layered_smoke_design_contract.py
59c66ac2aebb57a05a39a0f59577ca509ef3d5de0b81d47828f73649fd2d181a

test_project_core_grid_aware_layered_smoke_design_contract.py
1a65f40156910b600808b30930a5960ec4181f991254756c62dacd2a429028c6
```

## Validation

Focused tests:

```text
tests/test_project_core_grid_aware_layered_smoke_design_contract.py
3 passed
```

Figure check:

```text
project_core_grid_aware_layered_smoke_design_contract.png  2206x772, dynamic range=255
```
