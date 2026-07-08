# Field Experiment 545: Integrated Live Receipt Acceptance Frontier

Date: 2026-07-01

## Purpose

Join the measured-DZT signature gate and metadata JSON schema gate into one
live receipt frontier for the controlled field packet.

This run does not parse field data, accept provenance, promote an archive, run
field FWI, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/545_gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier_group_rows.csv
data/gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier_action_rows.csv
data/gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier_summary.json
figures/gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier.png
```

## Result

```text
receipt groups:                    3
actions:                           5
live receipt items required:        33
measured DZT slots:                 9
metadata JSON slots:                24
global metadata JSON files:         15
per-file metadata JSON files:       9
required metadata value fields:     96
parent directories present:         33
live files present:                 0
accepted live receipt items:        0
DZT signature passes:               0
metadata schema passes:             0
blank metadata value fields:        96
paired DZT signature passes:        0
complete actions:                   0
live receipt ready:                 false
parser ready:                       false
provenance ready:                   false
archive ready:                      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

## Interpretation

The field packet now has one current receipt boundary: nine measured `.DZT`
files must pass the GSSI DZT signature gate, and twenty-four metadata JSON
files must pass schema checks with real non-placeholder values. No live item is
present or accepted.

## Decision

Use this run as the current field live-receipt acceptance frontier. Keep
parser, provenance, archive, field FWI, and field 3D/HPC work blocked until all
33 live receipt items pass their gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_acceptance_frontier.py
3 passed
```

