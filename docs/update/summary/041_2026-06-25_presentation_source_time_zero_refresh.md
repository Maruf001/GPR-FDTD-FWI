# Presentation Source/Time-Zero Refresh

Date: 2026-06-25

## Scope

Refresh the BEM, field, and local 2D presentation materials after the run `147`
source/time-zero robustness gate.

This is a report/presentation artifact. It does not change compute gates and
does not launch FDTD, FWI, GPU work, field 3D/HPC, or neural-network training.

## Outputs

Evidence pack:

```text
outputs/summary_tables/148_bem_field_2d_presentation_evidence_pack_source_time_zero_refresh
```

Storyboard:

```text
outputs/summary_tables/149_bem_field_2d_presentation_storyboard_source_time_zero_refresh
```

## Result

Evidence pack:

```text
claim count:                  45
ready scoped/operational:     37
blocked claims:               8
gpu or field FWI ready:       false
```

The new blocked claim is:

```text
claim:         source/time-zero robustness gate
status:        blocked_general_claim
evidence:      summary run 147 / docs experiment 878
metric:        2 blocked sensitive cases
ready value:   false
```

Storyboard:

```text
slide count:                  8
tracks covered:               7
blocked claims preserved:     8
ready claims referenced:      37
gpu/fwi/3d launch ready:      false
source pack:                  148
```

## Interpretation

The presentation state now includes the current local 2D robustness boundary:
the close14-like case passes source/time-zero robustness, but broad
variable-radius cases are sensitive and block any general source/time-zero
robustness claim.

## Decision

Use outputs `148` and `149` for the current team-presentation planning state.
Keep the no-go claims explicit: no general source/time-zero robustness claim,
no measured-field claim, no field FWI, no heavy GPU work, no field 3D/HPC, and
no 3D validation claim follows from the current evidence.

## Validation

Focused tests:

```text
tests/test_bem_field_2d_presentation_source_time_zero_refresh.py
2 passed
```

Compile check:

```text
run_bem_field_2d_presentation_evidence_pack_source_time_zero_refresh.py: pass
run_bem_field_2d_presentation_storyboard_source_time_zero_refresh.py: pass
tests/test_bem_field_2d_presentation_source_time_zero_refresh.py: pass
```

Figure checks:

```text
148 evidence figure: 2052x954, dynamic range=255
149 storyboard figure: 2286x851, dynamic range=255
```

Script snapshots:

```text
run_bem_field_2d_presentation_evidence_pack_source_time_zero_refresh.py
sha256=865681252f11de65ea9c91de9037af797025931f8e768f9aa3aba89910b52c8e

run_bem_field_2d_presentation_storyboard_source_time_zero_refresh.py
sha256=2e303a1e00a5287b2f4905db4246c6eed0ae17ab00340b59b1eebc9100a7c8a9
```

## Next Marathon Branch

The marathon remains active. The next useful branch is to refresh the
milestone snapshot audit so it includes the newer source/time-zero and
presentation milestones.
