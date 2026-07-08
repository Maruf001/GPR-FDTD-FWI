# BEM Experiment 116: Fine-Mesh Import Template Smoke

Date: 2026-06-27

## Purpose

Check that the run `115` preferred nine-bin target/background FDTD import
templates behave correctly when blank and when synthetically filled.

The blank templates should be blocked because no real FDTD complex field values
are present. A synthetically filled copy should pass schema, receiver/frequency
key, receiver-position, and finite-component checks. This proves the template
surface is executable without claiming that any real FDTD data exist.

This run does not launch FDTD, install real returned files, perform BEM/FDTD
comparison, make a 3D validation claim, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/116_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_target_frequency_bin_import_template_smoke.csv
data/project_core_bem_3d_fdtd_fine_mesh_background_frequency_bin_import_template_smoke.csv
data/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.png
docs/PROJECT_CORE_BEM_3D_FDTD_FINE_MESH_FREQUENCY_BIN_IMPORT_TEMPLATE_SMOKE.md
scripts/run_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.py
scripts/test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                       9
receiver count:                        31
target template rows:                  279
background template rows:              279
target synthetic rows:                 279
background synthetic rows:             279
target blank component cells after fill:0
background blank component cells after fill:0
blank-template failed checks:          4
filled synthetic failed checks:        0
blank templates correctly blocked:     true
synthetic import smoke pass:           true
synthetic smoke only:                  true
real FDTD data ready:                  false
comparison ready:                      false
3D validation claim ready:             false
layered 3D GPR model ready:            false
field FWI ready:                       false
GPU/HPC ready:                         false
```

Scenario check counts:

| Scenario | Checks | Failed |
| --- | ---: | ---: |
| blank target template | 9 | 2 |
| blank background template | 9 | 2 |
| filled target synthetic | 9 | 0 |
| filled background synthetic | 9 | 0 |
| filled pair synthetic | 2 | 0 |

## Interpretation

The nine-bin template surface is behaving correctly. The blank target and
background templates fail because the complex field components are empty. After
deterministic synthetic values are inserted, both target and background files
pass all schema, key, receiver-position, and finite-component checks, and the
paired target/background keys match.

This is synthetic schema evidence only. It proves the import surface is usable,
not that any real FDTD validation has happened.

## Decision

Use run `116` as the smoke companion to the run `115` nine-bin templates.

Keep BEM/FDTD comparison, 3D validation, local 3D FDTD launch, and GPU/HPC work
blocked until actual paired FDTD target/background outputs fill the same
templates and pass the return gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.py
sha256: 4abab0e68f1c572b88140892033ac1dd128cd86dae595ca8acd410ca431f2828

test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.py
sha256: 9adf119ee6ae58af18e7fb1c750303d9669b418ec740132b821f9e57a3dd3036
```

Subsequent related BEM 3D return-intake experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_fine_mesh_frequency_bin_import_template_smoke.png
2248x850, dynamic range=255
```
