# Experiment 1666: 84-Grid Pilot Revised Real-Result Fillable Template Pack

Date: 2026-06-30

## Purpose

Refresh the fillable JSON result templates around the revised five-row pilot
payload set from runs `1664` and `1665`.

The old template pack still belonged to the earlier pilot identity that
included stale payload row `86`. This run creates the revised template pack for
payload rows `1;23;46;68;72`.

This run does not execute FDTD, fill measured result fields, accept pilot
evidence, launch GPU work, transfer to field evidence, or promote 3D/HPC
readiness.

## Output

```text
outputs/experiments/1666_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_field_value_domain_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_manifest_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_summary.json
data/real_pilot_result_json_templates/
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source revised checklist ready:         true
source revised command plan ready:      true
template files:                         5
template fields:                        50
required payload IDs:                   1;23;46;68;72
contains payload 68:                    true
contains stale payload 86:              false
contains retained_blend:                false
prefilled design fields:                20
blank or null measured fields:          30
JSON-parse-ready templates:             5
real result files:                      0
accepted field-domain rows:             0
new FDTD executions:                    0
pilot evidence-ready rows:              0
GPU work ready:                         false
field transfer ready:                   false
3D/HPC ready:                           false
template pack ready:                    true
```

The five generated template files are:

| Payload row | Grid model | Objective profile | Transition bin |
| ---: | --- | --- | ---: |
| 1 | dryrun90_001 | highband | 0 |
| 23 | dryrun90_023 | late | 4 |
| 46 | dryrun90_046 | late_high | 9 |
| 68 | dryrun90_068 | veryhigh | 13 |
| 72 | dryrun90_072 | veryhigh | 17 |

Each template pre-fills four design identity fields:
`payload_row_id`, `grid_model_id`, `objective_profile`, and `transition_bin`.
The measured result fields remain blank, `null`, or empty objects until a real
FDTD pilot run exists.

## Interpretation

The revised producer checklist, command plan, and fillable template pack now
agree on the same five payload rows. The stale `retained_blend` branch is no
longer present in the execution-preparation artifacts.

This is still only a prepared intake package. It proves that future real pilot
outputs have a consistent destination and schema, not that any FDTD result has
been computed.

## Decision

Use run `1666` as the revised template-pack source. The next defensible step is
to validate the revised checklist, command plan, and template pack together as
one coherent intake package before any real executor implementation or FDTD
execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack.py
4 passed
```

Figure check:

```text
2357x847, dynamic range=255
```
