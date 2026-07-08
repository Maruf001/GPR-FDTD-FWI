# BEM Experiment 808: Complex FDTD Adapter Input Template Pack

Date: 2026-07-01

## Purpose

Create the fill-in template for the real complex FDTD input required by the
matched BEM/FDTD complex-field comparison.

Runs `805-807` added and guarded the fail-closed writer dry run. This run turns
the guarded receiver-frequency identities and contract hash into a producer-side
CSV template that the FDTD export must fill with real complex values and
provenance.

## Output

```text
outputs/bem_experiments/808_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_input_template.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source interface guard ready:              true
source writer sensitivity ready:           true
adapter input columns:                     12
template rows:                             279
stages:                                    5
identity cells prefilled:                  1116
contract hash cells prefilled:             279
FDTD value blank cells:                    558
FDTD provenance blank cells:               1395
template ready for real FDTD fill:         true
contains real FDTD values:                 false
accepted as real FDTD input:               false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
field transfer ready:                      false
3D/HPC ready:                              false
gpu priority:                              none
```

The required contract hash is:

```text
8c0e4be114e3c7d8703aa8b0afaa468c6dd33968c62742fdff01bc52a736339a
```

## Interpretation

The template contains all 279 receiver-frequency identities needed by the
adapter. Only identity fields and the contract hash are prefilled. The 558 FDTD
real/imaginary value cells and 1395 FDTD provenance/status cells remain blank.

## Decision

Use this template as the real FDTD fill-in packet. Do not accept it as evidence
and do not run the comparison until the blank FDTD value and provenance fields
are replaced by real solver output and pass the adapter validator.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack.py

4 passed
```

Figure check:

```text
3004x918, dynamic range=255
```
