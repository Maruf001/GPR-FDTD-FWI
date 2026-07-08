# BEM Experiment 088: External 3D FDTD Return Full Bundle Smoke

Date: 2026-06-25

## Purpose

Create a synthetic external return bundle that satisfies both the metadata
preflight from run `086` and the frequency-bin return preflight from run `084`.

This is the full-bundle synthetic pass case for the external 3D FDTD handoff.

This run does not launch 3D FDTD, run the real comparator, field FWI, GPU/HPC
work, or neural-network training.

## Output

```text
outputs/bem_experiments/088_project_core_bem_3d_fdtd_external_return_full_bundle_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_full_bundle_metadata_checks.csv
data/project_core_bem_3d_fdtd_external_return_full_bundle_frequency_checks.csv
data/project_core_bem_3d_fdtd_external_return_full_bundle_smoke_summary.json
figures/project_core_bem_3d_fdtd_external_return_full_bundle_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_FULL_BUNDLE_SMOKE.md
synthetic_return/
scripts/run_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
scripts/test_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
synthetic frequency files:          2
frequency rows per run:             124
metadata preflight checks:          7
metadata blocking findings:         0
return preflight checks:            10
return blocking findings:           0
synthetic full bundle smoke pass:   true
synthetic smoke only:               true
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

## Interpretation

A complete synthetic external return bundle can satisfy both metadata and
frequency-bin return gates. This proves the full external-return acceptance
pipeline is satisfiable when files, schema, rows, components, metadata, and
hashes are complete.

The real external return remains absent. This run is synthetic only and does
not support a real BEM/FDTD comparison or 3D validation claim.

## Decision

Use run `088` only as an integration smoke for return-bundle acceptance. Keep
real BEM/FDTD comparison and 3D validation blocked until external returned data
pass the real run `086` metadata gate and run `084` frequency-bin gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py
2 passed
```

Compile check:

```text
run_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py: pass
tests/test_project_core_bem_3d_fdtd_external_return_full_bundle_smoke.py: pass
```

Figure check:

```text
1564x736, dynamic range=255
```
