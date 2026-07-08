# Experiment 1655: 84-Grid Pilot Real-Result Fillable Template Pack

Date: 2026-06-30

## Purpose

Create fillable JSON templates for the five future real pilot FDTD result
files.

Run `1654` defines the five non-executed JSON parse/checksum commands for
future real pilot outputs. This run materializes the expected JSON payloads in
the run output folder only. It pre-fills only stable design identity fields and
leaves solver, runtime, hash, result-summary, and execution-status fields blank
or null.

This run does not execute FDTD, accept pilot evidence, launch GPU work, or
promote field transfer or 3D/HPC readiness.

## Output

```text
outputs/experiments/1655_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack
```

Key artifacts:

```text
data/real_pilot_result_json_templates/
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_manifest_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source checklist ready:                    true
source command plan ready:                 true
template files:                            5
template fields:                           50
prefilled design fields:                   15
blank or null fields:                      35
JSON-parse-ready templates:                5
real result files:                         0
field-domain accepted files:               0
new FDTD executions:                       0
pilot evidence ready:                      0
bounded pilot execution ready:             false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
```

## Interpretation

The five pilot result payloads now have concrete, parseable templates. They are
not result files. The values that must come from real FDTD execution remain
blank or null.

## Decision

Use run `1655` as the fillable template pack for the five-row pilot. Fill the
templates only from real pilot FDTD execution outputs, then run the command
checks from run `1654` and rerun identity, field-domain, and acceptance gates.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack.py
4 passed
```

Figure check:

```text
2106x843, dynamic range=255
```
