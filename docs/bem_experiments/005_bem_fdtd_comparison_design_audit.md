# BEM Experiment 005: BEM/FDTD Comparison Design Audit

Date: 2026-06-23

## Purpose

Check whether the run `004` Bempp receiver response can be compared directly
against the current in-repo FDTD stack, and define the scientifically valid
next comparison path.

This is a design audit. It does not run FDTD, BEM/FDTD cross-validation,
field-data processing, inversion, or heavy GPU work.

## Output

```text
outputs/bem_experiments/005_bem_fdtd_comparison_design_audit
```

Key artifacts:

```text
data/fdtd_source_capabilities.csv
data/bem_fdtd_comparison_options.csv
data/bem_fdtd_comparison_design_summary.json
docs/BEM_FDTD_COMPARISON_DESIGN_AUDIT.md
run_manifest.json
```

## Result

```text
BEM response contract ready:          true
BEM receiver count:                   41
BEM max scattered norm:               0.027575913303849516
current FDTD 2D TMz ready:            true
current FDTD 3D ready:                false
direct 3D apples-to-apples ready:     false
2D sanity check ready:                true
BEM-only frequency sweep ready:       true
layered GPR or field claim ready:     false
recommended next:                     2d_tmz_cross_section_sanity_then_new_3d_fdtd_reference_design
```

The source capability audit identifies the current FDTD stack as 2D TMz:

| Component | Capability | Present |
| --- | --- | ---: |
| `core.fdtd` | CPU 2D TMz Yee FDTD with CPML | true |
| `gpu.fdtd_gpu` | GPU 2D TMz Yee FDTD | true |
| `gpu.fdtd_gpu_v2` | GPU 2D TMz Yee FDTD with CPML | true |
| `core.materials` | 2D material arrays | true |
| `core.geometry` | 2D circular rebar cross-sections | true |

## Interpretation

Run `004` gives a useful BEM response contract, but it is a 3D finite-cylinder
Maxwell result. The existing FDTD stack models a 2D TMz cross-section. A direct
quantitative comparison is therefore not ready.

The valid immediate comparison is a 2D sanity check: use the current FDTD code
to test response extraction and qualitative trends for an infinite-cylinder
cross-section. That should not be described as validation of the 3D BEM finite
rebar result.

## Decision

Use this sequence:

```text
1. 2D TMz cross-section sanity check using current FDTD.
2. Separate small 3D FDTD reference design for direct validation of run 004.
3. Only after validation, consider layered concrete/air, broadband GPR, antenna
   coupling, or inversion.
```

Do not claim BEM/FDTD validation, layered GPR readiness, field readiness, or
BEM-FWI readiness from the current run `004`/`005` evidence.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bem_fdtd_comparison_design_audit.py
python -m py_compile run_bem_fdtd_comparison_design_audit.py
conda run -n gpr-fdtd-fwi python run_bem_fdtd_comparison_design_audit.py --outdir outputs/bem_experiments/005_bem_fdtd_comparison_design_audit
```

## Next Action

Create the 2D TMz cross-section sanity check as a clearly labeled non-validation
experiment, or begin a separate minimal 3D FDTD reference design.
