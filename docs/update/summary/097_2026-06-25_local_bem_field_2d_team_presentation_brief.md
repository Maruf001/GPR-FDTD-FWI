# Local BEM Field 2D Team Presentation Brief

Date: 2026-06-25

## Scope

This checkpoint records output `200`, a slide-ready team brief built from the
current BEM, field, local 2D, and snapshot-policy endpoints.

## Output

```text
outputs/summary_tables/200_local_bem_field_2d_team_presentation_brief
```

Key artifacts:

```text
data/local_bem_field_2d_team_presentation_claims.csv
data/local_bem_field_2d_team_presentation_slides.csv
data/local_bem_field_2d_team_presentation_brief_summary.json
docs/LOCAL_BEM_FIELD_2D_TEAM_PRESENTATION_BRIEF.md
figures/local_bem_field_2d_team_presentation_brief.png
scripts/run_local_bem_field_2d_team_presentation_brief.py
scripts/test_local_bem_field_2d_team_presentation_brief.py
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                    4
slides:                    6
handoff-ready claims:      2
blocked compute claims:    3
snapshot policy ready:     true
presentation ready:        true
new compute ready:         false
```

Claims:

| Claim | Status | Evidence |
| --- | --- | --- |
| BEM 3D handoff | ready handoff, blocked validation | run `102` |
| Field collection | ready handoff, blocked FWI | field run `178` |
| Local 2D source factor | bounded evidence, no full batch | run `194` |
| Snapshot policy | pass | run `199` |

## Decision

Use this brief for the team discussion. Keep BEM 3D validation, field
FWI/GPU/3D, and source-factor full-batch runs blocked until their gates are
satisfied.

## Milestone Snapshot

This milestone froze:

```text
run_local_bem_field_2d_team_presentation_brief.py
sha256: 02decaa258d06b7e77681ebdd8bb608226d779de5d33725ef6fe662038de6eab

test_local_bem_field_2d_team_presentation_brief.py
sha256: b595b9be87f2f6f311ba7b67cb6cc3b191328bd73a1cbf61fbb6939063481046
```

## Validation

Focused tests:

```text
tests/test_local_bem_field_2d_team_presentation_brief.py
4 passed
```

Figure check:

```text
local_bem_field_2d_team_presentation_brief.png
1636x738, dynamic range=255
```

Marathon status: active. The next useful branch is snapshot-policy refresh and
then another bounded readiness/reporting improvement.
