# BEM Experiment 123: Fine-Mesh Handoff Bundle Unpack Smoke

Date: 2026-06-27

## Purpose

Unpack the run `122` fine-mesh BEM/FDTD handoff bundle into an isolated output
folder and verify the embedded checksum ledger from the consumer side.

This run does not create real FDTD data, run 3D FDTD locally, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/123_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_members.csv
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_checksums.csv
data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_HANDOFF_BUNDLE_UNPACK_SMOKE.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source archive SHA-256 matches run 122: true
archive members:                     17
archive safe members:                17
archive unsafe members:              0
checksum entries:                    16
checksum entries passing:            16
checksum entries failing:            0
extracted files:                     17
extracted attachments:               14
extracted helper files:              3
unpack smoke ready:                  true
bundle ready for handoff:            true
real FDTD data ready:                false
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
```

Archive checked:

```text
outputs/bem_experiments/122_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle/data/project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.tar.gz
sha256: a041256e8182db8b5d25e3ad09ffc31a60c59c947ce7a7509f530754f4e942d7
```

## Interpretation

The run `122` fine-mesh handoff bundle can be extracted safely, and all
embedded checksum entries verify. This proves the handoff archive is
transport-readable.

It still contains templates and BEM reference context rather than returned real
FDTD target/background data.

## Decision

Use the run `122` bundle for the preferred nine-frequency external FDTD return.
Keep real BEM/FDTD comparison, 3D validation, local 3D FDTD launch, GPU/HPC,
layered 3D GPR claims, field FWI, and neural-network training blocked until
real returned files pass the run `121` preflight.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.py
sha256: c514265232fc5a54ab1c4324b22ee94e8177c62e44547af8f9cf67d5b3a1af7f

test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.py
sha256: 1b03185bcf87d6e45ff5100a7d1148dcab9a85f4b30ca2dec524fd13434fcc5b
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused BEM bundle tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.py
10 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_handoff_bundle_unpack_smoke.png
1888x738, dynamic range=255
```
