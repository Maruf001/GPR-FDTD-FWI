# Field Experiment 036: GSSI 51600S Dataset Policy Through Waveform Panels

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the content-backed waveform
panel reducer in field experiment 035.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/036_gssi51600s_field_dataset_policy_synthesis
```

Artifacts:

```text
data/field_dataset_policy_evidence.csv
data/field_dataset_policy_summary.json
data/figure_validation.csv
figures/field_dataset_policy.png
run_manifest.json
```

## Inputs

```text
015_gssi51600s_survey_geometry_audit
020_gssi51600s_profile_network_alignment
021_gssi51600s_short_profile_stack_policy
022_gssi51600s_long_profile_stack_policy
024_gssi51600s_short_profile_time_zero_transfer_policy
025_gssi51600s_short_profile_time_zero_application_policy
027_gssi51600s_short_profile_phase_convention_transfer_policy
029_gssi51600s_short_profile_timing_bootstrap_policy
031_gssi51600s_short_profile_content_window_policy
033_gssi51600s_short_profile_content_synthetic_policy
035_gssi51600s_content_backed_waveform_panels
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Key added evidence:

| Evidence | Status | Key metric | Limitation |
| --- | --- | ---: | --- |
| Content-backed waveform panels | `content_backed_waveform_visual_qc` | valid panels = 4/4, min corr = 0.8195 | visual QC only, no field inversion |

Current field-data statement:

```text
The 014/016 short-profile pair remains the strongest measured-data bridge.
The preferred measured-data figure endpoint is now the content-backed waveform
panel figure from experiment 035.
The dataset remains 2D line-profile calibration/QC evidence, not a measured
field inversion, 3D survey, or FWI benchmark.
```

## Interpretation

This refresh makes the dataset-level policy current through experiment 035. It
does not change the boundary: field evidence is useful for measured-data visual
QC and repeatability/timing support, but not for field radius, cover-depth,
geometry, 3D, or FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py
tests/test_gssi_field_content_backed_waveform_panels.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png nonwhite=0.2679, dynamic range=255
```
