# Advisor Optimizer Script Bundle

Source repo: `/home/lam002/Documents/GPR-FDTD-FWI`
Bundle date: 2026-07-01

This folder contains the key optimizer and inversion scripts copied from the
working repository, with the local source modules needed to read or run the
main workflows. Large generated outputs, notebooks, and experiment archives are
intentionally excluded.

## Main Entry Points

- `run_multi_rebar_coordinate_optimizer.py` - reporting-first multi-rebar
  coordinate/radius optimizer.
- `run_single_rebar_inversion.py` - single-rebar geometry inversion pipeline.
- `run_inversion.py` - original geometry and pixel FWI entry point.
- `run_gssi_field_inversion_blocker_map.py` - field-data inversion blocker map.
- `run_gssi_field_inversion_readiness_synthesis.py` - field inversion readiness
  synthesis.

## Core Optimizer Modules

- `inversion/optimizer.py` - steepest descent and L-BFGS-B optimizer routines.
- `inversion/multi_rebar_coordinate.py` - coordinate-state update and reporting
  helpers for multi-rebar optimization.
- `inversion/single_rebar_pipeline.py` - single-rebar objective and optimizer
  workflow.
- `inversion/geometry_inversion.py` - finite-difference geometry inversion.
- `inversion/inversion_engine.py` - pixel-wise FWI orchestration.
- `inversion/objective.py` and `inversion/objective_variants.py` - misfit and
  objective variants.
- `inversion/adjoint.py` and `inversion/regularization.py` - adjoint gradient
  and regularization support.

## Supporting Code Included

- `core/` - FDTD, geometry, source, scan, and output helpers needed by the
  optimizer workflows.
- `gpu/` - GPU FDTD helpers referenced by the inversion code.
- `visualization/` - plotting helpers used by the entrypoint scripts.
- `config.py`, `environment.yml`, `requirements.txt`, and `requirements-gpu.txt`
  for environment context.

## Example Commands

```bash
python run_single_rebar_inversion.py --sources 5 --max-evals 25
python run_inversion.py --method geometry --iterations 30 --sources 15
python run_multi_rebar_coordinate_optimizer.py --help
```

