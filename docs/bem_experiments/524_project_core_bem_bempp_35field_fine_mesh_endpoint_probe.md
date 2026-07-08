# BEM Experiment 524: Bempp 35-Field Fine-Mesh Endpoint Probe

Date: 2026-06-30

## Purpose

Test whether the Bempp candidate exporter can move from the run `521` 4x12
smoke mesh toward the 8x20 fine-reference mesh.

Run `521` produced complete BEM-side candidate values on the required 31-by-9
grid, but the mesh did not match the 8x20 fine-reference setting identified
earlier in the BEM track. This run solves the 8x20 mesh at the two frequency
endpoints, 400 MHz and 3 GHz, and compares those receiver-line values against
the 4x12 candidate export.

## Output

```text
outputs/bem_experiments/524_project_core_bem_bempp_35field_fine_mesh_endpoint_probe
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_fine_mesh_endpoint_probe_frequency_rows.csv
data/project_core_bem_bempp_35field_fine_mesh_endpoint_probe_receiver_rows.csv
data/project_core_bem_bempp_35field_fine_mesh_endpoint_probe_summary.json
figures/project_core_bem_bempp_35field_fine_mesh_endpoint_probe.png
scripts/script_snapshot_manifest.json
```

## Result

```text
endpoint frequencies tested:              2
fine endpoint solves ready:               2
receiver rows:                            62
fine mesh endpoint probe ready:           true
fine mesh matches 8x20 reference:         true
estimated 9-frequency runtime:            192.5 s
endpoint solve time total:                42.8 s
4x12-to-8x20 relative L2 min:             0.0389
4x12-to-8x20 relative L2 max:             0.2535
4x12-to-8x20 relative L2 mean:            0.1462
full 8x20 35-field export complete:       false
matched FDTD return files present:        false
accepted evidence ready:                  false
real BEM/FDTD comparison ready:           false
```

Endpoint details:

| Frequency | Fine mesh elements | Fine RWG DOFs | Relative L2 vs 4x12 | Fine mean norm | Coarse mean norm |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 400 MHz | 360 | 540 | 0.0389 | 0.0633 | 0.0608 |
| 3 GHz | 360 | 540 | 0.2535 | 0.3301 | 0.4147 |

## Interpretation

The 8x20 fine mesh is feasible in the local Bempp environment for this
homogeneous PEC finite-cylinder setup. The high-frequency endpoint changes the
receiver-line response substantially compared with the 4x12 smoke mesh, so a
full 8x20 nine-frequency candidate export is justified.

The result is still a BEM-side mesh-sensitivity checkpoint only. It is not a
matched FDTD return and not accepted comparison evidence.

## Decision

Use run `524` as the go signal for a full 8x20 Bempp-side candidate value
export over all nine frequencies. Keep BEM/FDTD comparison, 3D validation,
GPU/HPC, field transfer, and field FWI blocked until matched FDTD return files
and accepted evidence writing exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_fine_mesh_endpoint_probe.py
4 passed
```

Figure check:

```text
2824x845, dynamic range=255
```
