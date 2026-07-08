# BEM Experiment 388: 35-Field Real-Return Preflight Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `387` validator for the aperture-aware run `386`
BEM/FDTD real-return preflight.

## Output

```text
outputs/bem_experiments/388_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh_validation_sensitivity
```

## Result

```text
scenario count:                     14
expected pass count:                1
observed pass count:                1
expected failure count:             13
observed failure count:             13
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 386:    true
validator rejects damaged variants: true
real external FDTD data ready:      false
preflight ready:                    false
real comparison ready:              false
3D validation ready:                false
layered 3D model ready:             false
field FWI ready:                    false
GPU/HPC ready:                      false
```

The exact run `386` artifacts pass. Thirteen damaged variants fail as expected:
source identity drift, frequency-row count drift, metadata-count drift,
blocking-failure count drift, expected-file role drift, expected-file blocking
drift, preflight-row order drift, false preflight pass, missing-metadata count
drift, aperture-guard drift, downstream promotion, figure drift, and
script-snapshot drift.

## Interpretation

Runs `386-388` now form a guarded aperture-aware real-return preflight block.
The refreshed gate is ready as a handoff contract, but not as measured
comparison evidence. Real BEM/FDTD comparison remains blocked until the target,
background, and metadata return files exist and pass the gate.

## Decision

Use runs `386-388` as the current preferred BEM/FDTD real-return preflight
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_real_return_preflight_35field_aperture_refresh_validation_sensitivity.py
3 passed
```

Figure check:

```text
3437x922, dynamic range=255
```
