# Presentation Field-176 Refresh

Date: 2026-06-25

## Scope

Refresh the BEM, field, and local 2D presentation materials after the field
run `176` real-archive acceptance contract.

This is a report/presentation artifact. It does not change any scientific gate
and does not launch FDTD, FWI, GPU work, field 3D/HPC, or neural-network
training.

## Outputs

Evidence pack:

```text
outputs/summary_tables/139_bem_field_2d_presentation_evidence_pack_field176_refresh
```

Storyboard:

```text
outputs/summary_tables/140_bem_field_2d_presentation_storyboard_field176_refresh
```

## Result

Evidence pack:

```text
claim count:                  44
ready scoped/operational:     37
blocked claims:               7
gpu or field FWI ready:       false
```

The new claim is:

```text
claim:         real archive acceptance contract
status:        ready_contract_currently_failing
evidence:      field run 176
metric:        8 contract stages
ready value:   true
```

The no-go field claim now points to runs `163-176` and remains blocked:

```text
claim:         field FWI / heavy GPU / 3D escalation
ready value:   false
metric:        0 accepted measured field packets
```

Storyboard:

```text
slide count:                  8
tracks covered:               7
blocked claims preserved:     7
ready claims referenced:      37
gpu/fwi/3d launch ready:      false
source pack:                  139
```

The field slide now uses run `176` as the primary artifact:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/176_gssi51600s_controlled_collection_real_archive_acceptance_contract.md
```

## Interpretation

The presentation state is now aligned with the current evidence boundary:

```text
BEM:    payload-based local 2D homogeneous/layered path is scoped-ready.
Field:  real archive acceptance is operationally designed but currently false.
2D:     detector result remains a narrow mechanism result, not a GPU queue.
3D:     comparison path is designed, but real paired FDTD data are absent.
```

## Decision

Use outputs `139` and `140` for the next team-presentation planning checkpoint.
Keep the no-go claims explicit: no measured-field claim, field FWI, heavy GPU
work, field 3D/HPC, neural-network training, or 3D validation claim follows
from the current evidence.

## Validation

Focused tests:

```text
tests/test_bem_field_2d_presentation_field176_refresh.py
2 passed
```

Compile check:

```text
run_bem_field_2d_presentation_evidence_pack_field176_refresh.py: pass
run_bem_field_2d_presentation_storyboard_field176_refresh.py: pass
tests/test_bem_field_2d_presentation_field176_refresh.py: pass
```

Figure checks:

```text
139 evidence figure: 2052x954, dynamic range=255
140 storyboard figure: 2286x851, dynamic range=255
```

Script snapshots:

```text
run_bem_field_2d_presentation_evidence_pack_field176_refresh.py
sha256=b41aed2955a35783f89fdae01e256f0b2a172a0264e8e69daf2b4511f9334da1

run_bem_field_2d_presentation_storyboard_field176_refresh.py
sha256=2e428d09a4b23bac3f8263f35bd142df953056a800ec522e28e7f3793ffb1f08
```

## Next Marathon Branch

The marathon remains active. The next useful branch should either tighten local
2D hypothesis selection against the refreshed pack or add tooling that checks
script snapshots and major-result docs across the BEM, field, and summary-table
streams.
