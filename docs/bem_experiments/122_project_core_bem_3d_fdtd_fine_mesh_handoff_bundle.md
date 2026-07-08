# BEM Experiment 122: Fine-Mesh BEM/FDTD Handoff Bundle

Date: 2026-06-27

## Purpose

Package the preferred fine-mesh BEM/FDTD return templates, metadata ledger,
preflight gate, and BEM reference context into one handoff bundle.

This run does not create real FDTD data, run 3D FDTD locally, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/122_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle
```

Key artifacts:

```text
bundle/
bundle/CHECKSUMS.sha256
bundle/README.md
bundle/RETURN_INSTRUCTIONS.md
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.tar.gz
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_attachments.csv
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_HANDOFF_BUNDLE.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
scripts/script_snapshot_manifest.json
```

## Result

```text
bundle attachment files:          14
helper files:                     3
frequency count:                  9
receiver count:                   31
rows per target/background file:  279
paired target/background rows:    558
metadata fields:                  30
blocking metadata fields:         29
comparator threshold relative L2: 0.1
bundle ready for handoff:         true
real FDTD data ready:             false
real BEM/FDTD comparison ready:   false
3D validation claim ready:        false
```

Bundle archive:

```text
outputs/bem_experiments/122_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle/data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.tar.gz
sha256: a041256e8182db8b5d25e3ad09ffc31a60c59c947ce7a7509f530754f4e942d7
size bytes: 55669
```

Bundle contents:

| Section | Attachments |
| --- | ---: |
| return input templates | 3 |
| return metadata | 3 |
| return gate | 3 |
| BEM reference | 4 |
| comparison context | 1 |

## Interpretation

The preferred fine-mesh BEM side and the synthetic comparator are now packaged
with the exact nine-frequency target/background templates and the 30-field
metadata ledger. This makes the external return path handoff-ready.

The bundle does not contain real FDTD target/background data. The current
preflight remains blocked by missing real target, background, and metadata
files.

## Decision

Use this bundle for the preferred nine-frequency external FDTD return. Keep
real BEM/FDTD comparison, 3D validation, local 3D FDTD launch, GPU/HPC, layered
3D GPR claims, field FWI, and neural-network training blocked until returned
files pass the run `121` preflight.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
sha256: 06daeeb9b41648887639b91eed2cb7d7657ebbcb456174da5b203994073bb519

test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
sha256: b6841fe98fbd073516cab5e14e53cb9a13eb0b8dd8a20ed341d1438f9e57581f
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused upstream and bundle tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_templates.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_bem_reference_export.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_comparator_synthetic_sensitivity.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_30field_refresh.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
23 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.png
2680x850, dynamic range=255
```
