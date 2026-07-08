# BEM Experiment 526: Bempp 35-Field Fine-Mesh Candidate Value Export Validator

Date: 2026-06-30

## Purpose

Validate run `525`, the full 8x20 Bempp-side candidate value export.

Run `525` wrote two BEM-side candidate return-file tables over all 31 receivers
and nine frequencies. This validator confirms that the fine-mesh candidate
files are complete, finite, on the expected 8x20 mesh, and still not accepted
BEM/FDTD evidence.

## Output

```text
outputs/bem_experiments/526_project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator_checks.csv
data/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator_summary.json
figures/project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
fine-mesh export validation ready:         true
fine-mesh candidate export ready:          true
candidate source-hash entries:             279
candidate scattered-norm entries:          279
ready frequency rows:                      9
accepted real return files:                0
matched FDTD return files present:         false
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
```

## Decision

Use run `526` as the artifact guard for the run `525` 8x20 fine-mesh BEM
candidate export.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_fine_mesh_endpoint_probe.py
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export.py
tests/test_project_core_bem_bempp_35field_fine_mesh_candidate_value_export_validator.py
12 passed
```

Figure check:

```text
2501x834, dynamic range=255
```
