# BEM Experiment 349: Real-Pair Execution Readiness Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `348` real-pair execution readiness validator with
controlled damaged variants.

This uses saved artifacts only. It does not run FDTD, ingest real trace files,
compare real BEM/FDTD outputs, calibrate thresholds, launch GPU/HPC work, run
3D validation, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/349_project_core_bem_real_pair_execution_readiness_after_full_payload_replay_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_sensitivity_scenarios.csv
data/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_sensitivity_summary.json
figures/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_sensitivity.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_REAL_PAIR_EXECUTION_READINESS_AFTER_FULL_PAYLOAD_REPLAY_SENSITIVITY.md
```

## Result

```text
scenarios:                 17
expected pass:             1
observed pass:             1
expected failures:         16
observed failures:         16
unexpected outcomes:       0
sensitivity ready:         true
accepts exact run 347:     true
rejects damaged variants:  true
real-pair execution ready: false
3D validation ready:       false
GPU work ready:            false
field FWI ready:           false
```

## Interpretation

The real-pair readiness validator accepts the exact run `347` audit and
rejects controlled damage to gate counts, support readiness, required
real-artifact counts, real-pair promotion, downstream promotion, blocker
reasons, figure validation, and script snapshots.

## Decision

Use runs `347-349` as the guarded post-replay BEM real-pair execution gate.
The next comparison work remains real trace staging and frequency extraction,
not BEM replay repair.
