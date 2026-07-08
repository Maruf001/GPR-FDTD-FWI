# Grid-Aware Payload BEM Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the BEM marathon block that turned the positive
run `091` grid-aware replay into executable homogeneous and layered payload
artifacts.

No field FWI, heavy GPU work, 3D/HPC work, neural-network training, or
historical `outputs/experiments` promotion was launched.

## New BEM Runs

```text
092_project_core_run089_grid_aware_adapter_contract
093_project_core_run089_grid_aware_adapter_smoke
094_project_core_run089_grid_aware_adapter_fresh_case_stress
095_project_core_grid_aware_layered_smoke_design_contract
096_project_core_grid_aware_layered_payload_smoke
097_project_core_grid_aware_layered_payload_stress_replay
098_project_core_grid_aware_payload_replacement_contract_refresh
```

Each result-driven output includes a `scripts/` folder with frozen generator
and test snapshots plus a SHA-256 manifest.

## Key Results

```text
continuous analytic-cylinder bridge L2:      1.5075838091082052
best alignment replay L2:                    1.0629842444792676
run-091 grid-aware replay L2:                0.5800814918790829
run-093 homogeneous payload smoke L2:        0.5800814918790826
run-094 homogeneous fresh-case worst L2:     0.6662947067388982
run-096 layered payload leave-one L2:        0.6497571611891657
run-097 layered payload stress worst L2:     0.6497571611891657
run-098 replacement contract rows:           8
```

The current BEM replacement boundary is now:

```text
homogeneous project-core cases:
  grid-aware target-cell payload

layered project-core cases:
  grid-aware target-cell payload with scalar Sommerfeld field provider
```

## Still Blocked

```text
measured-field claim:                 blocked
historical outputs/experiments promo: blocked
3D validation:                        blocked
GPU/FWI escalation:                   blocked
field transfer:                       blocked
```

## Presentation Refresh

The presentation evidence pack was refreshed:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
claim count:               43
ready-scoped claims:       36
blocked claims:            7
GPU/FWI/field launch:      false
```

The storyboard was refreshed:

```text
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
slides:                    8
ready claims referenced:   36
blocked claims preserved:  7
GPU/FWI/3D launch:         false
```

## Validation

Focused checks:

```text
17 passed
```

Full suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1138 passed in 30.23s
```

Whitespace check:

```text
git diff --check
pass
```

Resource check after focused validation:

```text
RAM used: 17 GiB / 119 GiB
GPU utilization: 6%
```

## Decision

Use runs `093`-`098` as the current local BEM payload evidence for
presentation and planning. Keep field, historical archive, 3D, GPU, and FWI
claims blocked until separate matched gates exist.

The marathon remains active; a clean checkpoint is not a stop condition.
