# BEM Experiment 569: Matched-FDTD Input-Bound Exporter Template Command Pack Validator

Date: 2026-06-30

## Purpose

Validate the run `568` matched-FDTD input-bound exporter template command pack.

Run `568` created two fillable input templates and two non-executed commands
for the input-bound matched-FDTD exporter. This run checks that the packet is
structurally valid and still non-evidence.

This run does not supply real FDTD rows, execute exporter commands, write
accepted FDTD return evidence, run a BEM/FDTD comparison, launch GPU/HPC work,
transfer to field evidence, or promote 3D validation readiness.

## Output

```text
outputs/bem_experiments/569_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source pack ready:                     true
checks:                                8
passed checks:                         8
failed checks:                         0
template files:                        2
template rows:                         558
blank real cells:                      3348
exporter commands:                     2
exporter commands executed:            0
accepted output files written:         0
BEM/FDTD comparison ready:             false
3D validation ready:                   false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
validation ready:                      true
```

Validation checks:

| Check | Passed |
| --- | --- |
| source pack ready | true |
| template file shape | true |
| identity fields prefilled | true |
| real solver provenance and values blank | true |
| commands are future-input commands | true |
| commands not executed | true |
| downstream remains blocked | true |
| figure and scripts exist | true |

## Interpretation

The run `568` packet is valid as a fillable handoff packet. It has the correct
two-file, 558-row shape; row identities are prefilled; real solver and
provenance fields remain blank; and the commands point to future real input
files rather than the blank templates.

## Decision

Use runs `568` and `569` as the guarded BEM/FDTD input-handoff packet. Do not
run the comparison, 3D validation claim, field transfer, or GPU/HPC escalation
until the two real matched-FDTD input files are filled and exported into
accepted return files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validator.py
3 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
