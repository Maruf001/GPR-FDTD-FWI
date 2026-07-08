# BEM Experiment 341: Fresh-Case Full-Payload Replay Audit

Date: 2026-06-28

## Purpose

Independently replay the saved run `340` full-payload fresh-case arrays.

Run `340` repaired the artifact gap identified by runs `337-339`: it saved the
Tx background fields, Rx background fields, and source spectrum for each fresh
case. This run verifies that those saved arrays are sufficient to recompute the
adapter formula and reproduce the saved adapter outputs.

This is a CPU-only saved-payload replay audit. It does not run FDTD, launch GPU
or HPC work, use field data, use the synthetic 2D archive, run field FWI, or
make a field-transfer claim.

## Output

```text
outputs/bem_experiments/341_project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit_case_replay.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit_variant_metrics.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit_frequency_scales.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit_summary.json
figures/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_audit.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_FRESH_CASE_FULL_PAYLOAD_REPLAY_AUDIT.md
```

## Result

```text
source full-payload stress ready:   true
source payload completeness ready:  true
case count:                         3
replay-ready cases:                 3
replay-blocked cases:               0
all saved payloads replay ready:    true
fresh-case replay validation ready: true
field claim ready:                  false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

All three run `340` fresh-case payloads replay from the saved formula inputs.
The saved adapter frequency bins and time-band outputs are reproduced to
numerical precision for every case.

## Decision

Use run `341` as the executable replay checkpoint for the full-payload
fresh-case stress branch. The next step is a saved-artifact validator and
sensitivity test for this replay audit.
