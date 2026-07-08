# Field Experiment 161: Controlled Collection Gate Sensitivity

Date: 2026-06-22

## Purpose

Use the accepted dry-run packet from run `160` as a baseline and remove one
collection-control family at a time. The goal is to check whether the field
packet validator catches each missing control before a real collection is used
for acceptance, inversion, or heavy work.

This is CPU-only dry-run sensitivity analysis. It is not measured field data
and does not authorize field full-waveform inversion, GPU work,
three-dimensional/high-performance-computing work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/161_gssi51600s_controlled_collection_gate_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_gate_sensitivity.csv
data/field_controlled_collection_gate_sensitivity_acceptance.csv
data/field_controlled_collection_gate_sensitivity_summary.json
docs/FIELD_COLLECTION_GATE_SENSITIVITY.md
```

## Result

```text
source dry run:                               160_gssi51600s_controlled_collection_packet_dry_run
variants tested:                             12
baseline packet accepted:                    true
blocked non-baseline variants:               11
all single-blocker variants block acceptance: true
baseline cross-table failures:               0
field-FWI/heavy-work ready variants:          1
current-archive field FWI ready:              false
heavy field work ready:                       false
field 3D/HPC ready:                           false
gpu priority:                                 none
```

The baseline dry-run packet passes all seven acceptance gates. Every tested
single-blocker variant fails packet acceptance:

```text
missing session metadata
missing target truth
missing profile geometry
missing profile file names / Tx-Rx offset / coupling condition
broken target cross-table link
missing time-zero measurements
only two time-zero references
missing amplitude measurements
only two amplitude references
missing reference file registry
only two controlled repeats
```

The `only_two_controlled_repeats` variant is useful because it has zero missing
required fields and zero cross-table failures, yet still fails
`short_repeat_redundancy` and `field_fwi_or_heavy_work`. That confirms the
repeat-count gate is not merely a metadata-completeness check.

## Interpretation

The controlled-collection packet can now be treated as a field-day quality
gate. A fully filled packet passes in dry run, but each missing-control family
blocks acceptance. This supports the collection workflow, not a measured-field
scientific claim.

The real next field action is still to collect measured target truth,
time-zero references, amplitude references, profile geometry, controlled
repeat profiles, and verified session/reference metadata into the run `158`
packet, then rerun the validator.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_gate_sensitivity.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_gate_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_gate_sensitivity.py: pass
```
