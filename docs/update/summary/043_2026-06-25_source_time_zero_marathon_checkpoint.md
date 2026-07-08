# Source/Time-Zero Marathon Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the local 2D source/time-zero continuation after the
field run `176` real-archive acceptance contract and the BEM payload milestone.

No new FDTD, GPU kernels, detector-FWI, field FWI, field 3D/HPC, or neural-
network training was launched.

## New Result Chain

Local 2D and summary-table outputs:

```text
142_local_2d_new_hypothesis_candidate_pack_field176_refresh
143_local_2d_matched_adapter_completion_audit
144_local_2d_source_time_zero_perturbation_replay_audit
145_local_2d_source_time_zero_replay_contract
146_local_2d_source_time_zero_selected_replay
147_local_2d_source_time_zero_robustness_gate
148_bem_field_2d_presentation_evidence_pack_source_time_zero_refresh
149_bem_field_2d_presentation_storyboard_source_time_zero_refresh
150_result_milestone_snapshot_audit_source_time_zero_refresh
```

Tracked experiment notes:

```text
docs/experiments/873_local_2d_new_hypothesis_candidate_pack_field176_refresh.md
docs/experiments/874_local_2d_matched_adapter_completion_audit.md
docs/experiments/875_local_2d_source_time_zero_perturbation_replay_audit.md
docs/experiments/876_local_2d_source_time_zero_replay_contract.md
docs/experiments/877_local_2d_source_time_zero_selected_replay.md
docs/experiments/878_local_2d_source_time_zero_robustness_gate.md
```

## Findings

Run `142` refreshed the local 2D hypothesis queue against the field run `176`
contract and the run `139` presentation pack. Field-to-2D prior replay is now
blocked on real archive acceptance, not synthetic archive smokes.

Run `143` corrected the queue: the generic matched 2D BEM/FDTD adapter is
already covered by BEM runs `014-016`, so rerunning a generic matched adapter is
not useful. The next useful local 2D branch became source-amplitude/time-zero
replay.

Run `144` scanned saved coordinate-objective diagnostics:

```text
diagnostic files audited:              648
diagnostic rows audited:               3807
replay-relevant files:                 645
nonzero time-shift files:              645
amplitude deviation >=5% files:        628
geometry-unstable files:               40
max absolute time shift ps:            50.0
max amplitude deviation percent:       48.64359318220286
```

Run `145` narrowed that broad audit to five cached replay cases and passed four
contract metrics.

Run `146` executed the selected replay:

```text
selected cases:                  5
selected rows:                   42
decision-sensitive cases:        2
geometry-stable cases:           3
max geometry span mm:            126.12394697280925
max time-shift span ps:          50.0
max amplitude span percent:      56.284751892158646
```

Run `147` converted the selected replay into a robustness gate:

```text
robust cases:                        3
blocked sensitive cases:             2
general source/time-zero claim ready: false
close14-like gate pass:              true
broad variable-radius claim ready:   false
new FDTD run ready:                  false
GPU work ready:                      false
field transfer ready:                false
```

## Current Decision

The source/time-zero result is mixed:

```text
scoped pass:  close10, close14, and low-effect control cases
blocked:      broad variable-radius cases with source/time-zero-sensitive geometry
```

Do not make a general source/time-zero robustness claim. Do not launch new
FDTD, GPU work, detector-FWI, field transfer, field FWI, or 3D/HPC from this
block.

## Presentation And Snapshot State

Run `148` refreshes the presentation evidence pack:

```text
claim count:                  45
ready scoped/operational:     37
blocked claims:               8
gpu or field FWI ready:       false
```

Run `149` refreshes the storyboard and preserves all eight blocked claims.

Run `150` refreshes the script-freezing audit:

```text
milestones audited:       19
passed milestones:        19
failed milestones:        0
snapshot files audited:   34
missing manifests:        0
sha mismatches:           0
source files missing:     0
snapshot policy pass:     true
```

## Validation

Focused source/time-zero and presentation tests:

```text
passed
```

Full test suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1165 passed in 30.40s
```

Whitespace check:

```text
git diff --check: pass
```

Resource check:

```text
RAM used: about 18 GiB of 119 GiB
GPU utilization: about 6 percent
```

## Next Marathon Branch

The marathon remains active. The next useful branch should be chosen from:

```text
1. BEM: tighten payload replacement reporting or 3D external-data acceptance;
2. Field: improve the real-archive operator/acceptance materials without pretending data exist;
3. Local 2D: derive a compact source/time-zero robustness table for report insertion;
4. Presentation: produce a concise team-meeting evidence brief from runs 098, 147, and 176.
```
