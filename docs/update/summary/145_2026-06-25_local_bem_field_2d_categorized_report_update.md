# Local BEM Field 2D Categorized Report Update

Date: 2026-06-25

## Scope

This checkpoint records run `244`, a categorized report update that separates
the current BEM, field, local 2D, and cross-track evidence into distinct
folders under `outputs/summary_tables`.

No BEM/FDTD comparison, field FWI, local 3D FDTD launch, GPU/HPC work, source
factor full-batch run, or neural-network training was started.

## Output

```text
outputs/summary_tables/244_local_bem_field_2d_categorized_report_update
```

Category folders:

```text
outputs/summary_tables/244_local_bem_field_2d_categorized_report_update/bem
outputs/summary_tables/244_local_bem_field_2d_categorized_report_update/field
outputs/summary_tables/244_local_bem_field_2d_categorized_report_update/local_2d
outputs/summary_tables/244_local_bem_field_2d_categorized_report_update/cross_track
```

## Result

```text
categories:                    4
report items:                  7
BEM report items:              2
field report items:            1
local 2D report items:         2
cross-track report items:      2
handoff-ready items:           7
compute/claim-ready items:     0
compute/claim-blocked items:   5
broad compute ready:           false
GPU work ready:                false
field transfer ready:          false
```

Category contents:

| Category | Contents |
| --- | --- |
| `bem` | return-inbox preflight and synthetic preflight smoke |
| `field` | controlled collection bundle unpack smoke |
| `local_2d` | neighbor-state mechanism and state-consistency guard |
| `cross_track` | handoff scoreboard and snapshot policy |

## Decision

Use run `244` as the current team-facing categorized report update. Keep BEM
3D validation, field FWI/GPU/3D, and local 2D source-factor full-batch/GPU work
blocked until their category-specific gates pass.

## Milestone Snapshot

This result-driven report froze:

```text
run_local_bem_field_2d_categorized_report_update.py
sha256: 8488e26b787c77c20a7bd9060de0ae130b77a8cf2a00cb1fa273dada855f5337

test_local_bem_field_2d_categorized_report_update.py
sha256: 23ef622bf52318da077f24b349e91176a29e97286afab3ea66ef72ddd1d52c79
```

## Validation

Focused test:

```text
tests/test_local_bem_field_2d_categorized_report_update.py
2 passed
```

Compile check:

```text
run_local_bem_field_2d_categorized_report_update.py: pass
tests/test_local_bem_field_2d_categorized_report_update.py: pass
```

Figure checks:

```text
top-level figure: 1924x738, dynamic range=255
BEM figure:       1205x696, dynamic range=255
field figure:     1205x696, dynamic range=255
local 2D figure:  1205x699, dynamic range=255
cross-track:      1205x698, dynamic range=255
```

## Marathon State

The requested autonomous marathon is still active. This report update is a
checkpoint, not a stop condition. Continue with snapshot refresh and focused
validation.
