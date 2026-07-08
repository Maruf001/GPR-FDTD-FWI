# Field Experiment 257: Controlled Collection Return Readiness Pack

Date: 2026-06-28

## Purpose

Combine the controlled-collection provenance closure from run `163` with the
guarded real-return boundary from runs `254-256`.

This run answers the practical handoff question:

```text
What is ready now, what must be collected, and what remains blocked after the
real controlled-collection files return?
```

This run does not execute future real-archive commands, inspect real measured
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/257_gssi51600s_controlled_collection_return_readiness_pack
```

Key artifacts:

```text
data/field_controlled_collection_return_readiness_rows.csv
data/field_controlled_collection_return_readiness_summary.json
data/figure_validation.csv
figures/field_controlled_collection_return_readiness_pack.png
docs/FIELD_CONTROLLED_COLLECTION_RETURN_READINESS_PACK.md
scripts/run_gssi_field_controlled_collection_return_readiness_pack.py
scripts/test_gssi_field_controlled_collection_return_readiness_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
readiness rows:                    13
collection action groups:          6
metadata action groups:            3
file action groups:                3
real files required:               9
controlled profile files:          3
time-zero reference files:         3
amplitude-reference files:         3
guarded return supports:           2
post-return blockers:              5
real-data blockers:                5
source structural ready:           true
source provenance ready:           false
collection-day execution ready:    true
post-execution boundary ready:     true
boundary sensitivity ready:        true
command plan guarded:              true
current guard execution guarded:   true
readiness pack ready:              true
real files present:                false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The field-side handoff is now one table rather than two separate decisions.
Six collection actions remain: three metadata/provenance actions and three file
action groups. The file groups require nine real files total: three controlled
profile repeats, three time-zero references, and three amplitude references.

The return-side guard work is ready. The real-return command checklist and the
current guard-execution smoke are both guarded. That readiness does not accept
the dry-run archive as field evidence. Five real-data/downstream blockers
remain until measured files and measured metadata exist.

## Decision

Use this run as the controlled field collection-return checklist. The current
dry-run archive cannot be promoted to field evidence. Do not launch field FWI,
field 3D/HPC, heavy GPU work, or neural-network training from the current field
archive.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_return_readiness_pack.py
3 passed
```

Figure validation:

```text
3221x885, dynamic range=255
```
