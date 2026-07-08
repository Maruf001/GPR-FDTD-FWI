# BEM Experiment 106: Bempp Dipole Mesh-Refinement Audit

Date: 2026-06-27

## Purpose

Check whether the local 3D Bempp finite-rebar dipole prototype is stable when
the triangular surface mesh is refined.

Run `072` proved that the 3D Bempp prototype can solve a homogeneous finite
rebar with a GPR-like point-dipole source. This run asks the next numerical
question:

```text
Is the selected baseline mesh close enough to a finer mesh for the receiver-line
observable we plan to compare against future paired 3D FDTD returns?
```

This is a homogeneous perfect-electric-conductor frequency-domain BEM audit. It
does not run 3D FDTD, use measured field data, launch GPU/HPC work, or validate
a layered 3D GPR forward model.

## Output

```text
outputs/bem_experiments/106_project_core_bem_bempp_dipole_mesh_refinement_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_dipole_mesh_refinement_cases.csv
data/project_core_bem_bempp_dipole_mesh_refinement_frequency_summary.csv
data/project_core_bem_bempp_dipole_mesh_refinement_receivers.csv
data/project_core_bem_bempp_dipole_mesh_refinement_comparisons.csv
data/project_core_bem_bempp_dipole_mesh_refinement_audit_summary.json
figures/project_core_bem_bempp_dipole_mesh_refinement_audit.png
docs/PROJECT_CORE_BEM_BEMPP_DIPOLE_MESH_REFINEMENT_AUDIT.md
scripts/run_project_core_bem_bempp_dipole_mesh_refinement_audit.py
scripts/test_project_core_bem_bempp_dipole_mesh_refinement_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
mesh cases:                         3
frequencies checked:                2
receiver rows:                      186
comparison rows:                    6
finite all responses:               true
Bempp return codes all zero:         true
baseline-to-fine max relative L2:    0.010296810068779048
baseline-to-fine max shape L2:       0.00036683620112687774
coarse-to-fine max relative L2:      0.032293038544475516
refinement change decreases:         true
mesh-stability audit passed:         true
Bempp 3D dipole mesh baseline ready: true
3D FDTD validation ready:            false
layered 3D GPR ready:                false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Mesh comparisons:

| Frequency GHz | Left mesh | Right mesh | Relative L2 | Shape L2 | Peak ratio |
| ---: | --- | --- | ---: | ---: | ---: |
| 0.5 | coarse_4x12 | baseline_6x16 | 0.02222509 | 0.00013356 | 0.97773210 |
| 0.5 | baseline_6x16 | fine_8x20 | 0.01029681 | 0.00003966 | 0.98968984 |
| 0.5 | coarse_4x12 | fine_8x20 | 0.03229304 | 0.00017321 | 0.96765153 |
| 1.5 | coarse_4x12 | baseline_6x16 | 0.00559136 | 0.00095409 | 0.99528559 |
| 1.5 | baseline_6x16 | fine_8x20 | 0.00370427 | 0.00036684 | 0.99666208 |
| 1.5 | coarse_4x12 | fine_8x20 | 0.00926867 | 0.00131605 | 0.99196340 |

## Interpretation

The baseline `6x16` finite-cylinder mesh is close to the finer `8x20` mesh for
the tested dipole receiver-line observable. The largest baseline-to-fine
amplitude change is about 1.03%, and the normalized line-shape differences are
much smaller. The refinement change also decreases from the coarse-to-baseline
step to the baseline-to-fine step.

This supports the current `6x16` mesh as a practical local 3D Bempp prototype
baseline. It does not validate the BEM result against 3D FDTD, and it does not
close the layered-material or measured-field gates.

## Decision

Keep the `6x16` Bempp dipole mesh as the local 3D prototype baseline for future
matched FDTD comparison setup work.

Do not treat this as 3D FDTD validation, layered 3D GPR readiness, field FWI
readiness, or GPU/HPC readiness. It only supports the BEM-side prototype
stability claim.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_bempp_dipole_mesh_refinement_audit.py
sha256: 5242ef7fa47a194287be94c2232a022fbc35c000a2f9ee200858e7a51116fde8

test_project_core_bem_bempp_dipole_mesh_refinement_audit.py
sha256: 359529271a30090c3fcb5ee3eec931a907d70f859136270eda42ba85b936c2d1
```

Subsequent Bempp 3D source or receiver-convention experiments should start
from a duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_dipole_mesh_refinement_audit.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_dipole_mesh_refinement_audit.png
2644x845, dynamic range=255
```
