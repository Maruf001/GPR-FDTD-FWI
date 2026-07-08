# Local BEM Field 2D Handoff Scoreboard: Full Suite 1345 Refresh

Date: 2026-06-25

## Scope

This checkpoint records summary run `214`, a refreshed cross-track readiness
scoreboard after the current full suite passed.

No BEM/FDTD comparison, field FWI, local 3D FDTD launch, GPU/HPC work, source
factor full-batch run, or neural-network training was started.

## Output

```text
outputs/summary_tables/214_local_bem_field_2d_handoff_readiness_scoreboard_full_suite_1345_refresh
```

## Result

```text
tracks:                         4
handoff-ready tracks:           4
compute/claim-ready tracks:     0
compute/claim-blocked tracks:   3
snapshot policy pass:           true
BEM real-return preflight:      false
BEM synthetic smoke passed:     true
field bundle unpack smoke:      true
BEM 3D validation ready:        false
field FWI ready:                false
source-factor full batch ready: false
full test suite:                1345 passed in 30.80 s
```

Current track endpoints:

| Track | Current artifact | Primary metric | Compute/claim ready |
| --- | --- | --- | --- |
| BEM 3D | runs `104`/`105` return-inbox preflight plus smoke | `17` real blockers; smoke `18/18` | false |
| Field | run `179` bundle unpack smoke | checksums `18/18` | false |
| Local 2D | run `194` source-factor x/z/radius decision boundary | update cases `2/2` | false |
| Snapshot policy | run `213` milestone snapshot audit | `90/90` milestones pass | true |

## Decision

Use the BEM return-inbox preflight/smoke, field bundle unpack smoke, and local
2D decision-boundary audit as the current handoff state. Do not start BEM 3D
validation, field FWI/GPU/3D, or source-factor full-batch work until their
listed gates are satisfied.

## Milestone Snapshot

This result-driven summary froze:

```text
run_local_bem_field_2d_handoff_readiness_scoreboard_full_suite_1345_refresh.py
sha256: 65650eed3698e6ce583660ad16b5def75caeec8910b52ac20002ca0a191a11ad

test_local_bem_field_2d_handoff_readiness_scoreboard_full_suite_1345_refresh.py
sha256: cdec78238ef552eae9e5530d7071d8614265523517c486a24ce9e0675be9fa8f
```

## Validation

Focused test:

```text
tests/test_local_bem_field_2d_handoff_readiness_scoreboard_full_suite_1345_refresh.py
2 passed
```

Full test suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1345 passed in 30.80 s
```

Figure check:

```text
local_bem_field_2d_handoff_readiness_scoreboard.png
1744x774, dynamic range=255
```
