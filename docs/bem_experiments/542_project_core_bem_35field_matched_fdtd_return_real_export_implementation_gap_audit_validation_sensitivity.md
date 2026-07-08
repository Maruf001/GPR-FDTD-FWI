# BEM Experiment 542: Matched FDTD Return Real-Export Implementation Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `541` validator.

The exact run `540` implementation-gap audit should pass. Damaged source
readiness, exporter probe counts, exporter refusals, exporter enablement,
exported-value promotion, writer probe counts, writer refusals, writer
enablement, accepted-file promotion, evidence promotion, blocker readiness,
blocker counts, downstream promotion, figure damage, and script-snapshot damage
should fail.

## Output

```text
outputs/bem_experiments/542_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     16
expected pass scenarios:                   1
expected failure scenarios:                15
unexpected scenarios:                      0
implementation-gap sensitivity ready:      true
exact source artifacts pass:               true
exporter damage rejected:                  true
writer damage rejected:                    true
blocker damage rejected:                   true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
exporter_probe_count_drift
exporter_refusal_count_drift
exporter_enabled_promotion
exporter_value_promotion
writer_probe_count_drift
writer_refusal_count_drift
writer_enabled_promotion
accepted_file_promotion
evidence_promotion
blocker_ready_promotion
blocker_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `540-542` as the guarded matched-FDTD real-export implementation-gap
block. The next BEM implementation task is real FDTD value export into the run
`537` schema, not accepted comparison evidence or field transfer.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
3077x839, dynamic range=255
```
