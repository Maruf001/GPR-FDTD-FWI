# Field Experiment 162: Controlled Collection Provenance Gate

Date: 2026-06-22

## Purpose

Add a provenance gate above the ordinary controlled-packet validator. Run `160`
proved that a fully filled packet can pass the structural validator. This run
checks whether that same accepted dry-run packet would still be blocked before
any scientific field claim because it contains artificial placeholders,
future/sentinel dates, and file references that do not resolve to real data.

This is CPU-only validation. It does not run DZT preprocessing,
finite-difference time-domain simulation, full-waveform inversion, GPU kernels,
field full-waveform inversion, three-dimensional/high-performance-computing
work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/162_gssi51600s_controlled_collection_provenance_gate
```

Key artifacts:

```text
data/field_controlled_collection_structural_findings.csv
data/field_controlled_collection_structural_table_status.csv
data/field_controlled_collection_structural_acceptance_status.csv
data/field_controlled_collection_provenance_findings.csv
data/field_controlled_collection_provenance_gate_summary.json
docs/FIELD_COLLECTION_PROVENANCE_GATE.md
```

## Result

```text
packet checked:                         160_gssi51600s_controlled_collection_packet_dry_run/dry_run_packet
packet tables:                          5
packet rows:                            12
structural packet acceptance:           true
structural blocking findings:           0
structural missing required values:     0
structural cross-table failures:        0
structural ready acceptance gates:      7 / 7
provenance ready:                       false
provenance blocking findings:           42
placeholder-token findings:             32
missing file-reference findings:        9
future-date findings:                   1
scientific field claim ready:           false
current-archive field FWI ready:        false
heavy field work ready:                 false
field 3D/HPC ready:                     false
gpu priority:                           none
```

## Interpretation

The result is the intended safety behavior. The ordinary packet validator
accepts the dry-run packet because every required field is filled and all joins
are valid. The provenance gate rejects the same packet because the values are
clearly artificial and the referenced files do not exist.

This creates a two-stage field acceptance policy:

1. The structural validator checks whether the packet is complete and internally
   joined.
2. The provenance gate checks whether the completed packet can be treated as
   real field evidence.

Dry-run packets can pass stage 1 but must fail stage 2.

## Decision

Use the provenance gate after packet validation and before any measured-field
scientific claim, field full-waveform inversion, heavy GPU work, or
three-dimensional/high-performance-computing escalation. A future real packet
must pass both structural validation and provenance validation.

## Validation

Focused provenance-gate tests:

```text
tests/test_gssi_field_controlled_collection_provenance_gate.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_provenance_gate.py: pass
tests/test_gssi_field_controlled_collection_provenance_gate.py: pass
```
