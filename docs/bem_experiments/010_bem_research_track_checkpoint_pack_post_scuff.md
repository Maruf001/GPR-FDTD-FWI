# BEM Experiment 010: Research Track Checkpoint Pack Post SCUFF

Date: 2026-06-23

## Purpose

Refresh the BEM research checkpoint after the SCUFF-EM feasibility probe in
run `009`. This pack aggregates all current BEM evidence from runs `001`-`007`
and `009`.

This is a synthesis/checkpoint run. It does not run new BEM solves, FDTD
validation, field-data processing, inversion, or heavy GPU work.

## Output

```text
outputs/bem_experiments/010_bem_research_track_checkpoint_pack_post_scuff
```

Key artifacts:

```text
data/bem_research_run_matrix.csv
data/bem_backend_applicability.csv
data/bem_research_track_checkpoint_summary.json
docs/BEM_RESEARCH_TRACK_CHECKPOINT_PACK.md
run_manifest.json
```

## Result

```text
runs aggregated:                  8
backends aggregated:              3
primary backend:                  bempp-cl
reference backends:               OpenBEM, SCUFF-EM
validated 3D BEM/FDTD ready:      false
layered GPR BEM ready:            false
BEM-FWI ready:                    false
```

Current backend decision:

```text
The BEM track is viable and should continue in parallel with FDTD. bempp-cl is
the best first prototype backend; OpenBEM and SCUFF-EM remain valuable
references/tools with licensing and integration caveats. Current evidence
supports prototype development and presentation, not a validated 3D GPR-BEM or
BEM-FWI claim.
```

## Proven Now

- A separate BEM docs/output track exists.
- SCUFF-EM, `bempp-cl`, and OpenBEM have been cloned and assessed.
- OpenBEM C++ examples build and run locally.
- The isolated `bempp-cl` environment imports and solves a Maxwell sphere smoke.
- `bempp-cl` solves a direct finite rebar-like cylinder without Gmsh.
- `bempp-cl` emits a receiver-line scattered-field response.
- The direct finite-rebar response remains finite across a small wavenumber sweep.
- The current 2D TMz FDTD stack emits a finite single-rebar sanity response.
- SCUFF-EM has relevant scattering/RF examples but is not locally dependency-ready.

## Not Proven Yet

- Direct 3D BEM/FDTD validation.
- Layered concrete/air BEM forward modeling.
- Broadband time-domain GPR synthesis from BEM.
- Antenna/source coupling equivalence.
- Field-data readiness.
- BEM-FWI readiness.

## Presentation Outline

1. Motivation: 3D FDTD is expensive, so BEM is a parallel fast-forward-model track.
2. Repository assessment: `bempp-cl` for first Python prototype, OpenBEM for RWG formulation reference, SCUFF-EM as mature external benchmark/reference.
3. Current prototype evidence: Bempp environment, direct finite-cylinder mesh, Maxwell solve, receiver response, and frequency sweep.
4. Validation boundary: current FDTD is 2D TMz, so run `004` is not directly validated yet.
5. Next technical decision: reproduce verified 2D GPR-BEM code, then define a shared BEM/FDTD comparison problem or small 3D FDTD reference.

## Decision

Use run `010` as the current BEM research checkpoint.

The preferred technical branch is still:

```text
1. receive/import the verified 2D GPR-BEM code;
2. reproduce the known 2D cases;
3. define a shared BEM/FDTD comparison problem;
4. only then add layered media, broadband handling, and inversion hooks.
```

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bem_research_track_checkpoint_pack.py
python -m py_compile run_bem_research_track_checkpoint_pack.py
conda run -n gpr-fdtd-fwi python run_bem_research_track_checkpoint_pack.py --outdir outputs/bem_experiments/010_bem_research_track_checkpoint_pack_post_scuff
```

## Next Action

Begin the shared-comparison design or wait for the colleague's verified 2D
GPR-BEM code, then reproduce those cases inside this BEM track.
