# BEM Experiment 317: Receiver Operator Holdout Design Packet Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `316` validator for the run `315` receiver-operator
holdout design packet.

The exact run `315` design packet should pass. Damaged copies should fail when
file worklists, acceptance checks, frozen operators, summary states, downstream
guards, figure validation, or script snapshots drift.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC,
field transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/317_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_DESIGN_PACKET_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          41
expected pass scenarios:             1
observed pass scenarios:             1
expected failure scenarios:          40
observed failure scenarios:          40
unexpected outcomes:                  0
sensitivity ready:                   true
exact run 315 accepted:              true
damaged variants rejected:           true
holdout data present:                false
receiver operator holdout ready:     false
physical claim ready:                false
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
field transfer ready:                false
GPU/HPC ready:                       false
field FWI ready:                     false
```

Damage coverage:

| Category | Damaged variants |
| --- | ---: |
| required file worklist | 5 |
| acceptance-check contract | 4 |
| frozen operator rows | 7 |
| source summary and packet counts | 10 |
| downstream promotion | 8 |
| source lineage | 1 |
| figure validation | 3 |
| script snapshots | 2 |

## Interpretation

The holdout design-packet validator accepts the exact run `315` packet and
rejects every damaged variant tested here. The rejected cases cover file
worklist drift, acceptance-check drift, frozen-operator drift, summary drift,
downstream promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `315-317` as the guarded BEM receiver-operator holdout design-packet
block. Continue to require independent holdout data and apply-only validation
before any physical BEM/FDTD, 3D, field-transfer, GPU/HPC, or field-FWI claim.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_sensitivity.py
3 passed
```

Figure validation:

```text
3256x1565, dynamic range=255
```
