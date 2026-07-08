# BEM Experiment 568: Matched-FDTD Input-Bound Exporter Template Command Pack

Date: 2026-06-30

## Purpose

Create the concrete handoff packet for the input-bound matched-FDTD exporter.

Run `567` added an exporter shell that can validate and write matched-FDTD
return CSV files only when real FDTD input rows are supplied. This run prepares
the two fillable input templates and the two non-executed commands needed to use
that exporter later.

This run does not supply real FDTD rows, execute exporter commands, write
accepted FDTD return evidence, run a BEM/FDTD comparison, launch GPU/HPC work,
transfer to field evidence, or promote 3D validation readiness.

## Output

```text
outputs/bem_experiments/568_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack
```

Key artifacts:

```text
data/real_fdtd_input_templates/fdtd_source_hash_manifest_real_input_template.csv
data/real_fdtd_input_templates/fdtd_scattered_norm_values_real_input_template.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_command_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source exporter audit ready:           true
template files:                        2
template rows:                         558
prefilled identity cells:              2790
blank real solver/provenance cells:    3348
future real input files required:      2
real input files present:              0
accepted output files written:         0
exporter commands:                     2
exporter commands executed:            0
contract probes:                       2
contract checks passed:                2
BEM/FDTD comparison ready:             false
3D validation ready:                   false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
pack ready:                            true
```

Template status:

| File key | Template rows | Prefilled cells | Blank real cells |
| --- | ---: | ---: | ---: |
| fdtd_source_hash_manifest | 279 | 1395 | 1674 |
| fdtd_scattered_norm_values | 279 | 1395 | 1674 |

## Interpretation

The row identity problem is now fully specified for the matched-FDTD return
path. Each required row has its pair key, worksheet row, receiver index,
frequency, and file key prefilled. The fields that would prove real FDTD
execution remain blank: solver run identifier, solver status, solver log hash,
input contract hash, real-export flag, and the returned FDTD value.

The generated commands intentionally point to future real input files, not to
the blank templates. They should be run only after the templates are filled with
real matched-FDTD solver output and provenance.

## Decision

Use run `568` as the current practical handoff packet for the BEM/FDTD bridge.
The next comparison-enabling work is to fill the two real input files from
matched FDTD runs and execute the two generated exporter commands.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_input_bound_return_exporter.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack.py
13 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
