# Experiment 653: Scene Visualization Template And GSSI Field-Data Intake

## Purpose

Restore the system-visualization discipline used in earlier single-rebar
experiments and prepare a cautious intake plan for the new real GSSI 51600S
reinforced-concrete data under:

```text
data/2026-06-09_GSSI_model_51600S
```

This is a CPU-only implementation and planning checkpoint. No new GPU FDTD
experiment was launched.

## Implementation

Added a reusable scene/context visualization script:

```text
run_experiment_scene_visualization.py
```

The script can read a coordinate-optimizer summary or explicit geometry lists
and writes:

```text
figures/system_scene_geometry.png
data/system_scene_geometry_summary.json
```

It also updates `figures/FIGURE_NOTES.md` with an idempotent scene-geometry
section. The figure shows the x-z cross-section, concrete surface, Tx/Rx
aperture, true rebar locations, selected/final rebar locations, and highlighted
target rebar.

The coordinate optimizer now calls this scene writer automatically for future
runs, so upcoming optimizer experiments will not depend on manual scene-figure
backfills.

## Backfilled Artifacts

The new scene figure was generated for the latest seed225851433717 runs:

```text
outputs/experiments/1116_coordinate_optimizer_variable_depth_radius_seed225851433717_target0_sources8_txrx60_ringdown050_objectives/figures/system_scene_geometry.png
outputs/experiments/1117_coordinate_optimizer_variable_depth_radius_seed225851433717_target2_sources5_txrx60_ringdown050_objectives/figures/system_scene_geometry.png
outputs/experiments/1118_coordinate_optimizer_variable_depth_radius_seed225851433717_target1_sources5_txrx60_ringdown050_objectives/figures/system_scene_geometry.png
```

Validation:

```text
1116 system_scene_geometry.png: 1569x1029 RGB, nonwhite_fraction=0.7295, unique_colors=1656
1117 system_scene_geometry.png: 1569x1029 RGB, nonwhite_fraction=0.7294, unique_colors=1638
1118 system_scene_geometry.png: 1569x1029 RGB, nonwhite_fraction=0.7294, unique_colors=1646
```

Trackers 650-652 were updated to include the scene figure validation and the
system-scene section in their figure notes.

## GSSI 51600S Data Inventory

Local files:

```text
PROJECT001C__013.DZT  1,783,808 bytes
PROJECT001C__013.DZX      2,279 bytes
PROJECT001C__014.DZT    692,224 bytes
PROJECT001C__014.DZX      2,279 bytes
PROJECT001C__015.DZT  1,798,144 bytes
PROJECT001C__015.DZX      2,279 bytes
PROJECT001C__016.DZT    692,224 bytes
```

The DZX sidecar is missing for `PROJECT001C__016.DZT`.

Parsed DZX metadata for files 013-015:

```text
system: SIR4K
softwareVersion: 1.4.35
dielectric/originalDielectric: 2.25
scanPerMeters: 300
unitsPerScan: 0.003333 m
depthRange: 0.45 m
samplesPerScan: 512
antenna serial: 3385
antenna model number: 70
scanRate: 333
transmitRate: 500
surfacePct: 10
scan ranges:
  PROJECT001C__013: 0-806
  PROJECT001C__014: 0-273
  PROJECT001C__015: 0-813
```

`readgssi` is not installed in the active FNO environment, so DZT import is
not yet available through that package.

## External Research Notes

Official GSSI sources identify the 51600S as a 1600 MHz concrete antenna with
about 0-18 inch / 0-50 cm stated depth range depending on concrete. The GSSI
RADAN material describes `.DZT` as the raw GPR profile and `.DZX` as the
sidecar carrying processing/user-mark information. The open-source `readgssi`
documentation treats DZT as GSSI's native binary data format and provides a
reasonable candidate reader/import path.

References used:

```text
https://www.geophysical.com/wp-content/uploads/2017/10/GSSI-Antenna-Manual.pdf
https://www.geophysical.com/antennas
https://www.geophysical.com/gssi-academy-getting-started-with-radan-7
https://readgssi.readthedocs.io/
https://readgssi.readthedocs.io/en/latest/translating.html
```

## Interpretation

The scene template should be part of every future optimizer run. Wavefield
animations should still be generated when they explain a physical ambiguity,
candidate confusion, or a representative propagation state; they should not be
forced onto every cheap reporting run.

The real GSSI data are useful, but they should enter as a separate field-data
branch rather than being mixed directly into the current synthetic confidence
chain. The DZX dielectric value of 2.25 should be treated as acquisition/display
metadata until velocity is calibrated from hyperbolas, known cover, slab
geometry, or independent material knowledge. Directly replacing the synthetic
concrete dielectric with 2.25 would be an unjustified shortcut.

## Field-Data Plan

1. Add a GSSI intake/QC script that inventories `.DZT`/`.DZX` pairs, parses DZX
   XML metadata, flags missing sidecars, and records file hashes.
2. Add or vendor a tested DZT reader. Prefer `readgssi` if compatible with the
   environment; otherwise implement a minimal read-only parser against the GSSI
   DZT header documentation and test it on these files.
3. Generate raw B-scan QC figures for each profile: raw amplitude image,
   time-zero/surface estimate, per-trace amplitude statistics, and a metadata
   panel.
4. Estimate field velocity/dielectric from observed hyperbola curvature and/or
   known cover before any FWI comparison. Keep the DZX dielectric as metadata,
   not as truth.
5. Build a field-data synthetic bridge: 1.6 GHz source family, 3.333 mm scan
   spacing, 512 sample display/QC scale, realistic antenna offset/standoff, and
   concrete depth up to 450 mm.
6. Only after B-scan QC and velocity calibration, compare synthetic and field
   profiles with the current objective diagnostics. Treat disagreement as a
   modeling gap first, not as an optimizer failure.

## Validation

```text
pytest: tests/test_experiment_scene_visualization.py and tests/test_multi_rebar_coordinate_optimizer.py pass
py_compile: run_experiment_scene_visualization.py and run_multi_rebar_coordinate_optimizer.py pass
figure validation: backfilled scene figures for runs 1116-1118 are nonblank and readable
DZX parse: files 013-015 parse as XML; file 016 has no DZX sidecar
```

## Next Decision

Before the next long GPU marathon, run one short CPU-only GSSI intake/QC stage
to make raw B-scan figures and metadata tables. Continue synthetic Fibonacci
replication only after the archive has the scene figure generated automatically
for the next optimizer run.
