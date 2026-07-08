# BEM Experiment 347: Real-Pair Execution Readiness After Full-Payload Replay

Date: 2026-06-29

## Purpose

Audit whether the guarded full-payload replay repair makes a real matched
BEM/FDTD comparison executable.

This uses saved artifacts only. It does not run FDTD, ingest real trace files,
compare real BEM/FDTD outputs, calibrate thresholds, launch GPU/HPC work, run
3D validation, transfer to field evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/347_project_core_bem_real_pair_execution_readiness_after_full_payload_replay_audit
```

Key artifacts:

```text
data/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_audit_gate_rows.csv
data/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_audit_summary.json
figures/project_core_bem_real_pair_execution_readiness_after_full_payload_replay_audit.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_REAL_PAIR_EXECUTION_READINESS_AFTER_FULL_PAYLOAD_REPLAY_AUDIT.md
```

## Result

```text
gates:                              11
ready gates:                        3
blocked gates:                      8
real-data blockers:                 7
full-payload replay guarded:        true
replay-ready fresh cases:           3
max replay frequency delta:         0.0
max replay band delta:              0.0
trace intake manifest ready:        true
required trace files:               26
background / target traces:         13 / 13
receiver keys / frequency keys:     13 / 9
return-readiness pack ready:        true
threshold metrics:                  4
required metadata fields:           8
real trace files present:           false
real frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
real-pair execution ready:          false
broad BEM replacement ready:        false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

The BEM-side full-payload replay repair is guarded, and the real-trace intake
plus return-readiness contracts are available. A real matched BEM/FDTD
comparison is still not executable because the 26 target/background projected
scalar FDTD traces, scalar projection convention, time-zero reference,
amplitude reference, frequency extraction, paired residual table, and
calibrated thresholds are absent.

## Decision

Use this as the post-replay real-pair execution gate. The next BEM/FDTD
comparison step is not more replay repair; it is producing and staging the 26
real projected scalar FDTD traces with references and metadata, then extracting
frequency bins and running the guarded first-pair comparison path.
