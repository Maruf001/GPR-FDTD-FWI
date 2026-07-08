# Team Meeting Evidence Brief: BEM 3D Decision Refresh

Date: 2026-06-25

## Scope

This checkpoint records output `154`, a refreshed team-meeting evidence brief
that includes BEM run `099` and the refreshed milestone snapshot audit from
output `153`.

No gates were relaxed. No local 3D FDTD, GPU/HPC work, field FWI, or
neural-network training was launched.

## Output

```text
outputs/summary_tables/154_team_meeting_evidence_brief_bem3d_decision_refresh
```

Key artifacts:

```text
data/team_meeting_evidence_brief.csv
data/team_meeting_evidence_brief_summary.json
docs/TEAM_MEETING_EVIDENCE_BRIEF.md
figures/team_meeting_evidence_brief.png
scripts/run_team_meeting_evidence_brief_bem3d_decision_refresh.py
scripts/test_team_meeting_evidence_brief_bem3d_decision_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
brief items:                 6
ready scoped items:          3
blocked or mixed items:      4
heavy compute ready:         false
field FWI ready:             false
GPU work ready:              false
field 3D/HPC ready:          false
BEM 3D validation ready:     false
snapshot policy pass:        true
```

## Anchors

| Track | Anchor | Current message |
| --- | --- | --- |
| BEM | run `098` payload replacement contract | Scoped homogeneous/layered local 2D project-core payload replacement is ready. |
| BEM 3D | run `099` external-FDTD decision brief | External paired full-Maxwell FDTD request is ready, but 3D validation is not. |
| Local 2D | run `147` source/time-zero robustness gate | Close14-like case passes; broad variable-radius source/time-zero robustness is blocked. |
| Field | run `176` real-archive acceptance contract | Field process is operationally designed; real archive acceptance is false and nine real files are required. |
| Presentation | run `148` evidence pack | Presentation planning is ready with eight blocked claims preserved. |
| Process | run `153` milestone snapshot audit | Twenty-one major milestones and 38 frozen snapshots pass SHA validation. |

## Decision

Use this as the current compact team-discussion brief. The decision requests
should focus on:

```text
1. who owns paired 3D full-Maxwell FDTD target/background data generation,
2. whether real field collection can supply the nine required files,
3. how to present scoped BEM/local-2D progress without promoting blocked claims.
```

## Milestone Snapshot

This is a result-driven presentation/process milestone. The exact script and
focused test were frozen under the output-local `scripts/` folder:

```text
run_team_meeting_evidence_brief_bem3d_decision_refresh.py
sha256: 1f8070369d3132d95bd41e63cd9f9c95508ac4b0ae5cd9f008d05155a860e3aa

test_team_meeting_evidence_brief_bem3d_decision_refresh.py
sha256: 970e3b185e09f6367400752f414e4bdaaef492fe83f1900c154718861df496d3
```

Subsequent related presentation or brief refreshes should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_team_meeting_evidence_brief_bem3d_decision_refresh.py
2 passed
```

Figure check:

```text
team_meeting_evidence_brief.png
1565x774, dynamic range=255
```

Marathon status: active. The next defensible branch is either a presentation
evidence-pack refresh that absorbs run `099`/`154`, or a field-side intake
readiness improvement that reduces collection-day ambiguity.
