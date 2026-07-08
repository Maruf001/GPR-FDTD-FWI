# BEM Experiment 113: Fine-Mesh Frequency-Grid Audit

Date: 2026-06-27

## Purpose

Repeat the full run `111` 0.4-3.0 GHz frequency grid on the finer 8x20
surface mesh selected by run `112`.

Run `111` showed that the 6x16 mesh produced finite BEM responses over the
full frequency grid. Run `112` then showed that the 6x16 mesh is not the safest
high-frequency reference because the 3.0 GHz 6x16-to-8x20 difference reaches
about 5.6%, while the 8x20-to-10x24 difference is below 1%.

This run answers the next practical question:

```text
Can the full frequency grid be evaluated on 8x20, and should 8x20 become the
BEM-side reference mesh for high-frequency comparison?
```

This run does not run 3D FDTD, validate against real FDTD returns, model
layered 3D GPR, use field data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/113_project_core_bem_bempp_fine_mesh_frequency_grid_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_frequency_grid_rows.csv
data/project_core_bem_bempp_fine_mesh_frequency_grid_receiver_rows.csv
data/project_core_bem_bempp_fine_mesh_frequency_grid_adjacent_comparison.csv
data/project_core_bem_bempp_fine_mesh_frequency_grid_mesh_comparison.csv
data/project_core_bem_bempp_fine_mesh_frequency_grid_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_frequency_grid_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FREQUENCY_GRID_AUDIT.md
scripts/run_project_core_bem_bempp_fine_mesh_frequency_grid_audit.py
scripts/test_project_core_bem_bempp_fine_mesh_frequency_grid_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
frequencies tested:                       9
receiver rows:                            279
adjacent frequency comparisons:           8
mesh comparisons versus 6x16 baseline:    9
finite frequencies:                       9
all frequencies finite:                   true
Bempp return code:                        0
max adjacent relative L2:                 3.364677384664746
max adjacent normalized shape L2:         0.06786245488660995
mean adjacent normalized shape L2:        0.02097388602986652
baseline-to-fine max relative L2:         0.055639649360411644
baseline-to-fine max shape L2:            0.008752001112977892
baseline-to-fine relative L2 at 3 GHz:    0.055639649360411644
baseline-to-fine shape L2 at 3 GHz:       0.008752001112977892
fine mesh frequency grid usable:          true
6x16 sufficient for full-grid reference:  false
8x20 recommended for high-frequency ref.: true
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
layered 3D GPR model ready:               false
field FWI ready:                          false
GPU/HPC ready:                            false
```

Baseline-to-fine mesh comparison:

| Frequency GHz | Relative L2 | Shape L2 | Peak ratio |
| ---: | ---: | ---: | ---: |
| 0.4 | 0.010573510005741023 | 0.000036744458635135796 | 0.9894117849058682 |
| 0.5 | 0.010296810068779048 | 0.000039659698122233445 | 0.9896898445636346 |
| 0.75 | 0.009156646658881511 | 0.00002809308903520839 | 0.9908598767781863 |
| 1.0 | 0.007425055149665965 | 0.00008020042357375972 | 0.9926541029505945 |
| 1.25 | 0.005199742413752004 | 0.0002006701982644101 | 0.9949981230429514 |
| 1.5 | 0.0037042675959667376 | 0.00036683620112687774 | 0.996662078315822 |
| 2.0 | 0.0012746072059177597 | 0.000949291809172839 | 1.000194412778324 |
| 2.5 | 0.0070932339277239055 | 0.002288571202184213 | 1.009640708824403 |
| 3.0 | 0.055639649360411644 | 0.008752001112977892 | 1.0624430903149282 |

## Interpretation

The full 0.4-3.0 GHz BEM frequency grid runs cleanly on the 8x20 fine mesh. All
nine frequency responses are finite and the receiver-line shape behavior stays
similar to run `111`.

The important result is the mesh comparison. The 6x16 and 8x20 responses are
close across most of the grid, but the high-frequency end is different. The
largest baseline-to-fine difference occurs at 3.0 GHz, where the relative L2 is
0.055639649360411644. That repeats the run `112` warning on the full grid:
6x16 is useful for fast convention and sensitivity work, but it should not be
the BEM-side reference mesh for high-frequency BEM/FDTD comparison.

The 8x20 fine mesh is now the safer BEM-side reference for future full-grid
frequency data, especially near 3.0 GHz.

## Decision

Use the 8x20 mesh for future 3D Bempp frequency-grid reference data.

Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR modeling, field
FWI, and GPU/HPC work blocked until real target/background FDTD returns pass
the upgraded metadata and frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_bempp_fine_mesh_frequency_grid_audit.py
sha256: a5cdef0ef662b15d9b6a2c4e527a57e3219bd4fa20aaf47a775662b47aadef01

test_project_core_bem_bempp_fine_mesh_frequency_grid_audit.py
sha256: 94d82b4fccfbe57bc8d65133eda33ccb4eaff696cb3122634afa9d8fd1d1aae3
```

Subsequent related BEM frequency-grid experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_frequency_grid_audit.py
3 passed
```

Figure check:

```text
project_core_bem_bempp_fine_mesh_frequency_grid_audit.png
2284x1493, dynamic range=255
```
