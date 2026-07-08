# Field Experiment 023: GSSI 51600S Field Dataset Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only synthesis of the current local GSSI 51600S field-data state. This
run consolidates the survey audit, all-profile network alignment, short-profile
stack, and long-profile stack into one field policy decision.

It does not run FDTD, FWI, or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/023_gssi51600s_field_dataset_policy_synthesis
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
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Decision:

```text
The local GSSI 51600S dataset should be used as 2D line-profile QC and
timing/repeatability evidence only. The short pair 014/016 is the strongest
repeat/timing anchor; the long pair 015/013 is pattern-only because 013 lacks
phase-anchor picks. The survey audit still lacks recoverable crossline/grid
metadata, so the dataset is not a 3D survey or measured-data FWI benchmark.
```

Evidence table:

| Evidence | Status | Key metric | Limitation |
| --- | --- | ---: | --- |
| Survey geometry | `independent_2d_line_profiles` | 4 profiles | no GPS/grid/crossline metadata |
| Profile network | repeat candidates = 2 | embedded candidates = 0 | no recoverable 3D layout |
| Short pair 014/016 | `repeat_stack_limited_qc` | corr = 0.9312, event pairs = 3 | radius matches = 0/3 |
| Long pair 015/013 | `long_repeat_stack_pattern_only_qc` | corr = 0.7244, stable anchors = 6 | 013 has no phase-anchor picks |

## Interpretation

This synthesis answers the current field-data scope question. The field data
is not a 3D survey, and it is not ready for field FWI claims. It is useful as
measured-data QC evidence:

```text
014/016: strongest repeat/timing QC pair.
015/013: long-profile pattern repeat only.
All four files: separate 2D line profiles, not a recovered 3D grid.
```

The field stream should remain separate from synthetic 2D experiment trackers.
Future field work needs external survey layout or target metadata before
geometry, radius, cover-depth, 3D, or FWI claims are defensible.

## Validation

Focused synthesis tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py: included in 4 passed
tests/test_gssi_field_long_profile_stack_policy.py: included in 4 passed
```

The policy figure was validated as nonblank:

```text
field_dataset_policy.png nonwhite=0.3763, dynamic range=255
```
