# BEM Experiment 073: 3D FDTD Manifest Contract

Date: 2026-06-25

## Purpose

Write paired target/background FDTD manifest templates for the run `072` Bempp
dipole-source reference.

This is a no-launch design artifact. It does not run 3D FDTD, field FWI,
GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/073_project_core_bem_3d_fdtd_manifest_contract
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_target_manifest_template.json
data/project_core_bem_3d_fdtd_background_manifest_template.json
data/project_core_bem_3d_fdtd_receiver_positions.csv
data/project_core_bem_3d_fdtd_frequency_bins.csv
data/project_core_bem_3d_fdtd_manifest_comparison_requirements.csv
data/project_core_bem_3d_fdtd_manifest_contract_summary.json
figures/project_core_bem_3d_fdtd_manifest_contract.png
docs/PROJECT_CORE_BEM_3D_FDTD_MANIFEST_CONTRACT.md
```

## Result

```text
manifest templates:                  2
receiver count:                      31
frequency count:                     4
comparison requirements:             7
missing external FDTD runs:          2
blocked requirements:                3
grid cells with PML:                 268800
time steps:                          630
padded memory estimate GiB:          0.16021728515625
paired FDTD manifest templates ready:true
paired FDTD data ready:              false
3D FDTD launch ready:                false
3D validation claim ready:           false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

## Interpretation

The run `072` Bempp dipole source now has explicit target/background FDTD
manifest templates and comparison requirements. The target manifest includes
the finite PEC cylinder; the background manifest omits it. Both preserve the
same homogeneous epsr-6 medium, source, receivers, and frequency bins.

The comparison remains blocked by missing external FDTD target and background
outputs. This run is therefore a contract for future implementation or import,
not a validation result.

## Decision

Use these manifests as the input contract for any future 3D FDTD implementation
or imported result.

Do not launch or claim validation until the target/background runs are explicitly
produced and pass the manifest gates.

## Validation

Figure check:

```text
2104x840, dynamic range=255
```
