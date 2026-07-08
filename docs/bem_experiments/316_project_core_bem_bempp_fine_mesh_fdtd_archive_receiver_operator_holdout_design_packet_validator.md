# BEM Experiment 316: Receiver Operator Holdout Design Packet Validator

Date: 2026-06-28

## Purpose

Validate the saved run `315` receiver-operator holdout design packet from a
consumer perspective.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC,
field transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/316_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_DESIGN_PACKET_VALIDATOR.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
source design packet ready:         true
required files:                     9
acceptance checks:                  7
frozen operator rows:               27
apply without refit:                true
holdout data present:               false
receiver operator holdout ready:    false
physical claim ready:               false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
field transfer ready:               false
GPU/HPC ready:                      false
field FWI ready:                    false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and packet counts | pass |
| required file worklist is exact and unfilled | pass |
| acceptance check contract is exact | pass |
| frozen operator rows are apply-only | pass |
| holdout data and downstream states blocked | pass |
| source run lineage present | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The run `315` holdout design packet validates as an exact apply-only worklist:
nine missing future artifacts, seven acceptance checks, and 27 frozen operator
coefficient rows are present, while holdout data and all physical/downstream
claims remain blocked.

## Decision

Use run `316` as the guarded validator for the run `315` holdout design
packet. Do not promote the receiver-operator diagnostic, BEM/FDTD agreement,
3D validation, field transfer, GPU/HPC, or field FWI until an independent
holdout pair exists and passes apply-only validation.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_validator.py
3 passed
```

Figure validation:

```text
2897x892, dynamic range=255
```
