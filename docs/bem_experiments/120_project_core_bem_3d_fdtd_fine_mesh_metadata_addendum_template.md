# BEM Experiment 120: Fine-Mesh Metadata Addendum Template

Date: 2026-06-27

## Purpose

Extend the external-return metadata template with fields that explicitly
identify the preferred fine-mesh BEM reference used by the nine-bin BEM/FDTD
comparison path.

This run does not launch FDTD, install real returned files, perform real
BEM/FDTD comparison, make a 3D validation claim, launch GPU/HPC work, run field
FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/120_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_metadata_requirements.csv
data/project_core_bem_3d_fdtd_fine_mesh_metadata_template.csv
data/project_core_bem_3d_fdtd_fine_mesh_metadata_hash_commands.csv
data/project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_METADATA_ADDENDUM_TEMPLATE.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
scripts/script_snapshot_manifest.json
```

## Result

```text
base combined metadata fields: 25
fine-mesh addendum fields:     5
full metadata fields:          30
blocking metadata fields:      29
nonblocking metadata fields:   1
prefilled template values:     18
blank template values:         12
metadata template ready:       true
real FDTD data ready:          false
real BEM/FDTD comparison ready:false
3D validation claim ready:     false
```

New fine-mesh addendum fields:

| Metadata key | Required value |
| --- | --- |
| `bem_reference_mesh` | `Bempp finite cylinder axial_segments=8 radial_segments=20` |
| `bem_reference_frequency_count` | `9` |
| `bem_reference_receiver_count` | `31` |
| `bem_scattered_reference_sha256` | `f8c7a778275938ce6360cc7cc6fe8fb25151c169e7249e1fd3e5b17b99d57eaa` |
| `comparator_pass_threshold_relative_l2` | `0.1` |

## Interpretation

The older combined metadata ledger has 25 fields, but the preferred comparison
now depends on the `8x20` fine-mesh BEM reference and the run `118` comparator
threshold. This run adds five explicit fine-mesh reference fields, bringing the
fillable template to 30 fields.

## Decision

Use this 30-field template for preferred nine-bin external FDTD returns. A
future real-return preflight should require these fine-mesh addendum fields
before accepting real comparison data.

Real BEM/FDTD comparison, 3D validation, layered 3D GPR claims, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
real target/background files and the filled metadata ledger pass the gate.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
sha256: 37f19e2688a588068abdf0e2ca89535c0ee0363f5337d4ee5da565ab54f1d95f

test_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
sha256: 0a9c4fbdcc5357b8aa5e5c88a09ee7648f663b2a8e2942eecf63b6d2d93625b4
```

Subsequent related BEM/FDTD return experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_metadata_addendum_template.png
2680x851, dynamic range=255
```
