# BEM Experiment 098: Grid-Aware Payload Replacement Contract Refresh

Date: 2026-06-25

## Purpose

Refresh the BEM replacement contract around the run `093`-`097` grid-aware
payload artifacts.

Runs `093` and `094` established a homogeneous grid-aware target-cell payload
path. Runs `096` and `097` established a layered grid-aware payload path using
the scalar Sommerfeld field provider. This run records the updated claim
boundary.

This is CPU-only contract synthesis. It does not rerun FDTD, use field data,
launch GPU kernels, run FWI, perform 3D/HPC work, train neural networks, or use
the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/098_project_core_grid_aware_payload_replacement_contract_refresh
```

Key artifacts:

```text
data/project_core_grid_aware_payload_replacement_contract_refresh_summary.json
data/project_core_grid_aware_payload_replacement_contract_refresh.csv
figures/project_core_grid_aware_payload_replacement_contract_refresh.png
docs/PROJECT_CORE_GRID_AWARE_PAYLOAD_REPLACEMENT_CONTRACT_REFRESH.md
scripts/run_project_core_grid_aware_payload_replacement_contract_refresh.py
scripts/test_project_core_grid_aware_payload_replacement_contract_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
contract rows:                         8
homogeneous payload ready:             true
homogeneous payload worst L2:          0.6662947067388982
layered payload ready:                 true
layered payload worst L2:              0.6497571611891657
ready for presentation update:         true
field claim ready:                     false
historical outputs/experiments ready:  false
3D/FWI/GPU ready:                      false
ready for half-space promotion:        false
ready for outputs/experiments promo:   false
ready for field transfer:              false
ready for 3D validation:               false
ready for GPU work:                    false
```

Contract rows:

| Item | Active method | Evidence | Value | Ready | Scope |
| --- | --- | --- | ---: | --- | --- |
| homogeneous payload smoke | grid-aware target-cell payload | 093 | 0.5800814918790826 | true | run-089 homogeneous dielectric payload emission |
| homogeneous payload fresh stress | grid-aware target-cell payload | 094 | 0.6662947067388982 | true | three fresh homogeneous project-core cases |
| layered payload smoke | grid-aware payload with scalar Sommerfeld surface | 096 | 0.6497571611891657 | true | base air/concrete layered epsr-9 payload emission |
| layered payload fresh stress | grid-aware payload with scalar Sommerfeld surface | 097 | 0.6497571611891657 | true | four fresh air/concrete layered project-core cases |
| measured field claim | none | 163-175 | 0.0 | false | blocked until real controlled files and provenance pass |
| historical outputs/experiments promotion | none | 098 | 0.0 | false | blocked; current results are controlled project-core BEM/FDTD payload gates |
| 3D validation | external 3D FDTD/Bempp comparison path | 071-088 | 0.0 | false | blocked until real 3D target/background frequency-bin returns exist |
| GPU/FWI escalation | none | 098 | 0.0 | false | blocked; no GPU or FWI decision-changing run is justified |

## Interpretation

The current local BEM replacement boundary is now payload-based:

```text
homogeneous project-core cases:
  grid-aware target-cell payload

layered project-core cases:
  grid-aware target-cell payload with scalar Sommerfeld field provider
```

This is a scoped local 2D/project-core result. Measured-field, historical
`outputs/experiments`, 3D, GPU, and FWI claims remain blocked.

## Decision

Use the run `093`-`097` payload artifacts as the current BEM evidence for
presentation and planning. Do not promote beyond the scoped local 2D
project-core gates without separate matched evidence.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test:

```text
scripts/run_project_core_grid_aware_payload_replacement_contract_refresh.py
scripts/test_project_core_grid_aware_payload_replacement_contract_refresh.py
scripts/script_snapshot_manifest.json
```

Recorded SHA-256 values:

```text
run_project_core_grid_aware_payload_replacement_contract_refresh.py
76237046d01965ff14b620e8760511b0167bdfde5e88f3803c7dca6d1505e661

test_project_core_grid_aware_payload_replacement_contract_refresh.py
e102a61b65d135548b834cc65a2021c72872733b81221054e2faba81129bac96
```

## Validation

Focused tests:

```text
tests/test_project_core_grid_aware_payload_replacement_contract_refresh.py
2 passed
```

Figure check:

```text
project_core_grid_aware_payload_replacement_contract_refresh.png  2284x770, dynamic range=255
```
