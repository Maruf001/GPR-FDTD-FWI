# Team Meeting Evidence Brief

Date: 2026-06-25

## Scope

Create a compact meeting brief from the current decision anchors:

```text
BEM:       run 098 payload replacement contract
Local 2D:  run 147 source/time-zero robustness gate
Field:     run 176 real-archive acceptance contract
Report:    run 148 presentation evidence pack
```

This is a presentation artifact. It does not change gates or launch compute.

## Output

```text
outputs/summary_tables/151_team_meeting_evidence_brief
```

Key artifacts:

```text
data/team_meeting_evidence_brief.csv
data/team_meeting_evidence_brief_summary.json
figures/team_meeting_evidence_brief.png
docs/TEAM_MEETING_EVIDENCE_BRIEF.md
scripts/run_team_meeting_evidence_brief.py
scripts/test_team_meeting_evidence_brief.py
scripts/script_snapshot_manifest.json
```

## Result

```text
brief items:                 4
ready scoped items:          2
blocked or mixed items:      3
heavy compute ready:         false
field FWI ready:             false
GPU work ready:              false
field 3D/HPC ready:          false
```

Meeting anchors:

| Track | Status | Main message |
| --- | --- | --- |
| BEM | scoped_ready | Payload-based BEM replacement is ready inside scoped homogeneous/layered local 2D gates. |
| Local 2D | mixed_blocks_general_claim | Close14-like source/time-zero robustness passes, but broad variable-radius robustness is blocked. |
| Field | operational_contract_blocked_until_real_archive | Field process is designed, but real archive acceptance is false. |
| Presentation | ready_with_blocked_no_go_claims | Use the pack with eight blocked claims explicit. |

## Decision

Use this as the compact team-meeting brief. Decision requests should focus on
real field collection, paired 3D FDTD data, or presentation/report packaging
around scoped claims.

## Validation

Focused tests:

```text
tests/test_team_meeting_evidence_brief.py
2 passed
```

Figure check:

```text
1565x774, dynamic range=255
```

Script snapshots:

```text
run_team_meeting_evidence_brief.py
sha256=b45481559eabc70051c8f7b0616e99f5c2c60c32c74611d16e255ce7a49def2b

test_team_meeting_evidence_brief.py
sha256=c011a3e3033ad57d993636e26efa980d328294ccbf32ef0d020fd9fb856f4a8d
```

## Next Marathon Branch

The marathon remains active. The next useful work is to validate this final
reporting increment, then either refresh the snapshot audit again or continue
with a bounded BEM/field/local-2D improvement branch.
