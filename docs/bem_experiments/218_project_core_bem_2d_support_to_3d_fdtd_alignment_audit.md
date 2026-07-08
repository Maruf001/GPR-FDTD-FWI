# BEM Experiment 218: 2D Support To 3D FDTD Alignment Audit

Date: 2026-06-28

## Purpose

Audit whether the guarded 2D support-specific BEM claim from runs `215`-`217`
can change the 3D FDTD validation path from runs `072` and `083`-`088`.

This run does not launch 3D FDTD, run a real BEM/FDTD comparison, compare
against field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/218_project_core_bem_2d_support_to_3d_fdtd_alignment_audit
```

Key artifacts:

```text
data/project_core_bem_2d_support_to_3d_fdtd_alignment_rows.csv
data/project_core_bem_2d_support_to_3d_fdtd_alignment_audit_summary.json
figures/project_core_bem_2d_support_to_3d_fdtd_alignment_audit.png
docs/PROJECT_CORE_BEM_2D_SUPPORT_TO_3D_FDTD_ALIGNMENT_AUDIT.md
scripts/run_project_core_bem_2d_support_to_3d_fdtd_alignment_audit.py
scripts/test_project_core_bem_2d_support_to_3d_fdtd_alignment_audit.py
```

## Result

```text
alignment items:                   10
ready or handoff-ready items:      4
direct 3D promotion blockers:      6
recommended 2D policy:             grid15_shell11_tabulated_surface_offset_repair
surface/support:                   grid_15mm_only + outer_shell_11mm_binary
external 3D request ready:         true
synthetic 3D return smoke ready:   true
real external FDTD data present:   false
direct 2D-to-3D promotion ready:   false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The audit finds that the latest 2D support claim is guarded, and the 3D
external-return pipeline remains handoff-ready, but six items block direct 2D
to 3D promotion: dimensionality/unknowns, source convention, medium model,
observable contract, absent real 3D FDTD data, and field transfer.

## Interpretation

The guarded 2D BEM correction is useful inside its tested local 2D family. It
does not replace the 3D finite-rebar Bempp/FDTD validation pipeline.

The 3D path still requires real paired target/background FDTD returns that pass
the existing metadata, schema, and comparator gates.

## Decision

Keep the 2D support claim and the 3D external-return gate separate.

Use the 2D result as bounded algorithm evidence. Keep real BEM/FDTD comparison,
3D validation, field transfer, GPU/HPC, and field FWI blocked until real
returned 3D FDTD data pass the existing acceptance gates.

## Validation

Focused tests:

```text
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_audit.py
3 passed
```

Python compile check:

```text
run_project_core_bem_2d_support_to_3d_fdtd_alignment_audit.py: pass
tests/test_project_core_bem_2d_support_to_3d_fdtd_alignment_audit.py: pass
```

Figure check:

```text
2897x879, dynamic range=255
```
