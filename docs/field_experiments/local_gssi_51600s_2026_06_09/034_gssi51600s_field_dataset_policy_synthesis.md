# Field Experiment 034: GSSI 51600S Dataset Policy Through Content-Synthetic QC

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the content-backed
field-to-synthetic waveform QC in field experiment 033.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/034_gssi51600s_field_dataset_policy_synthesis
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
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Key evidence:

| Evidence | Status | Key metric | Limitation |
| --- | --- | ---: | --- |
| Survey geometry | `independent_2d_line_profiles` | 4 profiles | no recoverable grid/crossline metadata |
| Profile network | repeat candidates = 2 | strongest corr = 0.9312 | not a 3D survey |
| Short pair 014/016 | `repeat_stack_limited_qc` | corr = 0.9312, pairs = 3 | radius matches = 0/3 |
| Short time-zero transfer | `relative_time_zero_transfer_limited_qc` | offset = 0.127701 ns | not absolute time zero |
| Applied short time-zero | `applied_relative_time_zero_transfer_qc` | residual reduction = 6.000x | no geometry/radius/depth claim |
| Phase-convention transfer | `multi_phase_relative_time_zero_supported_qc` | stable conventions = 4/6 | relative timing QC only |
| Timing bootstrap | `bootstrap_relative_time_zero_supported_qc` | median = 0.117878 ns, CI envelope = 0.108055-0.147348 ns | relative timing QC only |
| Content windows | `repeat_content_windows_limited_qc` | content-backed events = 2/3 | content QC only |
| Content-synthetic waveform QC | `content_backed_field_to_synthetic_qc_supported` | content-supported = 2/2, min corr = 0.8195 | visual QC only |
| Long pair 015/013 | `long_repeat_stack_pattern_only_qc` | corr = 0.7244 | 013 has no phase-anchor picks |

## Interpretation

The field-data policy is now current through experiment 033. The strongest
measured-data path is:

```text
014/016 repeat profile pair
relative timing supported across stable phase conventions and bootstrap resampling
two repeat-content anchors
both repeat-content anchors supported by field-to-synthetic waveform candidates
```

This supports using event pairs 2 and 3 as measured-data examples in future
visual field-to-synthetic figures. It does not turn the local GSSI dataset into
a field inversion benchmark: the data remain separate 2D line profiles with no
recoverable 3D grid/crossline metadata, and no field radius, cover-depth,
geometry, 3D, or FWI claim is supported.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py
tests/test_gssi_field_short_profile_content_synthetic_policy.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png nonwhite=0.2732, dynamic range=255
```
