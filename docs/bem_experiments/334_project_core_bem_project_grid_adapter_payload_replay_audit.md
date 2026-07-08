# BEM Experiment 334: Project-Grid Adapter Payload Replay Audit

Date: 2026-06-28

## Purpose

Replay the saved run `093` grid-aware adapter payload from its interface items.

This run checks whether the eight-item payload is not only present but
executable: it recomputes the formula variants from the stored transmitter
fields, receiver fields, target weights, source spectrum, and selected
frequency bins, then compares the replayed adapter output against the saved
run `093` adapter output.

This is a payload replay audit. It does not run FDTD, GPU/HPC work, field data,
field FWI, neural-network training, or synthetic 2D archive promotion.

## Output

```text
outputs/bem_experiments/334_project_core_bem_project_grid_adapter_payload_replay_audit
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_payload_replay_audit_payload_shapes.csv
data/project_core_bem_project_grid_adapter_payload_replay_audit_variant_metrics.csv
data/project_core_bem_project_grid_adapter_payload_replay_audit_frequency_scales.csv
data/project_core_bem_project_grid_adapter_payload_replay_audit_checks.csv
data/project_core_bem_project_grid_adapter_payload_replay_audit_summary.json
figures/project_core_bem_project_grid_adapter_payload_replay_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
target cells:                         753
scan positions:                       7
selected frequency bins:              17
variants replayed:                    3
source best variant:                  receiver_conjugate_div_source
replayed best variant:                receiver_conjugate_div_source
source best time symmetric L2:        0.5800814918790826
replayed best time symmetric L2:      0.5800814918790826
max frequency-bin replay delta:       0.0
max time-band replay delta:           0.0
validation checks:                    7
passed checks:                        7
failed checks:                        0
payload replay ready:                 true
field claim ready:                    false
3D validation ready:                  false
GPU work ready:                       false
field FWI ready:                      false
```

## Interpretation

The saved run `093` payload is replayable from its interface items. Recomputing
the three formula variants recovers the same best variant and reproduces the
saved adapter frequency bins and time-band output to numerical precision.

This is stronger than the earlier interface checks: it shows that the eight
interface items are sufficient to execute the current grid-aware payload
adapter without rerunning the original FDTD generation script.

## Decision

Use run `334` as the executable replay checkpoint for the eight-item
grid-aware payload. The branch remains a controlled BEM/FDTD adapter result and
does not promote field, historical-archive, 3D, GPU, or field-FWI claims.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_payload_replay_audit.py
3 passed
```

Figure validation:

```text
3364x842, dynamic range=255
```
