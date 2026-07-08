# BEM Experiment 829: Complex FDTD Adapter Input Stage-1 Live Return Contract

Date: 2026-07-01

## Purpose

Define the exact live-return contract for replacing the output-local stage-1
synthetic smoke from run `826` with a real FDTD complex-field return.

This run does not create the live file, execute FDTD, merge into the full
external input, pass preflight, write completed stage files, run comparison,
transfer to field evidence, or promote 3D/HPC work.

## Output

```text
outputs/bem_experiments/829_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_contract_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_action_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staged packet ready:                 true
source positive-control sensitivity ready:  true
stage-1 contract rows:                      1
required columns:                           12
full required rows:                         279
stage-1 live partial parent present:        true
stage-1 live partial file present:          false
full external input file present:           false
stage-1 direct full preflight ready:        false
accepted as full external input:            false
actions:                                    3
complete actions:                           0
completed stage files ready:                false
real BEM/FDTD comparison ready:             false
field transfer ready:                       false
3D/HPC ready:                               false
```

Expected stage-1 live partial path:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_partial.csv
```

Full external input path still required for preflight:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input.csv
```

## Interpretation

The first real producer return is now exact: one row, receiver index `15`,
frequency `1.0 GHz`, and the same 12-column complex-field schema used by the
full adapter input. The row must include finite `fdtd_real` and `fdtd_imag`
values, a source hash, solver run identifier, successful solver status, solver
log hash, real-export flag, and the canonical input contract hash.

The stage-1 partial file is only an incremental producer check. It cannot pass
the full external preflight by itself because the full preflight requires all
279 receiver-frequency identities.

## Decision

Use this contract for the first real FDTD complex-field return. Keep full
preflight, completed stage files, real BEM/FDTD comparison, field transfer, and
3D/HPC blocked until the 279-row external input exists and passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract.py
2 passed
```

Figure check:

```text
2645x919, dynamic range=255
```
