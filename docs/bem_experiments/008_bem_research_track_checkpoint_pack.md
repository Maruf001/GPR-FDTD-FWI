# BEM Experiment 008: Research Track Checkpoint Pack

Date: 2026-06-23

## Purpose

Aggregate BEM runs `001` through `007` into a single checkpoint and
presentation-oriented pack. This turns the separate repository evaluation,
Bempp probes, response contract, FDTD audit, frequency sweep, and 2D FDTD
sanity check into one resumable research state.

This is a synthesis/checkpoint run. It does not run new BEM solves, FDTD
validation, field-data processing, inversion, or heavy GPU work.

## Output

```text
outputs/bem_experiments/008_bem_research_track_checkpoint_pack
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
runs aggregated:                  7
backends aggregated:              3
primary backend:                  bempp-cl
reference backends:               OpenBEM, SCUFF-EM
validated 3D BEM/FDTD ready:      false
layered GPR BEM ready:            false
BEM-FWI ready:                    false
```

The checkpoint decision is:

```text
The BEM track is viable and should continue in parallel with FDTD. bempp-cl is
the best first prototype backend; OpenBEM and SCUFF-EM remain valuable
references/tools with licensing and integration caveats. Current evidence
supports prototype development and presentation, not a validated 3D GPR-BEM or
BEM-FWI claim.
```

## Proven Now

- A separate BEM docs/output track exists.
- SCUFF-EM, bempp-cl, and OpenBEM have been cloned and assessed.
- OpenBEM C++ examples build and run locally.
- The isolated `bempp-cl` environment imports and solves a Maxwell sphere smoke.
- `bempp-cl` solves a direct finite rebar-like cylinder without Gmsh.
- `bempp-cl` emits a receiver-line scattered-field response.
- The direct finite-rebar response remains finite across a small wavenumber sweep.
- The current 2D TMz FDTD stack emits a finite single-rebar sanity response.

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

Use run `008` as the current BEM research checkpoint and presentation seed.

Do not claim validated 3D GPR-BEM, layered GPR readiness, field readiness, or
BEM-FWI readiness from the current evidence.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_bem_research_track_checkpoint_pack.py
python -m py_compile run_bem_research_track_checkpoint_pack.py
conda run -n gpr-fdtd-fwi python run_bem_research_track_checkpoint_pack.py --outdir outputs/bem_experiments/008_bem_research_track_checkpoint_pack
```

## Next Action

Receive/import the colleague's verified 2D GPR-BEM code, reproduce its known
cases, and define a shared BEM/FDTD comparison problem that avoids mixing a 3D
finite-cylinder BEM result with a 2D TMz FDTD sanity result.
