# BEM Experiment 315: Receiver Operator Holdout Design Packet

Date: 2026-06-28

## Purpose

Turn the run `314` holdout blocker into an exact design packet for the next
independent BEM/FDTD receiver-operator holdout.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC,
field transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/315_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_required_files.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_acceptance_checks.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_frozen_operator_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_DESIGN_PACKET.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required files:                     9
acceptance checks:                  7
frozen operator models:             3
frozen operator frequency rows:     27
expected receivers:                 31
expected frequencies:               9
expected rows per export:           279
apply without refit:                true
holdout design packet ready:        true
holdout data present:               false
receiver operator holdout ready:    false
physical claim ready:               false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
field transfer ready:               false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The packet freezes three run `311` operator families for future apply-only
holdout validation:

| Operator model | Frequencies | Holdout usage |
| --- | ---: | --- |
| identity scale | 9 | baseline only |
| edge and gradient | 9 | apply only, no refit |
| edge, gradient, and curvature | 9 | apply only, no refit |

Required future artifacts:

| Artifact | Required rows | Purpose |
| --- | ---: | --- |
| holdout BEM total target reference | 279 | BEM total-field target reference for the independent holdout geometry |
| holdout BEM incident background reference | 279 | BEM background reference |
| holdout BEM scattered reference | 279 | BEM scattered reference for operator application |
| holdout FDTD target frequency rows | 279 | independent FDTD target-scene export |
| holdout FDTD background frequency rows | 279 | independent FDTD background-scene export |
| holdout FDTD scattered frequency rows | 279 | target-minus-background scattered rows |
| holdout receiver-operator apply-only rows | 54 | apply edge-and-gradient and edge-gradient-curvature operators without refitting |
| holdout pair metadata | 1 | pair id, geometry hash, source/receiver lock, solver versions, and no-refit declaration |
| holdout operator validation summary | 1 | pass/fail summary for the independent holdout |

## Interpretation

Run `314` showed that no independent holdout currently exists. Run `315`
converts that blocker into a concrete implementation target. The key rule is
that the run `311` receiver operators must be applied to the holdout without
refitting on holdout data. Otherwise the holdout would repeat the same
training-on-the-evaluation-grid problem that blocked physical interpretation.

## Decision

Use run `315` as the BEM receiver-operator holdout design packet. Do not
promote the receiver-operator diagnostic, BEM/FDTD agreement, 3D validation,
field transfer, GPU/HPC, or field FWI until the required independent holdout
data exist and pass the apply-only validation.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_design_packet.py
3 passed
```

Figure validation:

```text
2789x865, dynamic range=255
```
