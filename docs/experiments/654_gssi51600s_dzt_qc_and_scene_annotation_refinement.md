# Experiment 654: GSSI 51600S DZT QC And Scene Annotation Refinement

## Purpose

Install the DZT reader in the FNO environment, run the first CPU-only QC pass
on the local GSSI 51600S reinforced-concrete data, and refine the reusable
system-scene visualization script based on visual review.

This is not a GPU FWI run and does not claim a 3D inversion result.

## Environment Update

Installed `readgssi` in the FNO conda environment:

```text
readgssi 0.0.22
```

The package imports successfully from:

```text
/home/lam001/miniforge3/envs/FNO/bin/python
```

The reproducibility dependency was also recorded in:

```text
requirements.txt
```

## Implementation

Added a CPU-only field-data QC wrapper:

```text
run_gssi_dzt_qc.py
```

It reads local `.DZT` files through `readgssi`, parses `.DZX` sidecars with a
namespace-safe XML parser, records SHA-256 hashes, writes CSV/JSON inventory
artifacts, and creates validated QC figures.

Added an optional field-data dependency spec:

```text
requirements-field-data.txt
```

This keeps the base synthetic workflow requirements unchanged while documenting
the `readgssi==0.0.22` dependency needed for GSSI DZT import.

Added tests:

```text
tests/test_gssi_dzt_qc.py
```

Refined the scene visualization template:

```text
run_experiment_scene_visualization.py
```

Changes:

- The cover arrow now measures from the concrete surface to the bar top rather
  than to the rebar center.
- The cover label now says `bar-top cover`.
- A representative Tx-Rx pair gets a visible double-arrow callout with the
  numeric offset.
- The cover annotation is placed on the clearer side of the selected target.

## Output

New field-data QC output:

```text
outputs/experiments/1119_gssi51600s_dzt_qc
```

Key artifacts:

```text
data/gssi_dzt_inventory.csv
data/gssi_dzt_qc_summary.json
figures/field_profile_qc_context.png
figures/gssi_dzt_inventory.png
figures/PROJECT001C__013_ch0_bscan_qc.png
figures/PROJECT001C__014_ch0_bscan_qc.png
figures/PROJECT001C__015_ch0_bscan_qc.png
figures/PROJECT001C__016_ch0_bscan_qc.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Imported profile/channel records:

```text
PROJECT001C__013.DZT ch0: 807 traces x 510 samples, 2.686398 m
PROJECT001C__014.DZT ch0: 274 traces x 510 samples, 0.909909 m
PROJECT001C__015.DZT ch0: 814 traces x 510 samples, 2.709729 m
PROJECT001C__016.DZT ch0: 274 traces x 510 samples, 0.910000 m, missing DZX sidecar
```

Common header metadata:

```text
antenna: 51600S
frequency: 1600 MHz
time range: 5 ns
header dielectric: 2.25
header depth: 0.5 m
readgssi-trimmed samples: 510
```

The three available DZX sidecars report:

```text
system: SIR4K
softwareVersion: 1.4.35
scanPerMeters: 300
unitsPerScan: 0.003333 m
depthRange: 0.45 m
samplesPerScan: 512
```

## Backfilled Scene Figures

Regenerated the improved scene geometry figure and summary for:

```text
outputs/experiments/1115_coordinate_optimizer_variable_depth_radius_seed139583862445_target1_sources9_txrx60_ringdown050_objectives
outputs/experiments/1116_coordinate_optimizer_variable_depth_radius_seed225851433717_target0_sources8_txrx60_ringdown050_objectives
outputs/experiments/1117_coordinate_optimizer_variable_depth_radius_seed225851433717_target2_sources5_txrx60_ringdown050_objectives
outputs/experiments/1118_coordinate_optimizer_variable_depth_radius_seed225851433717_target1_sources5_txrx60_ringdown050_objectives
```

The regenerated 1115 figure was visually checked and shows both the corrected
bar-top cover callout and the Tx-Rx offset callout.

## Interpretation

The measured data should not be treated as a direct replacement for the current
2D synthetic benchmark. The DZT files are profile/B-scan records. A full 3D
survey interpretation would require crossline geometry, line ordering, antenna
pose, calibration targets or independent cover/velocity information, and a 3D
forward/inversion path.

The useful bridge right now is profile-level QC and calibration:

1. Keep the 1119 output as the field-data intake baseline.
2. Pick visible hyperbolas or known-depth features to estimate velocity and
   effective dielectric.
3. Build 2D or 2.5D synthetic profile comparisons only after velocity/cover
   calibration.
4. Defer full 3D FWI until a tiny 3D synthetic smoke test and field-data value
   case justify HPC time.

## Validation

```text
pytest -q tests/test_gssi_dzt_qc.py tests/test_experiment_scene_visualization.py
11 passed in 0.20s

py_compile run_gssi_dzt_qc.py run_experiment_scene_visualization.py
passed

run_gssi_dzt_qc.py
imported 4 DZT channel records and wrote validated figures under output 1119
```

## Next Decision

Do not start GPU FWI from the measured data yet. Use the field branch for
CPU-only QC, hyperbola/velocity picking, and acquisition-geometry clarification.
The next synthetic marathon, if continued, should resume with
seed365435296162 target0 using the now-improved scene figure generation.
