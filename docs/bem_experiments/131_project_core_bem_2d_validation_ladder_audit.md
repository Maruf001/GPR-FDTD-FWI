# BEM Experiment 131: 2D Validation Ladder Audit

Date: 2026-06-27

## Purpose

Synthesize the BEM-track 2D validation ladder from the scarep analytic
convergence and matched BEM/FDTD adapter runs.

This run does not compare against the project FDTD archive, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/131_project_core_bem_2d_validation_ladder_audit
```

Key artifacts:

```text
data/project_core_bem_2d_validation_ladder_rows.csv
data/project_core_bem_2d_validation_ladder_audit_summary.json
figures/project_core_bem_2d_validation_ladder_audit.png
docs/PROJECT_CORE_BEM_2D_VALIDATION_LADDER_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
stage count:                         4
ready stage count:                   4
matched BEM/FDTD stage count:        3
best matched FDTD/BEM relative L2:   0.02330746966791303
half-space FDTD/BEM relative L2:     0.030998297443390457
project-core FDTD matched stages:    0
uses project experiment archive:     false
validation ladder ready:             true
project-core FDTD comparison ready:  false
field FWI ready:                     false
3D validation ready:                 false
gpu/hpc ready:                       false
```

Ladder rows:

| Stage | Reference | BEM/reference error | FDTD/BEM error | Ready |
| --- | --- | ---: | ---: | --- |
| scarep_dielectric_analytic_convergence | analytic_dielectric_cylinder | 0.0007053747139208214 |  | true |
| matched_dielectric_bem_fdtd | analytic_dielectric_cylinder | 0.003190629524250936 | 0.02330746966791303 | true |
| matched_pec_bem_fdtd | analytic_pec_cylinder | 4.762231342258939e-05 | 0.03432024436144074 | true |
| matched_halfspace_pec_bem_fdtd | 32_panel_layered_bem_reference | 0.0004746867074423852 | 0.030998297443390457 | true |

## Interpretation

The BEM track now has a coherent 2D validation ladder:

- scarep CPU BEM analytic convergence on a dielectric cylinder;
- matched dielectric BEM/FDTD in free space;
- matched PEC-cylinder BEM/FDTD in free space;
- matched air/concrete half-space PEC BEM/FDTD.

This validates BEM-side method behavior and matched 2D adapters. It still does
not validate the older project FDTD archive, measured field data, or 3D
finite-rebar modeling.

## Decision

Use this ladder as the BEM-side 2D validation checkpoint. The next comparison
step remains a project-core FDTD adapter or real returned 3D FDTD files. Do
not treat this as field evidence, project archive validation, or 3D validation.

## Validation

Focused test:

```text
tests/test_project_core_bem_2d_validation_ladder_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_2d_validation_ladder_audit.png
2859x847, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_2d_validation_ladder_audit.py
sha256=9730e6af4b5aa354f5c5a138caaea38603cfdf0f83bf7a0f1ae43f4e160c49ee

tests/test_project_core_bem_2d_validation_ladder_audit.py
sha256=828dba1cb8a17581385c81c808fb811d3b8c953c2edd767a177cd43e4e90fdde
```
