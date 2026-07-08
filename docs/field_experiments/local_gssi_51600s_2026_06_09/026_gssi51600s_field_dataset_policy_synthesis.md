# Field Experiment 026: GSSI 51600S Dataset Policy Synthesis Refresh

Date: 2026-06-17

## Purpose

CPU-only refresh of the local GSSI 51600S field-data policy after the relative
time-zero transfer and applied-transfer stress test in field experiments 024
and 025.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/026_gssi51600s_field_dataset_policy_synthesis
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
| Long pair 015/013 | `long_repeat_stack_pattern_only_qc` | corr = 0.7244 | 013 has no phase-anchor picks |

## Interpretation

The field-data boundary is now current through experiment 025:

```text
014/016: strongest repeatability and relative timing-QC pair.
015/013: long-profile pattern repeat only.
All four files: separate 2D line profiles, not a recovered 3D grid.
```

The applied relative transfer strengthens the field timing-QC claim, but it is
still not an absolute calibrated time zero. The local GSSI data remain useful
for measured-data QC and timing/repeatability support, not field FWI, field
radius/depth inversion, or 3D reconstruction claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py: included in 6 passed
```

The policy figure was validated as nonblank:

```text
field_dataset_policy.png nonwhite=0.3302, dynamic range=255
```
