# BEM Experiment 380: Fine-Mesh Receiver-Aperture Sensitivity Audit

Date: 2026-06-29

## Purpose

Quantify whether the run `113` fine-mesh 3D Bempp receiver response can be
treated as a point-receiver response for future paired BEM/FDTD comparison.

This run reuses saved complex receiver fields from the 8x20 Bempp mesh over
nine frequencies. It does not run 3D FDTD, stage returned files, use field
data, run field FWI, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/380_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit_rows.csv
data/project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit_aperture_summary.csv
data/project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit_summary.json
figures/project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_RECEIVER_APERTURE_SENSITIVITY_AUDIT.md
scripts/run_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.py
scripts/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                              113
frequencies:                             9
receiver count per frequency:            31
aperture cases:                          5
aperture comparisons:                    45
point receiver exact pass:               true
max 3-sample relative L2:                0.08009547612144642
max 5-sample relative L2:                0.189423069968709
max 7-sample relative L2:                0.3151872365924616
max 9-sample relative L2:                0.44166920910128993
worst frequency:                         3.0 GHz
first aperture above 5%:                 3 samples, 10.666666666666657 mm
finite-aperture metadata required:       true
finite-aperture operator required:       true
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
```

## Interpretation

Finite receiver aperture is not a negligible detail for the fine-mesh Bempp
reference. Even the smallest non-point aperture tested changes the complex
scattered receiver line by more than 5% at the high-frequency end. Wider
apertures produce much larger changes, reaching 44.17% for the nine-sample
aperture.

## Decision

Future paired 3D BEM/FDTD returns must specify or match a receiver-aperture
operator before calibrated comparison. Point-receiver output remains useful as
a reference, but it is not an unconditional comparison convention.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_fine_mesh_receiver_aperture_sensitivity_audit.py
3 passed
```

Figure check:

```text
2536x1529, dynamic range=255
```
