# BEM Experiment 086: External 3D FDTD Return Metadata Preflight

Date: 2026-06-25

## Purpose

Make the run `085` external-return metadata handoff machine-checkable before
returned files are accepted for the run `084` frequency-bin return preflight.

This run answers:

```text
Can the returned metadata ledger and SHA-256 file hashes be validated before
the project trusts external 3D FDTD target/background files?
```

This is a CPU-only preflight. It does not launch 3D FDTD, run the real
BEM/FDTD comparator, field FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/086_project_core_bem_3d_fdtd_external_return_metadata_preflight
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_metadata_preflight.csv
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_summary.json
figures/project_core_bem_3d_fdtd_external_return_metadata_preflight.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_METADATA_PREFLIGHT.md
scripts/run_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
scripts/test_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
scripts/script_snapshot_manifest.json
```

## Result

```text
metadata requirements:              12
preflight checks:                   7
passed checks:                      0
failed checks:                      7
blocking findings:                  7
metadata preflight ready:           false
return file hashes verified:        false
ready for return preflight:         false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

## Interpretation

The metadata preflight is executable and currently fails for the right reason:
the pending external return has no metadata ledger and no hash-verifiable
target/background files.

This is not a 3D validation result. It is the gate that prevents external
returned files from being accepted without provenance and hash checks.

## Decision

Require run `086` to pass before trusting returned external 3D FDTD files
enough to run run `084`. Then require run `084` to pass before any real
BEM/FDTD comparator or 3D validation claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight.py
3 passed
```

Compile check:

```text
run_project_core_bem_3d_fdtd_external_return_metadata_preflight.py: pass
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight.py: pass
```

Figure check:

```text
1924x772, dynamic range=255
```
