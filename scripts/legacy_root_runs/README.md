# Legacy Root Runner Scripts

This folder holds one-off `run_*.py` scripts that previously lived in the repository root.

These scripts are mostly experiment launchers, audit/report builders, and historical reproducibility handles. They are not the reusable library surface of the project.

Use this layout going forward:

- `scripts/legacy_root_runs/field_inversion/` - field-data, GSSI51600S, Jazayeri/GGAE/FastGPR-style runners.
- `scripts/legacy_root_runs/bem_fdtd/` - BEM/FDTD bridge and comparison runners.
- `scripts/legacy_root_runs/legacy_2d/` - older 2D/synthetic/local detector runners.
- `scripts/legacy_root_runs/reports_handoff/` - advisor, milestone, handoff, and report-generation runners.
- `scripts/legacy_root_runs/misc/` - small legacy entrypoints that do not fit the above groups.

New reusable code should go under the project modules (`core/`, `inversion/`, `gpu/`, `visualization/`, `tools/`) rather than creating another root-level runner.

New temporary/generated runner scripts should go under `local_run_scripts/`, which is ignored by Git.
