# Presentation Evidence Pack: Matched Source Refresh

Date: 2026-06-25

## Scope

This checkpoint records presentation outputs `162` and `163`, refreshed after
the matched local 2D source/time-zero factorization and robustness gate in runs
`159-160`.

No gate was relaxed. No new FDTD, GPU work, field transfer, field FWI, 3D/HPC,
or neural-network training was launched.

## Outputs

Evidence pack:

```text
outputs/summary_tables/162_bem_field_2d_presentation_evidence_pack_matched_source_refresh
```

Storyboard:

```text
outputs/summary_tables/163_bem_field_2d_presentation_storyboard_matched_source_refresh
```

## Result

Evidence pack:

```text
claims:                         48
ready scoped claims:            40
blocked claims:                 8
BEM 3D decision ready:          true
time-zero-only explanation:     false
snapshot policy pass:           true
GPU or field FWI ready:         false
```

Storyboard:

```text
slides:                         9
tracks:                         8
blocked claims preserved:       8
ready claims referenced:        40
GPU/FWI/3D launch ready:        false
```

## Interpretation

The presentation layer now carries the corrected local 2D source message:

```text
The matched close14-like and stable/control cases pass. Broad variable-radius
source robustness remains blocked. The driver is not time-zero alone.
```

The pack still keeps the BEM and field boundaries unchanged: BEM 3D is
request-ready but validation-blocked, and the field side remains blocked until
real archive acceptance passes.

## Milestone Snapshots

Output `162` froze:

```text
run_bem_field_2d_presentation_evidence_pack_matched_source_refresh.py
sha256: cf9b5afdd443fa1ce364a6a527a0b9f907a182cc167e5d5ed9022246d6afa51f

test_bem_field_2d_presentation_matched_source_refresh.py
sha256: b61e5f3fca7304a5984a851ed06c62a7b272e18eb56d3aec37dddffa254e79b1
```

Output `163` froze:

```text
run_bem_field_2d_presentation_storyboard_matched_source_refresh.py
sha256: f78969a206d303db64727a8577b3c3e06d233de3b4625a726fa83a1fe741b3c3

test_bem_field_2d_presentation_matched_source_refresh.py
sha256: b61e5f3fca7304a5984a851ed06c62a7b272e18eb56d3aec37dddffa254e79b1
```

## Validation

Focused tests:

```text
tests/test_bem_field_2d_presentation_matched_source_refresh.py
2 passed
```

Figure checks:

```text
bem_field_2d_presentation_evidence_status.png
2052x954, dynamic range=255

bem_field_2d_presentation_storyboard.png
2286x851, dynamic range=255
```

Marathon status: active. The next defensible branch is to add outputs
`159-163` to the result-milestone snapshot audit.
