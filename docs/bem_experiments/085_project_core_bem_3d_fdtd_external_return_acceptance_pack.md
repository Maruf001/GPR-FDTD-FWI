# BEM Experiment 085: External 3D FDTD Return Acceptance Pack

Date: 2026-06-25

## Purpose

Turn the external 3D FDTD return gate from run `084` into an operator-facing
acceptance handoff.

This run answers the practical question:

```text
When the external full-Maxwell 3D FDTD target/background files arrive, exactly
what files, metadata, commands, and gates are required before comparison?
```

This is a CPU-only packaging run. It does not launch 3D FDTD, run the real
BEM/FDTD comparator, field FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/085_project_core_bem_3d_fdtd_external_return_acceptance_pack
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_required_files.csv
data/project_core_bem_3d_fdtd_external_return_metadata_requirements.csv
data/project_core_bem_3d_fdtd_external_return_acceptance_steps.csv
data/project_core_bem_3d_fdtd_external_return_gate_crosswalk.csv
data/project_core_bem_3d_fdtd_external_return_acceptance_pack_summary.json
figures/project_core_bem_3d_fdtd_external_return_acceptance_pack.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_ACCEPTANCE_PACK.md
scripts/run_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
scripts/test_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required return files:              2
current required files present:     0
metadata requirements:              12
acceptance steps:                   8
gate crosswalk rows:                8
expected rows per FDTD run:         124
expected total frequency rows:      248
ready to accept external return:    true
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
```

The two required returned files are:

```text
project_core_bem_3d_fdtd_target_frequency_bins.csv
project_core_bem_3d_fdtd_background_frequency_bins.csv
```

Each file must contain 124 frequency-bin rows using the exact run `075`
frequency-bin schema. The pair must therefore provide 248 total rows before
any real BEM/FDTD comparison can run.

## Interpretation

The external-return handoff is now unambiguous. A collaborator or external
solver path can return two CSV files plus metadata, copy them into the pending
return folder, and rerun run `084` as the acceptance gate.

The current pending return is still empty. This run is readiness for intake,
not real returned data and not 3D validation.

## Decision

Use run `085` as the external-return handoff checklist. Do not run or report a
real BEM/FDTD 3D comparison until run `084` passes on the returned files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_external_return_acceptance_pack.py
4 passed
```

Compile check:

```text
run_project_core_bem_3d_fdtd_external_return_acceptance_pack.py: pass
tests/test_project_core_bem_3d_fdtd_external_return_acceptance_pack.py: pass
```

Figure check:

```text
1996x772, dynamic range=255
```
