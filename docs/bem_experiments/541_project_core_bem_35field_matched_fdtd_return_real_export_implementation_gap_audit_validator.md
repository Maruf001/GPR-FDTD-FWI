# BEM Experiment 541: Matched FDTD Return Real-Export Implementation Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `540` from its artifacts.

The implementation-gap audit should pass only when the schema source block is
ready, both FDTD exporter real-mode probes refuse, all four accepted-writer
real-mode probes refuse, implementation blockers remain open, downstream states
stay blocked, and figure/script snapshots are present.

## Output

```text
outputs/bem_experiments/541_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
implementation-gap validation ready:       true
FDTD exporter probes:                      2
writer probes:                             4
implementation blockers:                   4
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The five validation checks confirm:

```text
source_chain_ready                         pass
fdtd_exporter_real_mode_refuses            pass
accepted_writer_real_mode_refuses          pass
blockers_and_downstream_states_preserved   pass
figure_and_script_snapshots_present        pass
```

## Decision

Use this validator as the artifact guard for run `540`. The next BEM step is a
validation-sensitivity run that proves exporter, writer, and downstream
promotion are rejected.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_implementation_gap_audit_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
