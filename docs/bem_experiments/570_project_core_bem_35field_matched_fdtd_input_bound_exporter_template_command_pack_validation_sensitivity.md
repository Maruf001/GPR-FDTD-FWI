# BEM Experiment 570: Matched-FDTD Input-Bound Exporter Template Command Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `569` validator for the matched-FDTD input-bound
exporter template command pack.

Run `569` validated the run `568` fillable input packet. This run checks that
the validator rejects damaged source readiness, template shape, command routing,
command execution, downstream promotion, figure, and script-snapshot states.

This run does not supply real FDTD rows, execute exporter commands, write
accepted FDTD return evidence, run a BEM/FDTD comparison, launch GPU/HPC work,
transfer to field evidence, or promote 3D validation readiness.

## Output

```text
outputs/bem_experiments/570_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
sensitivity cases:                     8
expected pass cases:                   1
expected fail cases:                   7
actual pass cases:                     1
actual fail cases:                     7
unexpected cases:                      0
damaged cases:                         7
BEM/FDTD comparison ready:             false
3D validation ready:                   false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
sensitivity ready:                     true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| source_ready_false | source pack readiness false |
| template_shape_damage | one template row-spec removed |
| command_routed_to_template | future input command points to blank template path |
| command_execution_promotion | exporter command marked executed |
| downstream_promotion | premature BEM/FDTD comparison promotion |
| figure_damage | figure path missing |
| script_snapshot_damage | script snapshot count missing |

## Interpretation

The guarded input-handoff block is now sensitivity-hardened. The validator
accepts only the exact non-evidence packet and rejects damaged routing or
promotion states that would otherwise risk confusing blank templates with real
matched-FDTD evidence.

## Decision

Use runs `568`-`570` as the guarded BEM/FDTD input-handoff block. The next
comparison-enabling work remains filling the two real matched-FDTD input files
and running the input-bound exporter.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_template_command_pack_validation_sensitivity.py
3 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
