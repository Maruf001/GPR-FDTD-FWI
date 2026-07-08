# BEM Experiment 500: 35-Field Real Return Producer-Route Audit

Date: 2026-06-29

## Purpose

Audit how the four required real return files could be produced for the
35-field BEM/FDTD normalized-comparator scorecard.

Runs `476`, `488`, and `494` already defined the file contract, acceptance
gate, and filesystem gap. This run asks whether the local codebase currently
contains an exact producer for those real-return files, or only templates,
synthetic consumers, and partial implementation references.

## Output

```text
outputs/bem_experiments/500_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_route_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_action_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
producer-route audit ready:                 true
required real return files:                 4
required real entries:                      1116
required real scorecard rows:               279
route rows:                                 4
action rows:                                5
exact real producer scripts ready:          0
producer gaps:                              4
partial local producer references:          176
open filesystem gaps:                       4
real-return file candidates:                0
blank-template candidates:                  4
synthetic-reference candidates:             4
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
```

The audit separates two ideas that were previously easy to confuse:

| File | Producer family | Exact producer ready | Required entries |
| --- | --- | ---: | ---: |
| `fdtd_source_hash_manifest.csv` | FDTD | false | 279 |
| `bem_source_hash_manifest.csv` | BEM | false | 279 |
| `fdtd_scattered_norm_values.csv` | FDTD | false | 279 |
| `bem_scattered_norm_values.csv` | BEM | false | 279 |

The repository contains many implementation references to FDTD, BEM, and
scattered-field norms, but no exact producer that writes the accepted
`real_return_files` CSV contract for these four files.

## Decision

The next BEM progress is producer-side work, not another consumer or template
audit. Build or receive the exact FDTD and BEM return files, then rerun the
real return-file acceptance gate and normalized-comparator scorecard.

Do not promote real BEM/FDTD comparison, 3D validation, GPU/HPC, field
transfer, or field FWI claims from the current templates or synthetic fills.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit.py
5 passed
```

Figure check:

```text
3257x842, dynamic range=255
```
