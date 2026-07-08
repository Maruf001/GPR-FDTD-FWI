# BEM Experiment 074: 3D FDTD Manifest Validator

Date: 2026-06-25

## Purpose

Validate the paired target/background FDTD manifest templates from run `073`
before any FDTD data exist.

This is a no-launch validator. It does not run 3D FDTD, field FWI, GPU/HPC
work, or neural-network training.

## Output

```text
outputs/bem_experiments/074_project_core_bem_3d_fdtd_manifest_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_manifest_validation.csv
data/project_core_bem_3d_fdtd_manifest_validator_summary.json
figures/project_core_bem_3d_fdtd_manifest_validator.png
docs/PROJECT_CORE_BEM_3D_FDTD_MANIFEST_VALIDATOR.md
```

## Result

```text
validation checks:                   9
passed checks:                       9
failed checks:                       0
manifest templates valid:            true
receiver count:                      31
frequency count:                     4
paired FDTD data ready:              false
3D FDTD launch ready:                false
3D validation claim ready:           false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Checks passed:

```text
manifest types
template status
target/background pairing except target fields
target presence delta
receiver pairing
frequency pairing
source pairing
domain pairing
current data explicitly absent
```

## Interpretation

The run `073` target/background manifests are internally paired and valid as
templates. This improves handoff quality but does not create FDTD data.

## Decision

Use this validator as the preflight gate before accepting any future FDTD
target/background result for BEM comparison.

Keep 3D validation blocked until real paired FDTD outputs exist.

## Validation

Figure check:

```text
2106x844, dynamic range=255
```
