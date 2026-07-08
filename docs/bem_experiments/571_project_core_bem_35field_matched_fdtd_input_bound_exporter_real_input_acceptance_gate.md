# BEM Experiment 571: Matched-FDTD Input-Bound Exporter Real Input Acceptance Gate

Date: 2026-06-30

## Purpose

Define the acceptance gate for the two future real matched-FDTD input CSV files
that can drive the input-bound return exporter.

Runs `568-570` produced and validated blank input templates plus non-executed
exporter commands. This run converts that handoff into a concrete gate:

```text
What must be present before the exporter can write accepted matched-FDTD return
files and before any BEM/FDTD comparison can be made?
```

This is a contract and current-state audit. It does not run FDTD, fill
templates, execute exporter commands, or compare BEM against FDTD.

## Output

```text
outputs/bem_experiments/571_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_file_gate_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_column_gate_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_action_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate.png
scripts/
```

## Result

```text
source template pack ready:                  true
source sensitivity ready:                    true
required real input files:                   2
required real input rows:                    558
required column gates:                       22
real input files currently present:          0
accepted real input files:                   0
accepted input rows:                         0
accepted return files present:               0
exporter commands:                           2
exporter commands executed:                  0
ready for exporter execution:                false
ready for real BEM/FDTD comparison:          false
ready for 3D validation claim:               false
ready for GPU/HPC:                           false
ready for field transfer:                    false
ready for field FWI:                         false
```

The required input files are:

| File key | Rows | Required value field | Value domain |
| --- | ---: | --- | --- |
| `fdtd_source_hash_manifest` | 279 | `returned_fdtd_source_hash` | lowercase SHA-256 hash |
| `fdtd_scattered_norm_values` | 279 | `returned_fdtd_scattered_norm` | positive finite float |

Each file has eleven required columns: five locked row-identity columns, five
real solver/provenance columns, and one real value column.

## Interpretation

The BEM side of the 35-field packet is accepted, but the matched-FDTD side still
has no real input files and no accepted return files. The comparison blocker is
now precise: two real matched-FDTD input CSVs must be produced with 558 total
rows and 22 file-column gates satisfied.

Blank templates and command strings are not evidence.

## Decision

Do not run a BEM/FDTD comparison, field transfer, field FWI, GPU/HPC escalation,
or 3D validation claim from this state. The next BEM-side step is to validate
this acceptance gate, then keep the branch blocked until real matched-FDTD input
files are available.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_input_bound_return_exporter.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_acceptance_gate.py

20 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
