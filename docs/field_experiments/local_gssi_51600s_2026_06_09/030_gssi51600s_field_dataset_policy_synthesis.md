# Field Experiment 030: GSSI 51600S Dataset Policy Synthesis Through Bootstrap Timing

Date: 2026-06-17

## Purpose

CPU-only refresh of the local GSSI 51600S field-data policy after the
short-profile timing-bootstrap uncertainty analysis in field experiment 029.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/030_gssi51600s_field_dataset_policy_synthesis
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
| Profile network | repeat candidates = 2 | embedded candidates = 0 | not a 3D survey |
| Short pair 014/016 | `repeat_stack_limited_qc` | corr = 0.9312, pairs = 3 | radius matches = 0/3 |
| Short time-zero transfer | `relative_time_zero_transfer_limited_qc` | offset = 0.127701 ns | not absolute time zero |
| Applied short time-zero | `applied_relative_time_zero_transfer_qc` | residual reduction = 6.000x | no geometry/radius/depth claim |
| Phase-convention transfer | `multi_phase_relative_time_zero_supported_qc` | stable conventions = 4/6 | relative timing QC only |
| Timing bootstrap | `bootstrap_relative_time_zero_supported_qc` | median = 0.117878 ns, CI envelope = 0.108055-0.147348 ns | relative timing QC only |
| Long pair 015/013 | `long_repeat_stack_pattern_only_qc` | corr = 0.7244 | 013 has no phase-anchor picks |

## Interpretation

The field-data policy is now current through experiment 029:

```text
014/016: strongest repeatability and relative timing-QC pair.
014/016 timing delay is supported across stable phase conventions.
Bootstrap resampling keeps the delay positive and bounded away from zero.
015/013: long-profile pattern repeat only.
All four files: separate 2D line profiles, not a recovered 3D grid.
```

The bootstrap result strengthens the relative timing claim by showing that the
short-pair delay is not an artifact of a single event, phase convention, or
profile-pair sample. The result is still not an absolute calibrated time zero
and must not be used as field radius, cover-depth, geometry, 3D, or FWI
evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py: included in focused field validation
```

The policy figure was validated as nonblank:

```text
field_dataset_policy.png nonwhite=0.2742, dynamic range=255
```
